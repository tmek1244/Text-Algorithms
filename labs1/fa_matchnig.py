import re
import string
import collections


def fa_string_matching(text, delta):
    q = 0
    result = []
    for s in range(0, len(text)):
        q = delta[q][text[s]]
        if q == len(delta) - 1:
            result.append(s + 1 - q)
    return result


def transition_table(pattern):
    result = []
    for q in range(0, len(pattern) + 1):
        result.append(collections.defaultdict(int))
        for a in string.ascii_letters:
            k = min(len(pattern) + 1, q + 2)
            while True:
                k = k - 1
                if pattern[:k] + "$" in pattern[:q] + a:
                    break
            result[q][a] = k
    return result
