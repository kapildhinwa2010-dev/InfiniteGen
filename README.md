# InfiniteGen

InfiniteGen is a small Python library for producing dense, seeded low-rank matrices. A `GenRecipe` stores matrix dimensions, a requested rank, and a seed; the module can generate one matrix, iterate over a deterministic sequence, or collect a finite prefix of that sequence. The repository is versioned as `0.1.0` and currently consists of this module and a compact test suite; it does not claim production readiness.

## Implemented behavior

- `GenRecipe(rows, cols, rank=8, seed=0)` validates that dimensions and rank are at least 1. The effective rank is clamped to `min(rows, cols)`.
- `generate(recipe)` returns a NumPy array with shape `(rows, cols)`. It draws standard-normal factors using NumPy's `default_rng(seed)` and computes their product divided by the square root of the effective rank.
- `generate_infinite(recipe)` is a lazy generator. Each successive result uses the recipe seed plus an incrementing integer offset.
- `take(recipe, count)` returns a list containing the first `count` matrices from the same sequence; `count` must be at least 1. Its first item is the same matrix as `generate(recipe)`.

The stream is reproducible for the same recipe in a compatible NumPy environment. This is a deterministic, seed-offset pseudorandom sequence; the implementation does not establish formal statistical independence between its outputs.

## Requirements

- Python 3.9 or newer, as declared in `pyproject.toml`.
- NumPy 1.24 or newer.

## Install

From a clone of this repository, install the project and its declared runtime dependency with:

```bash
python -m pip install .
```

To install the dependencies used by the repository's tests as well:

```bash
python -m pip install -r requirements.txt
```

## Example

```python
from infinitegen import GenRecipe, generate, generate_infinite, take

recipe = GenRecipe(rows=64, cols=128, rank=8, seed=0)
first = generate(recipe)             # NumPy array, shape (64, 128)
next_two = take(recipe, 2)           # finite list; item 0 equals first
stream = generate_infinite(recipe)   # lazy, unbounded iterator
stream_first = next(stream)          # seed offset 0; same as first
stream_second = next(stream)         # seed offset 1
```

`generate_infinite` has no built-in stopping condition. Use a bounded consumer or `take` when only a finite number of matrices is needed. The repository does not provide a command-line interface.

## Tests and CI

On the reviewed repository commit (`312ba09fcd672aa1dcbc4dc98b0677995a95f2d9`), the local test command `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider` completed with **8 passed**. The CI workflow is configured to run `python -m pytest -q` on Python 3.10, 3.11, and 3.12, plus compilation and an import smoke test. This local result does not verify a remote GitHub Actions run or those other Python versions. A separate CodeQL workflow is configured; no CodeQL result is reported here.

## Limitations and scope

- Every yielded matrix is materialized as a dense `rows × cols` NumPy array; the generator is lazy between outputs, not within a matrix.
- The returned matrices are low-rank products with rank bounded by the requested effective rank; this is not an orthogonality or exact-rank guarantee.
- The API does not implement batching beyond `take`, chunked or per-element streaming, parallel generation, persistence/checkpointing, or statistical tests and benchmarks.
- There are no benchmark measurements in this repository, so no performance claims are made.

## License

The repository includes an MIT License, with the copyright notice `Copyright (c) 2026 Kapildhinwa2010-dev`. See [LICENSE](LICENSE) for the full terms.
