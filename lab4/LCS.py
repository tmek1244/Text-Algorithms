from spacy.tokenizer import Tokenizer
from spacy.lang.pl import Polish
import random

from lab4.EditDistance import edit_distance


def delta2(x, y):
    return 2*(x != y)


def lcs(x, y, delta=delta2):
    table = edit_distance(x, y, delta)
    distance = table[-1][-1]
    common = []
    k, m = len(x), len(y)
    while k >= 0 and m >= 0 and not (k == 0 == m):
        if delta(x[k - 1], y[m - 1]) == 0:
            common.append(x[k - 1] if len(x[k - 1]) <= len(y[m - 1]) else y[m - 1])
            k -= 1
            m -= 1
        elif k - 1 >= 0 and m - 1 >= 0:
            if table[k - 1][m] < table[k][m - 1]:
                k -= 1
            else:
                m -= 1
        elif k - 1 >= 0:
            k -= 1
        elif m - 1 >= 0:
            m -= 1

    return (len(x) + len(y) - distance) // 2, list(reversed(common))


def file_to_tokens(path):
    tokenizer = Tokenizer(Polish().vocab)
    with open(path, 'r') as file:
        text = file.read()
        tokens = tokenizer(text)
    # print(dir(list(tokens)))
    return list(map(str, tokens))


def tokens_to_file(path, tokens):
    for i in range(len(tokens)):
        if '\n' not in tokens[i]:
            tokens[i] = tokens[i] + ' '
    with open(path, 'w') as file:
        file.write(''.join(tokens))


def remove_random_tokens(tokens, amount):
    for i in range(amount):
        tokens.pop(random.randint(0, len(tokens) - 1))


def create_smaller_version(input_path, output_path, amount):
    tokens = file_to_tokens(input_path)
    remove_random_tokens(tokens, int(amount * len(tokens)))
    tokens_to_file(output_path, tokens)


def main():
    path = 'romeo-i-julia-700.txt'
    smaller_version = 'romeo-i-julia-3%.txt'

    # create_smaller_version(path, smaller_version, 0.03)
    tokens1 = file_to_tokens(path)
    tokens2 = file_to_tokens(smaller_version)
    print(lcs(tokens1, tokens2))
    print(len(tokens1), len(tokens2))


if __name__ == '__main__':
    main()
