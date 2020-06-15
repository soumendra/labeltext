[![pypi labeltext version](https://img.shields.io/pypi/v/labeltext.svg)](https://pypi.python.org/pypi/labeltext)
[![Conda labeltext version](https://img.shields.io/conda/v/labeltext/labeltext.svg)](https://anaconda.org/labeltext/labeltext)
[![labeltext python compatibility](https://img.shields.io/pypi/pyversions/labeltext.svg)](https://pypi.python.org/pypi/labeltext)
[![labeltext license](https://img.shields.io/pypi/l/labeltext.svg)](https://pypi.python.org/pypi/labeltext)

[![latest release date](https://img.shields.io/github/release-date/soumendra/labeltext.svg)](https://pypi.python.org/pypi/labeltext)
[![latest release version](https://img.shields.io/github/release/soumendra/labeltext.svg)](https://pypi.python.org/pypi/labeltext)
[![issue count](https://img.shields.io/github/issues-raw/soumendra/labeltext.svg)](https://pypi.python.org/pypi/labeltext)
[![open pr count](https://img.shields.io/github/issues-pr-raw/soumendra/labeltext.svg)](https://pypi.python.org/pypi/labeltext)
[![last commit at](https://img.shields.io/github/last-commit/soumendra/labeltext.svg)](https://pypi.python.org/pypi/labeltext)
[![contributors count](https://img.shields.io/github/contributors/soumendra/labeltext.svg)](https://pypi.python.org/pypi/labeltext)

# Getting started

- Documentation: https://labeltext.readthedocs.io/en/latest/

## Workflow overview

After installing `labeltext`,

1. create a `TextAnnotation` object (or restore from earlier annotation session),
2. start annotating by calling the `.annotate()` method.

## Install `labeltext`

```python
pip install labeltext
```

## Create a `TextAnnotation` object

```python
task = TextAnnotation(
    records=["Albert Einstein", "Stephen King", "Marie Curie"],
    labels=["male", "female"],
    output="scientists.csv"
)
print(task)
```

- `records`: List of text records to be annotated
- `labels`: List of class labels (up to 16)
- `output`: The CSV file where annotations will be saved (default: `annotations.csv`)

It'll probably be more natural to read the records from a (csv) file somewhere.

```python
import pandas as pd
df = pd.read_csv("example.csv")

task = TextAnnotation(
    records=list(df.text.values), # `text` is a column in df
    labels=["male", "female"],
    output="scientists.csv"
)
print(task)
```

## Start annotating

```python
task.annotate(user_name="@dataBiryani", update_freq=2)
```

This function starts an interactive annotation session.

- `user_name` (optional): A project may have multiple annotators. If not provided, the user will be asked for a `user_name`
- `update_freq` (optional): New annotations are not immediately saved to disk. They are saved once every `update_freq` annotations (default 5), or if the user ends the annotation session, or if no records are left to annotate.

**Note**: The output of the annotation session will be written to a csv file that you can feed into your modeling pipeline. The current state of annotation will also be saved in a pickle file (with the same filename as the csv file, but with `.pkl` extension). You can use the `.pkl` file to continue annotation in future sessions.

## Continue from where you left off

```python
task = TextAnnotation()("annotations.pkl")
task.annotate(user_name="@dataBiryani")
```
