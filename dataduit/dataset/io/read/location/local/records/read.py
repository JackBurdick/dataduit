import pathlib


def read_tf_from_dir(config_dict):

    try:
        root_dir = config_dict["meta"]["root_location"]
    except KeyError:
        raise KeyError(f"no dataset meta:root_location name specified")

    try:
        dataset_name = config_dict["meta"]["name"]
    except KeyError:
        # TODO: list names in the root_location
        raise KeyError(f"no dataset meta:name name specified")

    try:
        stage = config_dict["read"]["from_stage"]
    except KeyError:
        # TODO: list names in the root_location
        raise KeyError(f"no dataset meta:name name specified")

    records_dir = pathlib.Path(root_dir).joinpath(dataset_name).joinpath(stage)

    print(records_dir)

    raise NotImplementedError(f"read_tf_from_dir() not implemented yet")
