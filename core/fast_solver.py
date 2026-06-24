from __future__ import annotations

import os
from functools import lru_cache

import numpy as np


try:
    from core.solver_accel import score_guesses
except ImportError:
    score_guesses = None


def is_accelerated() -> bool:
    return score_guesses is not None


@lru_cache(maxsize=None)
def encode_word(word: str) -> int:
    packed = 0
    for i, char in enumerate(word.lower()):
        packed |= (ord(char) - ord("a")) << (5 * i)
    return packed


def encode_words(words: list[str]) -> np.ndarray:
    return np.array([encode_word(word) for word in words], dtype=np.uint32)


def best_guess_fast(
    guesses: list[str],
    possible_solutions: set[str],
) -> tuple[str, tuple[int, float, bool]] | None:
    if score_guesses is None:
        return None

    solution_words = list(possible_solutions)
    encoded_guesses = encode_words(guesses)
    encoded_solutions = encode_words(solution_words)

    group_counts, stds = score_guesses(encoded_guesses, encoded_solutions)

    possible_lookup = possible_solutions
    best_word = guesses[0]
    best_key = (
        int(group_counts[0]),
        -float(stds[0]),
        int(best_word in possible_lookup),
    )

    for i, guess in enumerate(guesses[1:], start=1):
        key = (
            int(group_counts[i]),
            -float(stds[i]),
            int(guess in possible_lookup),
        )
        if key > best_key:
            best_word = guess
            best_key = key

    return best_word, best_key


def openmp_threads_hint() -> str:
    return os.environ.get("OMP_NUM_THREADS", "OpenMP default")
