from dataduit.dataset.io.read.location.local.read import read_local
from dataduit.dataset.io.read.location.memory.read import read_memory


def read(config_dict, obj=None):

    try:
        stage = config_dict["read"]["from_stage"]
    except KeyError:
        # if a stage is not defined, see if it's because we're operating on a memory object
        try:
            meta_from = config_dict["meta"]["in"]["from"]
        except KeyError:
            raise ValueError(
                f"read:from_stage not specified and meta:in:from not specified"
            )
        if meta_from == "memory":
            stage = "memory"
        else:
            raise KeyError(
                f"meta:in:from is specified as {meta_from} but only 'memory' is currently supported"
            )

    # TODO: this needs to be corrected
    if stage == "records":
        raise NotImplementedError("reading from records not supported yet")
    elif stage == "preprocessed":
        datasets = read_local(config_dict)
    elif stage == "memory":
        if obj is None:
            raise ValueError(
                f"{stage} is specified to 'memory', but no object is present"
            )
        datasets = read_memory(config_dict, obj)
    else:
        raise NotImplementedError(
            f"reading from {config_dict['read']['from']} not supported yet"
        )

    return datasets
