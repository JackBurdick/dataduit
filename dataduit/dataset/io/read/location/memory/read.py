from dataduit.dataset.io.read.location.memory.pandas.read import read_pandas


def read_memory(config_dict, obj):

    ACCEPTED_TYPES = ["records", "pandas", "numpy", "tfd"]
    try:
        data_read_type = config_dict["meta"]["in"]["type"].lower()
    except KeyError:
        data_read_type = None
        raise KeyError(
            f"meta:in:type: currently not specified, please select one of {ACCEPTED_TYPES}"
        )

    if not data_read_type in ACCEPTED_TYPES:
        raise ValueError(
            f"{data_read_type} currently not supported, please select one of {ACCEPTED_TYPES}"
        )

        # TODO: push block down a level
    if data_read_type == "pandas":
        datasets = read_pandas(config_dict, obj)
    elif data_read_type == "records":
        raise NotImplementedError(f"{data_read_type} currently not supported")
    elif data_read_type == "tfd":
        raise NotImplementedError(f"{data_read_type} currently not supported")
    elif data_read_type == "numpy":
        raise NotImplementedError(f"{data_read_type} currently not supported")
    else:
        raise NotImplementedError(f"{data_read_type} currently not supported")

    return datasets
