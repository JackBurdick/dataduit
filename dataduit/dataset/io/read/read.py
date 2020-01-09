from dataduit.dataset.io.read.location.local.read import read_local
from dataduit.dataset.io.read.location.memory.read import read_memory


def read(config_dict, obj=None):

    # TODO: this logic block will need to be rewritten to something a little more understandable
    ACCEPTED_TYPES = ["records", "pandas", "numpy", "tfd"]
    try:
        stage = config_dict["read"]["from_stage"]
    except KeyError:
        try:
            meta_from = config_dict["meta"]["in"]["from"]
        except KeyError:
            raise ValueError(
                f"read:from_stage not specified and meta:in:from not specified"
            )

        if meta_from == "memory":
            stage = "memory"

            try:
                data_read_type = config_dict["meta"]["in"]["type"].lower()
            except KeyError:
                raise KeyError(
                    f"meta:in:type: currently not specified, please select one of {ACCEPTED_TYPES}"
                )

            if not data_read_type in ACCEPTED_TYPES:
                raise ValueError(
                    f"{data_read_type} currently not supported, please select one of {ACCEPTED_TYPES}"
                )
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

        # TODO: push block down a level
        if data_read_type == "pandas":
            raise NotImplementedError(f"{data_read_type} currently not supported")
        elif data_read_type == "records":
            raise NotImplementedError(f"{data_read_type} currently not supported")
        elif data_read_type == "tfd":
            raise NotImplementedError(f"{data_read_type} currently not supported")
        elif data_read_type == "numpy":
            raise NotImplementedError(f"{data_read_type} currently not supported")
        else:
            raise NotImplementedError(f"{data_read_type} currently not supported")

    else:
        raise NotImplementedError(
            f"reading from {config_dict['read']['from']} not supported yet"
        )

    return datasets
