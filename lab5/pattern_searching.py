from time import time
from collections import defaultdict


class Node:
    def __init__(self, index):
        self.goto = defaultdict()
        self.out = []
        self.fail = None
        self.index = index


def create_forest(patterns):
    root = Node(0)

    i = 1
    for path in patterns:
        node = root
        for symbol in path:
            node = node.goto.setdefault(symbol, Node(i))
            i += 1
        node.out.append(path)
    return root


def build_automaton(patterns):
    root = create_forest(patterns)
    queue = []
    for node in root.goto.values():
        queue.append(node)
        node.fail = root

    while len(queue) > 0:
        rnode = queue.pop(0)

        for key, unode in rnode.goto.items():
            queue.append(unode)
            fnode = rnode.fail
            while fnode is not None and key not in fnode.goto:
                fnode = fnode.fail
            unode.fail = fnode.goto[key] if fnode else root
            unode.out += unode.fail.out

    return root


def kmp_string_matching(text, pattern, pi=None):
    if pi is None:
        pi = prefix_function(pattern)
    result = []
    q = 0
    for i in range(0, len(text)):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]
        if pattern[q] == text[i]:
            q = q + 1
        if q == len(pattern):
            result.append(i + 1 - q)
            q = pi[q - 1]
    return result


def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k = k + 1
        pi.append(k)
    return pi


def search_patterns(text, patterns, print_output=False, print_time=False, return_time=False):
    time1 = time()
    automaton = build_automaton(patterns)

    patterns_pattern = []
    pattern_number = []
    current = 0
    for pattern in patterns:
        current += len(pattern)
        num = current
        for p, n in pattern_number:
            if p == pattern:
                num = n

        patterns_pattern.append(num)
        if num == current:
            pattern_number.append((pattern, num))

    states = [[0 for _ in range(len(text[0]))] for _ in range(len(text))]

    for j in range(len(text[0])):
        node = automaton
        for i in range(len(text)):
            while node is not None and not text[i][j] in node.goto:
                node = node.fail
            if node is None:
                node = automaton
            else:
                node = node.goto[text[i][j]]
                states[i][j] = node.index

    time2 = time()
    i = -1 * len(patterns[0]) + 1
    count = 0
    for row in states:
        S = kmp_string_matching(row, patterns_pattern)
        lenS = len(S)
        count += lenS
        if print_output:
            for j in S:
                print("Pattern found at:")
                print((i, j), " ... ", (i, j + len(patterns) - 1))
                print("...             ...")
                print((i + len(patterns[0]) - 1, j)
                      , " ... ", (i + len(patterns[0]) - 1, j + len(patterns) - 1))
        i += 1
    time3 = time()

    if print_time:
        print("Building time:", 1000 * (time2 - time1), "ms")
        print("Searching time:", 1000 * (time3 - time2), "ms")

    if return_time:
        return count, 1000 * (time2 - time1), 1000 * (time3 - time2)
    return count
