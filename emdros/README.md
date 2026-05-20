# Emdros corpus toolchain

A structured database of annotated Vendergood sentences, queryable with [MQL](https://emdros.org).

Emdros is a text database engine for annotated text, created by Ulrik Petersen (MIT license — see `../NOTICE.md`).

## Layout

| Path | Contents |
|---|---|
| `Makefile` | `make load` / `make reload` / `make test` / `make query` targets |
| `schema/vendergood.mql` | Object type definitions: Word, Sentence |
| `corpus/sentences.jsonl` | Annotated worked sentences (one per line) |
| `tools/load_corpus.py` | Generates MQL `CREATE OBJECT` statements from the corpus |
| `tools/query.py` | `SELECT` + `GET FEATURES` with tabular output |
| `tools/sample_queries.mql` | Example queries for first corpus run |
| `tools/tests/` | Loader smoke tests (no Emdros required) |

## Prerequisites

- Python 3.9+ (no third-party packages required for load/query; pytest for tests)
- Emdros 3.9.0+ with SQLite3 backend, `mql` on PATH

The Makefile expects `mql` at `~/.local/bin/mql` and a Python venv at `~/workspace/venv/`. Adjust the `PYTHON` and `MQL` variables at the top of `Makefile` for your setup.

## Usage

From this directory:

```sh
make load                                    # apply schema + ingest corpus
make reload                                  # drop database, reload from scratch
make test                                    # run loader smoke tests
make query CONSTRAINT='root_2 <> ""'         # find compound words
make query CONSTRAINT='mood_suffix = "alt"'  # find habitual-mood verbs
```

The database is written to `emdros/db/vendergood` (gitignored; regenerated from corpus).

## Schema notes

The schema represents compounds as flat Word features (`root_1`, `root_2`, `root_3`) rather than nested Compound objects. This is sufficient for queries like *"find words sharing root X"* and avoids the complexity of phrase-level compound structure. See `schema/vendergood.mql` header comments for rationale.
