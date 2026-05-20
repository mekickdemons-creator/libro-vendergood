#!/usr/bin/env python3
"""
load_corpus.py — generate MQL to load the Vendergood corpus into Emdros.

Usage:
    python tools/load_corpus.py > generated/load.mql
    mql -b 3 generated/load.mql

Reads corpus/sentences.jsonl and emits MQL CREATE OBJECT statements for
Word and Sentence object types. Monads are assigned sequentially: each Word
is one monad; each Sentence spans the range of its words.

Run against the schema in schema/vendergood.mql (must already be applied).
"""

import json
import sys
from pathlib import Path

CORPUS_PATH = Path(__file__).parent.parent / "corpus" / "sentences.jsonl"


def esc(value: str) -> str:
    """Escape a string for use in an MQL string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def generate_mql(sentences: list[dict]) -> str:
    lines: list[str] = ["USE DATABASE 'vendergood' ;", ""]

    monad = 1

    word_blocks: list[str] = []
    sentence_blocks: list[str] = []

    for sent in sentences:
        words = sent.get("words", [])
        if not words:
            continue

        sent_start = monad

        for word in words:
            m = monad
            word_blocks.append(
                f"CREATE OBJECT FROM MONADS={{{m}}} WITH OBJECT TYPE [Word]\n"
                f'  surface:="{esc(word.get("surface", ""))}"\n'
                f'  lemma:="{esc(word.get("lemma", ""))}"\n'
                f'  root_1:="{esc(word.get("root_1", ""))}"\n'
                f'  root_2:="{esc(word.get("root_2", ""))}"\n'
                f'  category:="{esc(word.get("category", ""))}"\n'
                f'  mood_suffix:="{esc(word.get("mood_suffix", ""))}"\n'
                f'  tense:="{esc(word.get("tense", "present"))}"\n'
                f'  case:="{esc(word.get("case", ""))}"\n'
                f'  number:="{esc(word.get("number", "sg"))}"\n'
                f'  animacy:="{esc(word.get("animacy", ""))}"\n'
                f'  article_stem:="{esc(word.get("article_stem", ""))}"\n'
                f'  source:="{esc(sent.get("source", ""))}"\n'
                f'  gloss:="{esc(word.get("gloss", ""))}"\n'
                f"GO"
            )
            monad += 1

        sent_end = monad - 1
        sentence_blocks.append(
            f"CREATE OBJECT FROM MONADS={{{sent_start}-{sent_end}}} WITH OBJECT TYPE [Sentence]\n"
            f'  source:="{esc(sent.get("source", ""))}"\n'
            f'  text:="{esc(sent.get("text", ""))}"\n'
            f'  translation:="{esc(sent.get("translation", ""))}"\n'
            f'  moods_demonstrated:="{esc(sent.get("moods_demonstrated", ""))}"\n'
            f"GO"
        )

    for block in word_blocks:
        lines.append(block)
        lines.append("")

    for block in sentence_blocks:
        lines.append(block)
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    if not CORPUS_PATH.exists():
        print(f"ERROR: corpus not found at {CORPUS_PATH}", file=sys.stderr)
        sys.exit(1)

    sentences: list[dict] = []
    with open(CORPUS_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                sentences.append(json.loads(line))

    print(generate_mql(sentences))


if __name__ == "__main__":
    main()
