from dataduit.log.dataduit_logging import config_logger
from dataduit.dataset.io.download.location.online.tf.download import obtain_tfd


def read_local(config_dict):
    logger = config_logger(config_dict["logging"], "read")
    logger.debug(f"download_online({config_dict})")

    # TODO: this will need to change. only set up this way since tf will automatically
    # download or read
    if config_dict["obtain"]["type"] == "tf":
        datasets = obtain_tfd(config_dict)
        return datasets

