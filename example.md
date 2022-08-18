# Example

```python
dataset = Dataset(
    main=Indxr("queries.jsonl", key_id="q_id"),
    others=[
        Indxr("users.jsonl", key_id="u_id"),
        Indxr("docs.jsonl", key_id="d_id"),
    ],
    callback=do_something,
)
```

```python
def do_something(query, others):
    users, docs = others

    pos_docs = docs.get(query["pos_doc_ids"])
    pos_docs = [doc["text"] for doc in pos_docs]

    neg_docs = docs.get(user["neg_doc_ids"])
    neg_docs = [doc["text"] for doc in neg_docs]

    user = users.get(query["user_id"])
    user_docs = docs.get(user["doc_ids"])
    user_docs = [doc["text"] for doc in user_docs]

    return query["text"], pos_docs, neg_docs, user_docs
```

## queries.jsonl
```json
{
    "q_id": "q1",                       # query id
    "text": "lorem ipsum",              # query text
    "user_id": "u1",                    # user id
    "pos_doc_ids": ["d1", "d2"],        # positive samples
    "neg_doc_ids": ["d3", "d4", "d5"],  # negative samples
}
```

## users.jsonl
```json
{
    "u_id": "u1",               # user id
    "doc_ids": ["d11", "d22"],  # user-related doc ids
}
```

## docs.jsonl
```json
{
    "d_id": "d1",                     # doc id
    "text": "Lorem ipsum dolor sit",  # doc content
}
```