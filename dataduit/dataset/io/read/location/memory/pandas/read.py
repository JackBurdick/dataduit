import math

import pandas as pd
import tensorflow as tf

from dataduit.libraries.tensorflow.components.dtype import return_dtype


def _split_df(config_dict, df):

    TOLERANCE_PERCENT = 0.02
    full_len = len(df)

    try:
        split_percents = config_dict["read"]["split_percents"]
    except KeyError:
        raise KeyError(
            f"no split specified. Please specify a split. an example may be {[75, 15, 10]}"
        )

    try:
        split_names = config_dict["read"]["split_names"]
    except KeyError:
        raise KeyError(
            f"no split specified. Please specify a split. an example may be {['train', 'val', 'test']}"
        )

    assert len(split_percents) == len(
        split_names
    ), f"dataset percents(len:{len(split_percents)})and names(len:{len(split_names)}) don't match splits({split_percents}), names({split_names})"

    RANDOM_SEED = 42
    dsdfs = {}
    out_df, tmp_df = None, None
    percent_obtained = 0
    for i, cur_split in enumerate(split_names):
        cur_percent = split_percents[i]
        if cur_percent > 1:
            cur_percent /= 100
        if not isinstance(tmp_df, pd.DataFrame):
            out_df = df.sample(frac=cur_percent, random_state=RANDOM_SEED)
            df = df.drop(out_df.index)
            tmp_df = df.copy()
        else:
            # math
            percent_left = 1 - percent_obtained
            percent_to_obtain = cur_percent / percent_left
            out_df = tmp_df.copy()
            out_df = out_df.sample(frac=percent_to_obtain, random_state=RANDOM_SEED)
            tmp_df = tmp_df.drop(out_df.index)
        percent_obtained += cur_percent
        dsdfs[cur_split] = out_df

    new_len = 0
    for split, split_df in dsdfs.items():
        new_len += len(split_df)

    assert math.isclose(
        full_len, new_len, abs_tol=(TOLERANCE_PERCENT * full_len)
    ), f"{new_len} not within {TOLERANCE_PERCENT}% of {full_len}"

    return dsdfs


def _df_to_ds(config_dict, df):

    # TODO: this is where statistics could be calculated/stored

    outer_keys = config_dict["read"]["iterate"]["schema"].keys()
    outter_dict = {}
    for k in outer_keys:
        outer = config_dict["read"]["iterate"]["schema"][k]
        inner_dict = {}
        for k_inner in outer.keys():
            # use indictator if specified, else name of feature
            try:
                indictator = outer[k_inner]["indicator"]
            except KeyError:
                indictator = k_inner

            try:
                dt_conf = outer[k_inner]["datatype"]["in"]["options"]
            except KeyError:
                raise KeyError(
                    f"no datatype config defined for key {k}, feat {indictator}: {config_dict['read']['iterate']['schema']}"
                )

            try:
                out_dtype = dt_conf["dtype"]
            except KeyError:
                out_dtype = str(df[indictator].dtype)

            try:
                out_shape = dt_conf["shape"]
            except KeyError:
                out_shape = None
                # TODO: there should include some logic here for the curent numpy shape

            # extract and convert
            vals = df[indictator].values
            return_dtype(out_dtype)

            # TODO: there should likely be some warning logic about converting types here
            # e.g. going from float to int
            # TODO: may need some slight adapter here if the naming scheme is off
            # e.g. if <___> names the type int_64 and the tf logic expects int64
            vals = tf.cast(vals, out_dtype)

            # reshape
            # vals = tf.reshape(vals, tf.TensorShape([out_shape]))
            if out_shape == 1:
                # TODO: this is sloppy, but works currently
                vals = tf.expand_dims(vals, -1)

            inner_dict[k_inner] = vals  #

            # inner_dict[k_inner] = vals

        outter_dict[k] = inner_dict

    ds = tf.data.Dataset.from_tensor_slices(outter_dict)

    # return logic
    try:
        r_type = config_dict["read"]["iterate"]["return_type"]
    except KeyError:
        r_type = None

    def _output_as_tuple(example_proto):
        keys = example_proto.keys()
        o = []
        for k in keys:
            el = example_proto[k]
            if isinstance(el, dict):
                # if a nested dict, e.g. ["x"]["feat_a"]
                out = _output_as_tuple(el)
            else:
                out = el
            o.append(out)

        return tf.tuple(o)

    if r_type == "tuple":
        # TODO: this ...works... but it will need to be profiled and optimized
        # particularly the part in _output_as_tuple where we iterate over the keys
        ds = ds.map(_output_as_tuple)

    return ds


def _pandas_to_datasets(config_dict, dsdfs):
    datasets = {}
    for split, df in dsdfs.items():
        datasets[f"{split}"] = _df_to_ds(config_dict, df)
    return datasets


def read_pandas(config_dict, df):

    datasets = None

    # split according to the specified split
    dsdfs = _split_df(config_dict, df)

    # convert to datasets
    datasets = _pandas_to_datasets(config_dict, dsdfs)

    return datasets
