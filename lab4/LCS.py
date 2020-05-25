from spacy.tokenizer import Tokenizer
from spacy.lang.pl import Polish
import random

from lab4.EditDistance import edit_distance


def delta2(x, y):
    return 2*(x != y)


def lcs(x, y, delta=delta2):
    table = edit_distance(x, y, delta)
    distance = table[-1][-1]
    words_in_lcs = []
    x_iter, y_iter = len(x) - 1, len(y) - 1
    while x_iter >= 0 and y_iter >= 0:
        if delta(x[x_iter], y[y_iter]) == 0:
            words_in_lcs.append(x[x_iter])
            x_iter -= 1
            y_iter -= 1
        elif x_iter - 1 > 0 and y_iter - 1 > 0:
            if table[x_iter + 1][y_iter] > table[x_iter][y_iter + 1]:
                x_iter -= 1
            else:
                y_iter -= 1
        elif x_iter - 1 > 0:
            x_iter -= 1
        elif y_iter - 1 > 0:
            y_iter -= 1

    return (len(x) + len(y) - distance) // 2, list(reversed(words_in_lcs))


def file_to_tokens(path):
    tokenizer = Tokenizer(Polish().vocab)
    with open(path, 'r') as file:
        text = file.read()
        tokens = tokenizer(text)
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
    print("LCS length:", lcs(tokens1, tokens2)[0])
    print(len(tokens1), len(tokens2))


if __name__ == '__main__':
    main()
