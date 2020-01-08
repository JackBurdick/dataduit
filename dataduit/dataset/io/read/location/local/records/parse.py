import tensorflow as tf

from dataduit.libraries.tensorflow.components.feature_ops import return_configured_dtype


def return_parse_feature(parse_config):

    # datatype
    try:
        opt_dict = parse_config["in"]
    except KeyError:
        raise KeyError(f"no parse op information :in {parse_config}")

    parse_feature = return_configured_dtype(opt_dict)

    return parse_feature

