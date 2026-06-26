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


def calculate_guess_scores(
    guesses: list[str],
    possible_solutions: set[str],
) -> list[list[int]] | None:
    if score_guesses is None:
        return None

    solution_words = list(possible_solutions)
    encoded_guesses = encode_words(guesses)
    encoded_solutions = encode_words(solution_words)

    return score_guesses(encoded_guesses, encoded_solutions)


def best_guess_fast(
    guesses: list[str],
    possible_solutions: set[str],
) -> tuple[str, tuple[int, float, bool]] | None:
    if score_guesses is None:
        return None

    solution_words = list(possible_solutions)
    encoded_guesses = encode_words(guesses)
    encoded_solutions = encode_words(solution_words)

    groups_by_guess = score_guesses(encoded_guesses, encoded_solutions)

    possible_lookup = possible_solutions
    best_word = guesses[0]
    first_groups = groups_by_guess[0]
    best_key = (
        len(first_groups),
        -float(np.std(first_groups)),
        int(best_word in possible_lookup),
    )

    for i, guess in enumerate(guesses[1:], start=1):
        groups = groups_by_guess[i]
        key = (
            len(groups),
            -float(np.std(groups)),
            int(guess in possible_lookup),
        )
        if key > best_key:
            best_word = guess
            best_key = key

    return best_word, best_key


def openmp_threads_hint() -> str:
    return os.environ.get("OMP_NUM_THREADS", "OpenMP default")
