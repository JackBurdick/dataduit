from dataduit.dataset.io.read.location.local.read import read_local
from dataduit.dataset.io.read.location.memory.read import read_memory


def read(config_dict):

    # TODO: this needs to be corrected
    if config_dict["read"]["from_stage"] == "records":
        raise NotImplementedError("reading from records not supported yet")
    elif config_dict["read"]["from_stage"] == "preprocessed":
        datasets = read_local(config_dict)
    else:
        raise NotImplementedError(
            f"reading from {config_dict['read']['from']} not supported yet"
        )

    return datasets
