def kmp_string_matching(text, pattern, pi=None):
    # pi = prefix_function(pattern)4
    if pi is None:
        pi = prefix_function(pattern)
    result = []
    q = 0
    for i in range(0, len(text)):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q-1]
        if pattern[q] == text[i]:
            q = q + 1
        if q == len(pattern):
            result.append(i + 1 - q)
            # print("Przesunięcie {i + 1 - q} jest poprawne")
            q = pi[q-1]
    return result


def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k-1]
        if pattern[k] == pattern[q]:
            k = k + 1
        pi.append(k)
    return pi
