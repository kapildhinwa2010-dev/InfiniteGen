# InfiniteGen

[![CI](https://github.com/kapildhinwa2010-dev/InfiniteGen/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/InfiniteGen/actions/workflows/ci.yml)
[![CI](https://github.com/kapildhinwa2010-dev/InfiniteGen/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/InfiniteGen/actions/workflows/codeql.yml)

Endless seeded matrix generation: an iterator of independent low-rank matrices from one recipe.

**Part of the [Kapildhinwa2010-dev Toolkit](https://github.com/kapildhinwa2010-dev/Kapildhinwa2010-dev).**

## What it does

InfiniteGen owns the INFINITE mode of the DNA_DYNIMO generator
family: generate_infinite() yields an endless stream of independent
low-rank matrices from a single seeded GenRecipe; take() bounds it;
generate() gives the canonical matrix. Chunked, safe, parallel and
streaming modes live in the sibling repos.

## Install

```bash
pip install -r requirements.txt
```

## Quick start

```python
from infinitegen import GenRecipe, generate, take

recipe = GenRecipe(rows=64, cols=128, rank=8, seed=0)
W = generate(recipe)
batch = take(recipe, 5)  # 5 independent matrices
```

## API

- GenRecipe(rows, cols, rank, seed)
- generate(recipe) - the canonical matrix (seed + 0)
- generate_infinite(recipe) - endless generator
- take(recipe, count) - first count matrices

## Honest results and limitations

- Successive matrices are independent draws, NOT orthogonal: overlap
  between any two is O(1/sqrt(rows*cols)) but non-zero.
- Each draw costs a full rows x cols materialization - nothing is
  lazily computed per element.
- Rank is clamped to min(rows, cols); the output is exactly low-rank.

## License

MIT - see [LICENSE](LICENSE).
