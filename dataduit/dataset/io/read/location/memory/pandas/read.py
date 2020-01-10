import math

import pandas as pd


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


def read_pandas(config_dict, df):

    datasets = None

    # split according to the specified split
    _split_df(config_dict, df)

    raise NotImplementedError("TODO: convert to tf dataset")

    return datasets
