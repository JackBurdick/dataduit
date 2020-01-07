import tensorflow as tf


def _return_dtype(dtype_str):
    # TODO: automate this
    if dtype_str == "string":
        return tf.string
    elif dtype_str == "int64":
        return tf.int64
    else:
        raise NotImplementedError("dtype {dtype_str} not currently supported")


def _return_feature_type(feat_str, tf_dtype):
    # TODO: automate this
    if feat_str.lower() == "FixedLenFeature".lower():
        return tf.io.FixedLenFeature([], tf_dtype)
    elif feat_str.lower() == "VarLenFeature".lower():
        return tf.io.VarLenFeature(tf_dtype)


def return_parse_feature(parse_config):

    # datatype
    try:
        dtype_in_str = parse_config["in"]["dtype"]
    except KeyError:
        raise KeyError(f"no in datatype described by {parse_config['in']}")
    tf_dtype = _return_dtype(dtype_in_str)

    try:
        type_str = parse_config["in"]["type"]
    except KeyError:
        raise KeyError(f"no type described by {parse_config['in']}")
    parse_feature = _return_feature_type(type_str, tf_dtype)

    return parse_feature

