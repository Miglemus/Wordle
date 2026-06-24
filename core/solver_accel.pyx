# cython: language_level=3

import numpy as np
cimport numpy as cnp
from cython.parallel cimport prange
from libc.math cimport sqrt
from libc.stdint cimport int32_t, uint32_t, uint16_t

<void>cnp.import_array()


cdef inline uint16_t evaluate_guess_c(uint32_t guess, uint32_t solution) noexcept nogil:
    cdef int g_chars[5]
    cdef int s_chars[5]
    cdef int s_counts[26]
    cdef int i
    cdef uint16_t result = 0

    for i in range(26):
        s_counts[i] = 0

    for i in range(5):
        g_chars[i] = (guess >> (5 * i)) & 0x1F
        s_chars[i] = (solution >> (5 * i)) & 0x1F
        s_counts[s_chars[i]] += 1

    for i in range(5):
        if g_chars[i] == s_chars[i]:
            result |= <uint16_t>(2 << (2 * i))
            s_counts[g_chars[i]] -= 1

    for i in range(5):
        if ((result >> (2 * i)) & 0x3) == 2:
            continue

        if s_counts[g_chars[i]] > 0:
            result |= <uint16_t>(1 << (2 * i))
            s_counts[g_chars[i]] -= 1

    return result


cdef inline void score_one_guess_c(
    uint32_t guess,
    cnp.uint32_t[::1] solutions,
    int32_t* out_group_count,
    double* out_std,
) noexcept nogil:
    cdef Py_ssize_t j
    cdef int pattern
    cdef int count
    cdef int group_count = 0
    cdef int num_solutions = solutions.shape[0]
    cdef double mean
    cdef double variance = 0.0
    cdef int counts[1024]

    for pattern in range(1024):
        counts[pattern] = 0

    for j in range(num_solutions):
        pattern = evaluate_guess_c(guess, solutions[j])
        counts[pattern] += 1

    for pattern in range(1024):
        if counts[pattern] > 0:
            group_count = group_count + 1

    out_group_count[0] = group_count

    if group_count == 0:
        out_std[0] = 0.0
        return

    mean = <double>num_solutions / group_count

    for pattern in range(1024):
        count = counts[pattern]
        if count > 0:
            variance += (count - mean) * (count - mean)

    out_std[0] = sqrt(variance / group_count)


cpdef score_guesses(cnp.uint32_t[::1] guesses, cnp.uint32_t[::1] solutions):
    cdef Py_ssize_t i
    cdef int num_guesses = guesses.shape[0]

    cdef cnp.ndarray[cnp.int32_t, ndim=1] group_counts = np.zeros(
        num_guesses, dtype=np.int32
    )
    cdef cnp.ndarray[cnp.float64_t, ndim=1] stds = np.zeros(
        num_guesses, dtype=np.float64
    )

    for i in prange(num_guesses, nogil=True, schedule="static"):
        score_one_guess_c(
            guesses[i],
            solutions,
            &group_counts[i],
            &stds[i],
        )

    return group_counts, stds
