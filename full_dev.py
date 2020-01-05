conf_dict = {
    "meta": {
        "name": "mnist",
        "root_location": "<some_path>",
        "logging": {"log_stream_level": "INFO"},
        "in": {
            "from": "online",  # memory, local, online
            "type": "tfd",  # pandas, numpy, tfd, TODO:include popular websites
            "location": "<location>",  # may not be relevant
        },
    },  # The name must be valid if using tf
    "obtain_datasets": {
        "raw": {
            "out": {"out_ext": None}  # [parquet, pickle, ...], None will use a default
        },
        "records": {
            "in": {  # from raw.. for now I may rely on pandas for this
                "type": "directory",  # directory/file
                "contains": "multiple",  # if each _x_ either has multiple or single entries. e.g. single=image file, multiple=pandas row
                "features": {
                    "feature_a": {
                        "special": {
                            "type": "path",
                            "to_do": "read",
                            "image": {"encoding": "<some_ext>"},
                        },  # I'm thinking about a path to imagery here
                        "identifier": {"in": {}, "out": {}},
                        "datatype": {"in": {}, "out": {}},
                        "shape": {"in": {}, "out": {}},
                        "missing": {"skip_row": True, "log": True, "create_mask": True},
                    },
                    "feature_b": {
                        "identifier": {"in": {}, "out": {}},
                        "datatype": {"in": {}, "out": {}},
                        "shape": {"in": {}, "out": {}},
                        "missing": {"skip_row": True, "log": True, "create_mask": True},
                    },
                },
            },
            "out": {"partitions": {"num": None}},
        },
        "preprocessed": {"in": {}, "out": {}},
        "read": {  # create_ds should call obtain()
            "from": "preprocessed",  # ["records","preprocessed"]
            # "split_defaults": False # this would use the default splits specified (by TF datasets)
            "split_percents": [75, 15, 10],  # currently only support percents
            "split_names": ["train", "val", "test"],
        },
    },
}
# missing:
#             skip: ['True', 'False']
#             log:
#                 location: "<_path_>"
#             fill_with: ['nan', 'mean', 'median', ...]
#             mask: ['True', 'False']
