from dataduit.dataset.io.read.location.local.read import read_local
from dataduit.dataset.io.read.location.memory.read import read_memory


def create_ds(config_dict):

    # TODO: this needs to be corrected
    if (
        config_dict["obtain"]["primary_location"] == "local"
        or config_dict["obtain"]["primary_location"] == "online"
    ):
        datasets = read_local(config_dict)
    # elif config_dict["location"] == "memory":
    #     train_ds, valid_ds, test_ds = read_memory(config_dict)
    return datasets

