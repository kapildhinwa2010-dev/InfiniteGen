# InfiniteGen - Endless seeded matrix generation from a compact latent recipe
# Part of the Kapildhinwa2010-dev Toolkit.

"""Endless deterministic matrix streams from one seeded recipe.

Lineage: DNA_DYNIMO generators. This repo owns the INFINITE mode: an
endless generator of independent low-rank matrices from a single seed,
plus take() to bound it. Chunked, safe, parallel and streaming modes
live in the sibling repos.

HONEST LIMITATION: successive matrices are independent draws, NOT
orthogonal - overlap between any two is O(1/sqrt(rows*cols)) but
non-zero, and each draw costs a full rows x cols materialization.
"""

from __future__ import annotations

import math

import numpy as np

__all__ = ["GenRecipe", "generate", "generate_infinite", "take"]


class GenRecipe:
    """A seeded low-rank recipe: rows x cols output from rank x (rows+cols) latents."""

    def __init__(self, rows: int, cols: int, rank: int = 8, seed: int = 0) -> None:
        if rows < 1 or cols < 1:
            raise ValueError("rows and cols must be >= 1")
        if rank < 1:
            raise ValueError("rank must be >= 1")
        self.rows = rows
        self.cols = cols
        self.rank = min(rank, min(rows, cols))
        self.seed = seed

    def _latent(self, seed_offset: int) -> np.ndarray:
        rng = np.random.default_rng(self.seed + seed_offset)
        left = rng.standard_normal((self.rows, self.rank))
        right = rng.standard_normal((self.rank, self.cols))
        return (left @ right) / math.sqrt(self.rank)


def generate(recipe: GenRecipe) -> np.ndarray:
    """The canonical matrix of the recipe (seed + 0)."""
    return recipe._latent(0)

def generate_infinite(recipe: GenRecipe):
    """Yield an endless stream of independent matrices from the recipe."""
    counter = 0
    while True:
        yield recipe._latent(counter)
        counter += 1


def take(recipe: GenRecipe, count: int) -> list:
    """The first ``count`` matrices of the infinite stream."""
    if count < 1:
        raise ValueError("count must be >= 1")
    return [recipe._latent(i) for i in range(int(count))]