from lab4.LCS import lcs, file_to_tokens


def split_element(arr, index, pos):
    arr.insert(index + 1, arr[index][pos:])
    arr[index] = arr[index][:pos]


def delta3(a, b):
    return 0 if a == b or a[0] == b[0] == '\n' else 2


def diff(input_path, output_path):
    # delta = lambda a, b: 0 if a == b or a[:1] == b[:1] == '\n' else 2

    tokens1 = file_to_tokens(input_path)
    tokens2 = file_to_tokens(output_path)
    _, common_words = lcs(tokens1, tokens2, delta3)
    line_begin1, line_begin2 = 0, 0
    token1_index, token2_index = 0, 0
    lcs_ind, line_number = 0, 0
    is_difference = False
    first_shift = True
    differences = []
    print("------------------")

    def check_difference(token):
        # nonlocal lcs_ind
        # nonlocal differences
        # nonlocal common_words
        # print(tokens[act], is_difference, lcs_ind, act)
        nonlocal is_difference
        if delta3(token, common_words[lcs_ind]) != 0:
            differences.append(token)
            is_difference = True
            return True
        return False

    while token1_index < len(tokens1) and token2_index < len(tokens2):
        if check_difference(tokens1[token1_index]):
            token1_index += 1
        elif check_difference(tokens2[token2_index]):
            token2_index += 1
        # if delta3(tokens1[token1_index], common_words[lcs_ind]) != 0:
        #     if tokens1[token1_index] != '':
        #         differences.append(tokens1[token1_index])
        #     token1_index += 1
        #     is_difference = True
        #     print(tokens1[token1_index], is_difference, lcs_ind, token1_index)
        #
        #     print(token1_index)
        # elif delta3(tokens2[token2_index], common_words[lcs_ind]) != 0:
        #     if tokens2[token2_index] != '':
        #         differences.append(tokens2[token2_index])
        #     token2_index += 1
        #     is_difference = True
        else:
            if common_words[lcs_ind][0] == '\n':
                # if len(tokens1[token1_index]) != len(tokens2[token2_index]):
                #     # print("----------------------------------------------")
                #     if len(tokens1[token1_index]) > len(tokens2[token2_index]):
                #         split_element(tokens1, token1_index, len(tokens2[token2_index]))
                #         common_words.insert(lcs_ind + 1, tokens1[token1_index + 1])
                #         tokens1.insert(token1_index + 1, '')
                #     elif len(tokens1[token1_index]) < len(tokens2[token2_index]):
                #         split_element(tokens2, token2_index, len(tokens1[token1_index]))
                #         common_words.insert(lcs_ind + 1, tokens2[token2_index + 1])
                #         tokens2.insert(token2_index + 1, '')
                #
                #     if not first_shift:
                #         line_number += 1
                #     else:
                #         first_shift = False

                if is_difference:
                    print("Line", line_number + 1)
                    print("<", ' '.join(tokens1[line_begin1:token1_index]))
                    print(">", ' '.join(tokens2[line_begin2:token2_index]))
                    print("Words not in LCS:", ', '.join(differences))
                is_difference = False
                differences = []
                line_number += common_words[lcs_ind].count('\n')
                line_begin1 = token1_index + 1
                line_begin2 = token2_index + 1
            token1_index += 1
            token2_index += 1
            lcs_ind += 1


def main():
    path1 = 'romeo-i-julia-700.txt'
    path2 = 'romeo-i-julia-3%.txt'
    diff(path1, path2)


if __name__ == '__main__':
    main()
