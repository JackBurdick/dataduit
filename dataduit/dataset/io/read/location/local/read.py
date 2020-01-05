from dataduit.log.dataduit_logging import config_logger
from dataduit.dataset.io.download.location.online.tfd.tfd import obtain_tfd


def read_local(config_dict):
    logger = config_logger(config_dict["meta"]["logging"], "read")
    logger.debug(f"download_online({config_dict})")

    # TODO: this will need to change. only set up this way since tf will automatically
    # download or read
    if config_dict["meta"]["in"]["type"] == "tfd":
        datasets = obtain_tfd(config_dict)
    else:
        raise NotImplementedError(
            f"read_local type 'meta':'in':'type' {config_dict['meta']['in']['type']} not supported yet"
        )

    return datasets

