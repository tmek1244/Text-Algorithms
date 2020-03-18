import re
import string
import collections


def fa_string_matching(text, delta, pattern=None):
    q = 0
    result = []

    if delta is None:
        delta = transition_table(pattern)

    for s in range(0, len(text)):
        q = delta[q][text[s]]
        if q == len(delta) - 1:
            result.append(s + 1 - q)
    return result


def transition_table(pattern):
    result = []
    for q in range(0, len(pattern) + 1):
        result.append(collections.defaultdict(int))
        for a in set(pattern):
            k = min(len(pattern) + 1, q + 2)
            while True:
                k = k - 1
                # if re.search(pattern[:k] + "$", pattern[:q] + a):
                if pattern[:k] == (pattern[:q] + a)[-k:]:
                    break
            result[q][a] = k
    return result
