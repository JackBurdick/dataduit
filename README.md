# dataduit
raw data --> analysis ready data

This is a placeholder project for converting _x_ to 'analysis ready data'. Where _x_ may be parquet files, numpy arrays, pandas dataframe, etc.. and 'analysis ready data' will be either file type (tensorflow records) or a tf.data.Dataset object.

## Intended Use

some_data_config.yaml (or a ''' string in python)
```yaml
input:
    type: ['file', 'directory', 'dataframe', 'numpy']
    path: <xxxx>

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
        preprocessing:
            function: <xxxx>
            standard: [normalize, standardize, ...]
        on_missing:
            fill_with: ['nan', 'mean', 'median', ...]
            mask: ['True', 'False']

    feat_a:
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
        on_missing:
            fill_with: ['nan', 'mean', 'median', ...]
            mask: ['True', 'False']
            
feature_order:
    [feat_a, feat_b]

labels: (optional, unsupervised?)
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

config = totfr.parse_config('some_path.yaml')
out_info = totfr.create_tfr(config)

################################################
# Do something with the data...
# ... like:

## build+train
model = yml.build_model('<some_config>')
yml.train_model(model, '<some_config>')

## ... iterate+tune model as needed
# yml.eval_model('') # on "leader_board" set


## evaluate model
yml.eval_model('')


## serve model
yml.serve_model('')

```

## Note:
I'm still unsure whether preprocessing like normalization/standardization belong here. My initial though is ... no. I think rather that belongs in the input pipeline and the data should be saved in it's raw state -- however, maybe there are cases where if you know the dataset isn't changing and training time is important it would make sense to save the data out in preprocessed form.