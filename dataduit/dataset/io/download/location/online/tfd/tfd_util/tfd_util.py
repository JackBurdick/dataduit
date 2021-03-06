from typing import Any, Dict

import tensorflow_datasets as tfds
import pathlib

from dataduit.log.dataduit_logging import config_logger


def obtain_datasets(config_dict: Dict[str, Any]) -> Dict[str, Any]:
    logger = config_logger(config_dict["meta"]["logging"], "download")
    logger.debug(f"obtain_datasets({config_dict}")

    try:
        dataset_name = config_dict["meta"]["name"]
    except KeyError:
        raise KeyError(
            f"no dataset specified. please select one of {tfds.list_builders()}"
        )

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

    try:
        root_dir = config_dict["meta"]["root_location"]
        root_dir = pathlib.Path(root_dir).joinpath("tfd")
    except KeyError:
        root_dir = None
    logger.info(f"root dir set to {root_dir}")

    # TODO: another option should be to use the common/listed test split
    # TODO: ensure:
    # 1) shuffling
    # 2) consistency
    # https://github.com/tensorflow/datasets/blob/e53f3af5997bd0af9f7e61de3b8c98d8254e07b6/docs/splits.md

    # TODO: ensure this:
    # 1) shuffles
    # 2) is consistent each call
    ds_split_percents = tfds.Split.TRAIN.subsplit(split_percents)
    datasets = {}
    for i, ds_split_percent in enumerate(ds_split_percents):
        cur_ds = tfds.load(
            dataset_name, data_dir=root_dir, split=ds_split_percent, as_supervised=True
        )
        datasets[split_names[i]] = cur_ds

    return datasets


def dataset_info(config_dict: Dict[str, Any]) -> Any:

    # returntype: tensorflow_datasets.core.dataset_info.DatasetInfo
    logger = config_logger(config_dict["meta"]["logging"], "download")
    logger.debug(f"dataset_info({config_dict}")

    try:
        dataset_name = config_dict["meta"]["name"]
    except KeyError:
        raise KeyError(
            f"no dataset specified. please select one of {tfds.list_builders()}"
        )

    ds_builder = tfds.builder(dataset_name)
    return ds_builder.info
