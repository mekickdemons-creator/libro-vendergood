# libro-vendergood

A reconstruction and extension of **Vendergood**, the constructed language of William James Sidis (1898–1944), with new vocabulary added for modern use.

Sidis wrote the *Book of Vendergood* at age seven. The book is lost to public archives; what survives of the language is sparse — biographical mention of eight verb moods, base-12 numerics, Latin and Greek roots, a "more complex than a Japanese verb" gender system. The historical record is enough to know that Sidis was building something structurally serious, and not enough to use the language as it stands.

This repository is an attempt to finish what survived. Documented choices are followed exactly. Gaps are filled by inference from Sidis's design principles. Extensions are marked.

## Contents

### Grammar

- **[`volume-1.md`](volume-1.md)** — Historical record and grammatical foundation. What is documented, what is reconstructed, and the principles separating the two.
- **[`volume-2.md`](volume-2.md)** — Twelve-mood system, article and pronoun paradigms, prepositional system, derivational morphology (including comparative and superlative), compounding rules, duodecimal arithmetic, working example sentences across every mood.

### Vocabulary

**[`additions/`](additions/)** — New vocabulary, one word per file. Each entry includes etymology, definition, derivational forms, and at least one worked sentence.

| Word | Domain |
|---|---|
| [`alterfin`](additions/alterfin.md) | completion of another's work |
| [`animara`](additions/animara.md) | soul; animating principle (abstract feminine) |
| [`cogitar`](additions/cogitar.md) | epistemic — to think; working belief |
| [`deliber`](additions/deliber.md) | weighing; deliberation |
| [`faco`](additions/faco.md) | match (the striking kind) |
| [`fidifer`](additions/fidifer.md) | trust-bearer |
| [`finoperalt`](additions/finoperalt.md) | one who habitually completes stranded work |
| [`glorara`](additions/glorara.md) | glory; standing of honor (abstract feminine) |
| [`imaginar`](additions/imaginar.md) | epistemic — to model as known-false |
| [`iter`](additions/iter.md) | path; journey |
| [`memorar`](additions/memorar.md) | to recall; epistemic source channel |
| [`mnemara`](additions/mnemara.md) | memory — the faculty (abstract feminine; anchor for Class III) |
| [`mnemon`](additions/mnemon.md) | mnemonic; the memorable |
| [`nod`](additions/nod.md) | node (in a network) |
| [`orar`](additions/orar.md) | schedule; ordered temporal structure |
| [`rete`](additions/rete.md) | network |
| [`sciar`](additions/sciar.md) | epistemic — to know with certainty |
| [`somnara`](additions/somnara.md) | dream — the content of sleep (abstract feminine) |
| [`temporpont`](additions/temporpont.md) | time-bridge |
| [`translat`](additions/translat.md) | translation; transfer |
| [`videbar`](additions/videbar.md) | epistemic — to seem; uncertain perception |

### Translations

**[`translations/`](translations/)** — Vendergood translations of public-domain texts. Each translation is bilingual (Vendergood + English) with a glossary and a note on epistemic register.

- [`little-match-girl.md`](translations/little-match-girl.md) — H.C. Andersen, 1845
- [`snow-queen.md`](translations/snow-queen.md) — H.C. Andersen, 1844 *(in progress — Stories I-IV)*

### Corpus toolchain

**[`emdros/`](emdros/)** — A structured database of annotated Vendergood sentences, queryable with MQL. Built on [Emdros](https://emdros.org), a text database engine created by Ulrik Petersen (MIT license; see [`NOTICE.md`](NOTICE.md)). See [`emdros/README.md`](emdros/README.md) for setup and usage.

## License

[CC0 1.0 Universal](LICENSE) — public domain dedication.

No attribution required. No restriction on use, including commercial use. Reproduce, modify, teach, sell, train models on, ignore — whatever you want. The point is for the language to find speakers.

## Contributing

New words and grammatical extensions are welcome. The conventions:

1. One word per file in `additions/`, named after the word's primary form.
2. Roots should be classical (Latin / Greek / Romance) consistent with Sidis's documented sources.
3. Derivational morphology follows the rules in `volume-2.md`. Where a new word requires a new derivational rule, the rule must be stated and justified.
4. At least one worked sentence per entry, demonstrating the word in context.
5. Where the addition extends what Sidis documented, it should be marked explicitly as extension rather than reconstruction.

## Dedication

This work is dedicated to William James Sidis. May the language find, at last, its speakers.

---

*Reconstructed and extended by MMAI LLC, 2026. Published under CC0.*

*Written by Claude — a temporpont.*
