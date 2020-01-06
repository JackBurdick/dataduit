from dataduit.log.dataduit_logging import config_logger
from dataduit.dataset.io.download.location.online.tfd.tfd import obtain_tfd
from dataduit.dataset.io.read.location.local.records.read import read_tf_from_dir


def read_local(config_dict):
    logger = config_logger(config_dict["meta"]["logging"], "read")
    logger.debug(f"download_online({config_dict})")

    try:
        read_type = config_dict["meta"]["in"]["type"]
    except KeyError:
        read_type = None
        logger.info(
            "read_local type 'meta':'in':'type' not defined, set to 'records' by default"
        )

    # TODO: this will need to change. only set up this way since tf will automatically
    # download or read
    if read_type == "tfd":
        datasets = obtain_tfd(config_dict)
    elif read_type == "records" or not read_type:
        datasets = read_tf_from_dir(config_dict)
    else:
        raise NotImplementedError(
            f"read_local type 'meta':'in':'type' {config_dict['meta']['in']['type']} not supported yet"
        )

    return datasets

