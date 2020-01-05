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
    "read": {  # create_ds should call obtain()
        "from": "preprocessed",  # ["records","preprocessed"]
        # "split_defaults": False # this would use the default splits specified (by TF datasets)
        "split_percents": [75, 15, 10],  # currently only support percents
        "split_names": ["train", "val", "test"],
    },
}
# missing:
#             skip: ['True', 'False']
#             log:
#                 location: "<_path_>"
#             fill_with: ['nan', 'mean', 'median', ...]
#             mask: ['True', 'False']
