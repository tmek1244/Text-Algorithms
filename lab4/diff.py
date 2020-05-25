from lab4.LCS import lcs, file_to_tokens


def delta3(a, b):
    return 0 if a == b or a[0] == b[0] == '\n' else 2


def diff(input_path, output_path):
    tokens1 = file_to_tokens(input_path)
    tokens2 = file_to_tokens(output_path)
    _, words_in_lcs = lcs(tokens1, tokens2, delta3)
    line_begin1, line_begin2 = 0, 0
    token1_index, token2_index = 0, 0
    lcs_ind, line_number = 0, 0
    is_difference = False
    differences = []

    def check_difference(token):
        nonlocal is_difference
        if delta3(token, words_in_lcs[lcs_ind]) != 0:
            differences.append(token)
            is_difference = True
            return True
        return False

    while token1_index < len(tokens1) and token2_index < len(tokens2):
        if check_difference(tokens1[token1_index]):
            token1_index += 1
        elif check_difference(tokens2[token2_index]):
            token2_index += 1
        else:
            if words_in_lcs[lcs_ind][0] == '\n':
                if is_difference:
                    print("Line", line_number + 1)
                    print("<", ' '.join(tokens1[line_begin1:token1_index]))
                    print(">", ' '.join(tokens2[line_begin2:token2_index]))
                    print("Words not in LCS:", ', '.join(differences))
                is_difference = False
                differences = []
                line_number += words_in_lcs[lcs_ind].count('\n')
                line_begin1 = token1_index + 1
                line_begin2 = token2_index + 1
            lcs_ind += 1
            token1_index += 1
            token2_index += 1


def main():
    path1 = 'romeo-i-julia-700.txt'
    path2 = 'romeo-i-julia-3%.txt'
    diff(path1, path2)


if __name__ == '__main__':
    main()
