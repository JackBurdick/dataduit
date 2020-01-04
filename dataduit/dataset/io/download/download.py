from dataduit.dataset.io.download.location.online.online import download_online
from dataduit.log.dataduit_logging import config_logger


def download(config_dict, only_information=False):
    logger = config_logger(config_dict["logging"], "download")
    logger.debug(f"download({config_dict})")

    if config_dict["obtain"]["primary_location"] == "online":
        download_online(config_dict, only_information)


def info(config_dict):
    logger = config_logger(config_dict["logging"], "download")
    logger.debug(f"info({config_dict})")

    download(config_dict, only_information=True)
