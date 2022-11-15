<!-- <div align="center">
  <img src="https://repository-images.githubusercontent.com/268892956/750228ec-f3f2-465d-9c17-420c688ba2bc">
</div> -->

<p align="center">
  <!-- Python -->
  <a href="https://www.python.org" alt="Python">
      <img src="https://badges.aleen42.com/src/python.svg" />
  </a>
  <!-- Version -->
  <a href="https://badge.fury.io/py/indxr"><img src="https://badge.fury.io/py/indxr.svg" alt="PyPI version" height="18"></a>
  <!-- Black -->
  <a href="https://github.com/psf/black" alt="Code style: black">
      <img src="https://img.shields.io/badge/code%20style-black-000000.svg" />
  </a>
  <!-- License -->
  <a href="https://lbesson.mit-license.org/"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
</p>


## ⚡️ Introduction

[indxr](https://github.com/AmenRa/indxr) is a Python utility for indexing long files that allows you to read specific lines dynamically, avoiding hogging your RAM.

[indxr](https://github.com/AmenRa/indxr) can be particularly useful for managing large datasets split among multiple files and loading data dynamically and with a low memory footprint.

For an overview, follow the [Usage](#-usage) section.

<!-- ## ✨ Features -->

## 🔌 Installation
```bash
pip install indxr
```

## 💡 Usage

- [txt](https://github.com/AmenRa/indxr#txt)
- [jsonl](https://github.com/AmenRa/indxr#jsonl)
- [csv / tsv](https://github.com/AmenRa/indxr#csv--tsv--custom)
- [callback](https://github.com/AmenRa/indxr#callback-works-with-every-file-type)
- [write / read](https://github.com/AmenRa/indxr#write--read-index)
- [PyTorch Dataset example](https://github.com/AmenRa/indxr#usage-example-with-pytorch-dataset)

### TXT
```python
from indxr import Indxr

index = Indxr("sample.txt")

index[0]
>>> # First line of sample.txt

index.get("0")
>>> # First line of sample.txt

index.mget(["2", "1"])
>>> # List containing the third and second lines of sample.txt
```


### JSONl

```python
from indxr import Indxr

index = Indxr("sample.jsonl", key_id="id")  # key_id="id" is by default

# Returns the JSON object at line 43 as Python Dictionary
# Reads only the 43th line
index[42]

# Returns the JSON object with id="id_123" as Python Dictionary,
# Reads only the line where the JSON object is located
index.get("id_123")

# Same as `get` but for multiple JSON objects
index.mget(["id_123", "id_321"])
```


### CSV / TSV / ...

```python
from indxr import Indxr

index = Indxr(
  "sample.csv",
  delimiter=",",    # Default value. Automatically switched to `\t` for `.tsv` files.
  fieldnames=None,  # Default value. List of fieldnames. Overrides header, if any.
  has_header=True,  # Default value. If `True`, treats first line as header.
  return_dict=True, # Default value. If `True`, returns Python Dictionary, string otherwise.
  key_id="id",      # Default value. Same as for JSONl. Ignored if return_dict is `False`.
)

# Returns line 43 as Python Dictionary
index[42]

# Returns the line with id="id_123" as Python Dictionary
index.get("id_123")

# Same as `get` but for multiple lines
index.mget(["id_123", "id_321"])
```

### Custom
```python
from indxr import Indxr

# The file must have multiple lines
index = Indxr("sample.something")

index[0]
>>> # First line of sample.something in bytes

index.get("0")
>>> # First line of sample.something in bytes

index.mget(["2", "1"])
>>> # List containing the third and second lines of sample.something in bytes
```

### Callback (works with every file-type)

```python
from indxr import Indxr

index = Indxr("sample.txt", callback=lambda x: x.split())

index.get("0")
>>> # First line of sample.txt split into a list
```


### Write / Read Index
```python
from indxr import Indxr

index = Indxr("sample.txt", callback=lambda x: x.split())

index.write(path)  # Write index to disk

# Read index from disk, callback must be re-defined
index = Indxr.read(path, callback=lambda x: x.split())
```


### Usage example with PyTorch Dataset

```python
import random

from indxr import Indxr
from torch.utils.data import DataLoader, Dataset

class CustomDataset(Dataset):
    def __init__(self):
      self.queries = Indxr("queries.jsonl")
      self.documents = Indxr("documents.jsonl")

    def __getitem__(self, index: int):
        # Get query ------------------------------------------------------------
        query = self.queries[index]

        # Sampling -------------------------------------------------------------
        pos_doc_id = random.choice(query["pos_doc_ids"])
        neg_doc_id = random.choice(query["neg_doc_ids"])

        # Get docs -------------------------------------------------------------
        pos_doc = self.documents.get(pos_doc_id)
        neg_doc = self.documents.get(neg_doc_id)

        # The outputs must be batched and transformed to
        # meaningful tensors using a DataLoader and
        # a custom collator function
        return query["text"], pos_doc["text"], neg_doc["text"]

    def __len__(self):
        return len(self.queries)


def collator_fn(batch):
    # Extract data -------------------------------------------------------------
    queries = [x[0] for x in batch]
    pos_docs = [x[1] for x in batch]
    neg_docs = [x[2] for x in batch]

    # Texts tokenization -------------------------------------------------------
    queries = tokenizer(queries)    # Returns PyTorch Tensor
    pos_docs = tokenizer(pos_docs)  # Returns PyTorch Tensor
    neg_docs = tokenizer(neg_docs)  # Returns PyTorch Tensor

    return queries, pos_docs, neg_docs


dataloader = DataLoader(
    dataset=CustomDataset(),
    collate_fn=collate_fn,
    batch_size=32,
    shuffle=True,
    num_workers=4,
)
```

Each line of `queries.jsonl` is as follows:
```json
{
  "q_id": "q321",
  "text": "lorem ipsum",
  "pos_doc_ids": ["d2789822", "d2558037", "d2594098"],
  "neg_doc_ids": ["d3931445", "d4652233", "d191393", "d3692918", "d3051731"]
}
```

Each line of `documents.jsonl` is as follows:
```json
{
  "doc_id": "d123",
  "text": "Lorem ipsum dolor sit amet, consectetuer adipiscing elit."
}
```


## 🎁 Feature Requests
Would you like to see other features implemented? Please, open a [feature request](https://github.com/AmenRa/indxr/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BFeature+Request%5D+title).


## 🤘 Want to contribute?
Would you like to contribute? Please, drop me an [e-mail](mailto:elias.bssn@gmail.com?subject=[GitHub]%20indxr).


## 📄 License
[indxr](https://github.com/AmenRa/indxr) is an open-sourced software licensed under the [MIT license](LICENSE).
