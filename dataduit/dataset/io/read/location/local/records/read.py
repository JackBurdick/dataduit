import pathlib

import tensorflow as tf
import tensorflow_datasets as tfds
from dataduit.log.dataduit_logging import config_logger


def read_tf_from_dir(config_dict):
    logger = config_logger(config_dict["meta"]["logging"], "download")
    logger.debug(f"obtain_datasets({config_dict}")

    try:
        root_dir = config_dict["meta"]["root_location"]
    except KeyError:
        raise KeyError(f"no dataset meta:root_location name specified")

    try:
        dataset_name = config_dict["meta"]["name"]
    except KeyError:
        # TODO: list names in the root_location
        raise KeyError(f"no dataset meta:name name specified")

    try:
        stage = config_dict["read"]["from_stage"]
    except KeyError:
        # TODO: list names in the root_location
        raise KeyError(f"no dataset meta:name name specified")

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

    records_dir = pathlib.Path(root_dir).joinpath(dataset_name).joinpath(stage)
    if not records_dir.is_dir():
        raise ValueError(f"indicated directory does not exist: {records_dir}")
    logger.info(f"records_dir set to {records_dir}")

    # create splits
    # TODO: ensure this:
    # 1) shuffles
    # 2) is consistent each call
    # ds_split_percents = tfds.Split.TRAIN.subsplit(split_percents)

    # create dataset
    datasets = {}
    # for i, ds_split_percent in enumerate(ds_split_percents):
    #     cur_ds = tfds.load(
    #         dataset_name,
    #         data_dir=records_dir,
    #         split=ds_split_percent,
    #         as_supervised=True,
    #     )
    #     datasets[split_names[i]] = cur_ds

    # TODO: is this the right way to resolve the path to string?
    # print(list(records_dir.glob("*")))
    file_paths = [str(fp) for fp in list(records_dir.glob("*"))]

    SEED = 42
    filepath_dataset = tf.data.Dataset.list_files(file_paths, seed=SEED)

    # TODO: interesting example: https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset?version=stable
    # d = d.filter(lambda x: x < 3)

    full_dataset = filepath_dataset.interleave(
        lambda filepath: tf.data.TFRecordDataset(filepath),
        cycle_length=tf.data.experimental.AUTOTUNE,
    )

    feature_description = {
        # TODO: abstract
        # TODO: shape
        "image": tf.io.VarLenFeature(tf.string),
        "label": tf.io.FixedLenFeature([], dtype=tf.int64),
    }

    def _parse_function(example_proto):
        # Parse the input `tf.Example` proto using the dictionary above.
        return tf.io.parse_single_example(example_proto, feature_description)

    full_dataset = full_dataset.map(_parse_function)

    def _decode(example_proto):
        # decode the values
        # NOTE: may convert to more explicit decode_<img_type>
        example_proto["image"] = tf.io.decode_image(example_proto["image"].values[0])
        return example_proto

    full_dataset = full_dataset.map(_decode)

    datasets["train"] = full_dataset

    return datasets

