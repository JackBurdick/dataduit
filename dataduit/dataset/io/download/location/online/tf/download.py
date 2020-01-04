from dataduit.dataset.io.download.location.online.tf.tfd_handler.tfd_util import (
    obtain_datasets,
)
from dataduit.dataset.io.download.location.online.tf.tfd_handler.tfd_util import (
    dataset_info,
)
from dataduit.log.dataduit_logging import config_logger
from typing import Any, Dict


def obtain_tfd(config_dict, only_information=False):
    logger = config_logger(config_dict["logging"], "download")
    logger.debug("obtain_tfd")

    datasets: Dict[str, Any] = obtain_datasets(config_dict)
    return datasets


def information_tfd(config_dict):
    logger = config_logger(config_dict["logging"], "download")
    logger.debug("information_tfd")

    information = dataset_info(config_dict)
    return information
