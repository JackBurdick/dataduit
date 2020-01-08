import tensorflow as tf
import inspect
from dataduit.libraries.tensorflow.components.dtype import return_dtype


def _return_available_parse_ops():
    IGNORE_IO_FEAT_KEYS = ["tfrecordoptions", "tfrecordwriter"]
    IGNORE_ARGS = ["cls", "_cls"]

    feat_ops = {}
    available_parse_ops = tf.io.__dict__
    for opt_name, opt_func in available_parse_ops.items():
        if inspect.isclass(opt_func):
            if opt_name.lower() not in set(IGNORE_IO_FEAT_KEYS):
                feat_ops[opt_name.lower()] = {}
                feat_ops[opt_name.lower()]["function"] = opt_func
                new = opt_func.__new__
                args = None
                # if args exist
                if new:
                    try:
                        args = list(opt_func.__new__.__code__.co_varnames)
                        args = [a for a in args if a not in IGNORE_ARGS]
                    except KeyError:
                        args = None

                feat_ops[opt_name.lower()]["func_args"] = args

    return feat_ops


def return_configured_dtype(opt_dict):

    try:
        feat_op_str = opt_dict["type"]
    except KeyError:
        raise KeyError(f"no feature op type described by in:type: {parse_config['in']}")

    avail_ops = _return_available_parse_ops()

    try:
        # NOTE: this feels like the wrong place to add a .lower()
        feat_op_fn = avail_ops[feat_op_str.lower()]["function"]
        feat_op_args = avail_ops[feat_op_str.lower()]["func_args"]
    except KeyError:
        raise KeyError(
            f"feature op {feat_op_str} not available in options {avail_ops.keys()}"
        )

    cur_opts = None
    try:
        cur_opts = opt_dict["options"]
    except KeyError:
        pass

    if cur_opts:
        if not set(cur_opts.keys()).issubset(feat_op_args):
            raise ValueError(
                f"options {opt_dict['options'].keys()} not in {feat_op_args}"
            )
        out = feat_op_fn(**cur_opts)
    else:
        out = feat_op_fn()

    return out
