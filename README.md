# dataduit
raw data --> analysis ready data

This is a placeholder project for converting _x_ to 'analysis ready data'. Where _x_ may be parquet files, numpy arrays, pandas dataframe, etc.. and 'analysis ready data' will be either file type (tensorflow records) or a tf.data.Dataset object.

## Proposed/Intended Use

some_data_config.yaml (or a ''' string in python)
```yaml
input:
    type: ['file', 'directory', 'dataframe', 'numpy']
    path: <xxxx>

dataset_out: # true if present
    shuffle:
        buffer_size: <_n_>
    prefetch: <_n_>
    preprocess:
        # same `pipeline functionality as below`

    # ...

store_output: # true if present
    type: ['records', <others?>]
    num_records_per_file: <_n_>

features:
    feat_a:
        identifier:
            key: <xxxx>
        datatype:
            in: <xxxx>
            out: <xxxx>
        shape:
            in: <xxxx>
            out: <xxxx>
            other:
                variable:
                    max_len: <_n_> #(if known)
                    min_len: <_n_> #(if known)
        preprocessing:
            pipeline: 
                a: 
                    function: [normalize, standardize, <xxxx>, <custom_function>]
                b: 
                    function: [normalize, standardize, <xxxx>, <custom_function>]
                    # in: a # inferred 
                c: 
                    function: [normalize, standardize, <xxxx>, <custom_function>]
                    options:
                        function_args: [a]
                b: 
                    function: [normalize, standardize, <xxxx>, <custom_function>]
                        function_args: {input_a: a, input_b: c}
                        config_values: 
                            from_config: 
                                path: <xxxx>
                                identifier: # if obtaining from file
                            from_value: 
                                value: {input_a: 1, input_b: 3}

        missing:
            skip: ['True', 'False']
            log:
                location: "<_path_>"
            fill_with: ['nan', 'mean', 'median', ...]
            mask: ['True', 'False']

    feat_b:
        identifier:
            key: <xxxx>
        datatype:
            in: <xxxx>
            out: <xxxx>
        shape:
            in: <xxxx>
            out: <xxxx>
        preprocessing:
            function: <xxxx>
            standard: [normalize, standardize, ...]
        missing:
            fill_with: ['nan', 'mean', 'median', ...]
            mask: ['True', 'False']
    feat_c:
        # ...
    feat_d:
        # ...
    feat_e:
        # ...
            
out_features:
    out_feat_a:
        concat: [feat_a, feat_b]
    out_feat_b:
        stack: [feat_c, feat_d]
        axis: <_n_>
    features: {feature_a: out_feat_a, # can support combination of above features, or straight above features
               feature_b: out_feat_b,
               feature_c: feat_e}
    

labels: # (optional, unsupervised?)
    label_a:
        identifier:
            key: <xxxx>
        datatype:
            in: <xxxx>
            out: <xxxx>
        shape:
            in: <xxxx>
            out: <xxxx>
        preprocessing:
            function: <xxxx>
            standard: [normalize, standardize, ...]

# label_order: # single identifier is inferred
#     [label_a]

# this is used if all data currently exists in one directory
# will support an arbitrary number of splits
splits:
    train:
        percent: 65 # could be 'percent' or 'number'
    validation: 
        percent: 15
    leader:
        percent: 10
    test:
        percent: 10

```
```python
import dataduit as dd
import yeahml as yml

config = dd.parse_config('some_path.yaml')

# write to storage
out_info = dd.from_config(config)

# create dataset from raw data (additional caching is still possible)
out_ds = dd.from_config(config)

# or from pre created
out_ds = dd.from_storage(config)

# unpack
# this tuple could be variable length
train_ds = out_ds["train"]
val_ds = out_ds["val"]
test_ds = out_ds["test"]

################################################
# Do something with the data...
# ... like:

## build+train
model = yml.build_model('<some_config>')

yml.train_model(model, '<some_config>')
# OR
yml.train_model(model, dataset=out_ds)


## ... iterate+tune model as needed
# yml.eval_model('') # on "leader_board" set


## evaluate model
yml.eval_model('')


## serve model
yml.serve_model('')

```

## Note:
- I'm still unsure whether preprocessing like normalization/standardization belong here. My initial though is ... no. I think rather that belongs in the input pipeline and the data should be saved in it's raw state -- however, maybe there are cases where if you know the dataset isn't changing and training time is important it would make sense to save the data out in preprocessed form.
- Everything should stay in tensorflow, preferably graph mode (in case we want to build a function and use that for preprocessing for serving)
- TFX integration?