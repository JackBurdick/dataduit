conf_dict = {
    "meta": {
        "name": "xist",
        "root_location": "../datasets",  # relative path
        "logging": {"log_stream_level": "INFO"},
        "in": {
            "from": "online",  # memory, local, online
            "type": "records",  # records, pandas, numpy, tfd, TODO:include popular websites
            "location": "<location>",  # may not be relevant
        },
    },  # The name must be valid if using tf
    "read": {  # create_ds should call obtain()
        "from_stage": "preprocessed",  # ["records","preprocessed"]
        # "split_defaults": False # this would use the default splits specified (by TF datasets)
        "split_percents": [75, 15, 10],  # currently only support percents
        "split_names": ["train", "val", "test"],
        # if "out" is missing in each of "identifier", "datatype", "shape", and "missing", in is used
        "iterate": {
            "schema": {
                "x": {
                    "identifier": {"in": "image"},
                    "datatype": {"in": "int64", "out": {}},
                    "shape": {"in": {"dim": [28, 28, 1]}, "out": {}},
                    "missing": {"skip_row": True, "log": True, "create_mask": True},
                    # "statistics": {<if anything is known.. max/min val, median, basic stats?>}
                },
                "y": {
                    "identifier": {"in": "label"},
                    "datatype": {"in": {}, "out": {}},
                    "shape": {"in": {}, "out": {}},
                    "missing": {"skip_row": True, "log": True, "create_mask": True},
                    # "statistics": {<if anything is known.. max/min val, median, basic stats?>}
                },
            }
        },
    },
}
# missing:
#             skip: ['True', 'False']
#             log:
#                 location: "<_path_>"
#             fill_with: ['nan', 'mean', 'median', ...]
#             mask: ['True', 'False']
