from dataduit.dataset.io.download.location.online.online import download_online
from dataduit.dataset.io.download.location.online.tfd.tfd import information_tfd
from dataduit.log.dataduit_logging import config_logger


def download(config_dict):
    logger = config_logger(config_dict["meta"]["logging"], "download")
    logger.debug(f"download({config_dict})")

    if config_dict["obtain"]["primary_location"] == "online":
        download_online(config_dict)


def info(config_dict):
    logger = config_logger(config_dict["meta"]["logging"], "download")
    logger.debug(f"info({config_dict})")

    # TODO: this will need to be a little more robust
    if config_dict["meta"]["in"]["type"] == "tfd":
        information = information_tfd(config_dict)

    return information

