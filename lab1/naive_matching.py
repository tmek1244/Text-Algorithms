def naive_string_matching(text, pattern):
    result = []
    for s in range(0, len(text) - len(pattern) + 1):
        if pattern == text[s:s + len(pattern)]:
            result.append(s)
    return result
