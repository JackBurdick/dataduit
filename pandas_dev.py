conf_dict = {
    "meta": {
        "name": "albalone",
        # "root_location": "../datasets",  # relative path
        "logging": {"log_stream_level": "INFO"},
        "in": {
            "from": "memory",  # memory, local, online
            "type": "pandas",  # records, pandas, numpy, tfd, TODO:include popular websites
        },
    },  # The name must be valid if using tf
    "read": {  # create_ds should call obtain()
        # "from_stage": "memory",  # ["records","preprocessed"]
        # "split_defaults": False # this would use the default splits specified (by TF datasets)
        # TODO: in the parse_config - ensure these values sum to 100
        "split_percents": [75, 15, 10],  # currently only support percents
        "split_names": ["train", "val", "test"],
        # if "out" is missing in each of "identifier", "datatype", "shape", and "missing", in is used
        "iterate": {
            "return_type": "tuple",  # ["tuple", or dict]
            "schema": {  # the order defined below is the order in which items will be returned. only simple logic allowed
                # TODO: we need to ensure there are no name collisions here/across each highlevel grouping
                "x": {
                    "length": {
                        "datatype": {
                            "in": {
                                "type": "FixedLenFeature",
                                "options": {"dtype": "int64", "shape": 1},
                            },
                            "out": {},
                        },
                        "special": "decode",
                    },
                    "diameter": {
                        "datatype": {
                            "in": {
                                "type": "FixedLenFeature",
                                "options": {"dtype": "int64", "shape": 1},
                            },
                            "out": {},
                        },
                        "special": "decode",
                    },
                },
                "y": {
                    "rings": {
                        "datatype": {
                            "in": {
                                "type": "FixedLenFeature",
                                "options": {"dtype": "int64", "shape": 1},
                            },
                            "out": {},
                        }
                    },
                    # "missing": {"skip_row": True, "log": True, "create_mask": True},
                    # "statistics": {<if anything is known.. max/min val, median, basic stats?>}}
                },
            },
        },
    },
}
# missing:
#             skip: ['True', 'False']
#             log:
#                 location: "<_path_>"
#             fill_with: ['nan', 'mean', 'median', ...]
#             mask: ['True', 'False']
