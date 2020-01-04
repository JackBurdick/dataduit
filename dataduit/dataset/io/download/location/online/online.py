from dataduit.dataset.io.download.location.online.tf.download import obtain_tfd
from dataduit.log.dataduit_logging import config_logger


def download_online(config_dict, only_information=False):
    logger = config_logger(config_dict["logging"], "download")
    logger.debug(f"download_online({config_dict}, {only_information})")

    if config_dict["obtain"]["type"] == "tf":
        obtain_tfd(config_dict, only_information)
    pass
