"""
Smoke tests for load_corpus.py.

Tests MQL generation without requiring Emdros to be installed.
Run: python -m pytest tools/tests/test_load.py -q
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from load_corpus import generate_mql, esc


def make_sentence(source: str, text: str, words: list[dict]) -> dict:
    return {
        "source": source,
        "text": text,
        "translation": "test translation",
        "moods_demonstrated": "at",
        "words": words,
    }


def test_esc_quotes():
    assert esc('"hello"') == '\\"hello\\"'


def test_esc_backslash():
    assert esc("a\\b") == "a\\\\b"


def test_single_sentence_word_count():
    words = [
        {"surface": "Avlo", "lemma": "avlo", "root_1": "av", "root_2": "",
         "category": "article", "gloss": "the"},
        {"surface": "iter", "lemma": "iter", "root_1": "iter", "root_2": "",
         "category": "noun_inanimate", "gloss": "route"},
    ]
    sent = make_sentence("iter", "Avlo iter.", words)
    mql = generate_mql([sent])

    # Two Word objects and one Sentence object should be emitted
    assert mql.count("WITH OBJECT TYPE [Word]") == 2
    assert mql.count("WITH OBJECT TYPE [Sentence]") == 1


def test_monads_sequential():
    words = [
        {"surface": "A", "lemma": "a", "root_1": "a", "root_2": "",
         "category": "article", "gloss": "a"},
        {"surface": "B", "lemma": "b", "root_1": "b", "root_2": "",
         "category": "noun_inanimate", "gloss": "b"},
        {"surface": "C", "lemma": "c", "root_1": "c", "root_2": "",
         "category": "verb", "gloss": "c"},
    ]
    sent = make_sentence("test", "A B C.", words)
    mql = generate_mql([sent])

    assert "FROM MONADS={1}" in mql
    assert "FROM MONADS={2}" in mql
    assert "FROM MONADS={3}" in mql
    assert "FROM MONADS={1-3}" in mql  # Sentence span


def test_sentence_span_across_two_sentences():
    word = {"surface": "W", "lemma": "w", "root_1": "w", "root_2": "",
            "category": "verb", "gloss": "w"}
    s1 = make_sentence("s1", "W.", [word])
    s2 = make_sentence("s2", "W.", [word])
    mql = generate_mql([s1, s2])

    # s1 spans monad 1, s2 spans monad 2
    assert "FROM MONADS={1-1}" in mql
    assert "FROM MONADS={2-2}" in mql


def test_source_field_in_word():
    word = {"surface": "temporpontalt", "lemma": "temporpontalt",
            "root_1": "pont", "root_2": "tempor",
            "category": "noun_animate", "gloss": "one who bridges time"}
    sent = make_sentence("temporpont", "temporpontalt.", [word])
    mql = generate_mql([sent])

    assert 'source:="temporpont"' in mql


def test_compound_roots():
    word = {"surface": "alterfin", "lemma": "alterfin",
            "root_1": "fin", "root_2": "alter",
            "category": "noun_inanimate", "gloss": "completion of another's work"}
    sent = make_sentence("alterfin", "alterfin.", [word])
    mql = generate_mql([sent])

    assert 'root_1:="fin"' in mql
    assert 'root_2:="alter"' in mql


def test_corpus_file_loads():
    corpus_path = Path(__file__).parent.parent.parent / "corpus" / "sentences.jsonl"
    assert corpus_path.exists(), f"Corpus not found: {corpus_path}"

    sentences = []
    with open(corpus_path) as f:
        for line in f:
            line = line.strip()
            if line:
                sentences.append(json.loads(line))

    assert len(sentences) >= 10, f"Expected at least 10 sentences, got {len(sentences)}"

    mql = generate_mql(sentences)
    word_count = mql.count("WITH OBJECT TYPE [Word]")
    sentence_count = mql.count("WITH OBJECT TYPE [Sentence]")

    assert sentence_count == len(sentences)
    assert word_count > sentence_count  # every sentence has at least one word
