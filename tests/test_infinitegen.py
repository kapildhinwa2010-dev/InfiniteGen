import numpy as np
import pytest

from infinitegen import GenRecipe, generate, generate_infinite, take


def test_generate_shape():
    recipe = GenRecipe(rows=16, cols=32, rank=4, seed=0)
    assert generate(recipe).shape == (16, 32)


def test_generate_deterministic():
    recipe = GenRecipe(rows=8, cols=8, seed=3)
    assert np.array_equal(generate(recipe), generate(recipe))


def test_recipe_rejects_bad_args():
    with pytest.raises(ValueError):
        GenRecipe(rows=0, cols=8)
    with pytest.raises(ValueError):
        GenRecipe(rows=8, cols=8, rank=0)


def test_infinite_yields_distinct():
    recipe = GenRecipe(rows=4, cols=4, seed=1)
    stream = generate_infinite(recipe)
    first = next(stream)
    second = next(stream)
    third = next(stream)
    assert not np.array_equal(first, second)
    assert not np.array_equal(second, third)


def test_infinite_is_lazy():
    recipe = GenRecipe(rows=4, cols=4, seed=1)
    stream = generate_infinite(recipe)
    first = next(stream)
    assert first.shape == (4, 4)


# --- take (InfiniteGen-specific) ---


def test_take_returns_count_matrices():
    recipe = GenRecipe(rows=4, cols=4, seed=2)
    mats = take(recipe, 5)
    assert len(mats) == 5
    assert np.array_equal(mats[0], generate(recipe))


def test_take_matches_stream_prefix():
    recipe = GenRecipe(rows=4, cols=4, seed=2)
    stream = generate_infinite(recipe)
    from_stream = [next(stream) for _ in range(3)]
    taken = take(recipe, 3)
    assert all(np.array_equal(a, b) for a, b in zip(from_stream, taken))


def test_take_rejects_zero():
    with pytest.raises(ValueError):
        take(GenRecipe(rows=2, cols=2), 0)