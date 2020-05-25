import numpy as np


def delta1(a, b):
    return a != b


def edit_distance(input_text, output_text, delta=delta1):
    edit_table = np.empty((len(input_text) + 1, len(output_text) + 1))

    for i_in in range(len(input_text) + 1):
        edit_table[i_in, 0] = i_in
    for i_out in range(len(output_text) + 1):
        edit_table[0, i_out] = i_out

    for i_in in range(len(input_text)):
        for i_out in range(len(output_text)):
            edit_table[i_in + 1][i_out + 1] = \
                min(edit_table[i_in][i_out + 1] + 1,
                    edit_table[i_in + 1][i_out] + 1,
                    edit_table[i_in][i_out] + delta(input_text[i_in], output_text[i_out]))
    return edit_table


def visualization(input_text, output_text, edit_table=None):
    if not edit_table:
        edit_table = edit_distance(input_text, output_text)
    print("First word:", input_text, "Second word:", output_text, "Distance:", edit_table[-1][-1])
    i_out = 0
    i_in = 0
    counter = 0
    created_word = input_text
    while i_out != len(output_text) or i_in != len(input_text):
        before = created_word
        right = edit_table[i_in][i_out + 1] if i_out < len(output_text) else float('inf')
        diagonal = edit_table[i_in + 1][i_out + 1] \
            if i_in < len(input_text) and i_out < len(output_text) else float('inf')
        down = edit_table[i_in + 1][i_out] if i_in < len(input_text) else float('inf')
        min_step = min(right, diagonal, down)
        same_letter = False
        if min_step == diagonal:
            if edit_table[i_in][i_out] == edit_table[i_in+1][i_out+1]:
                print("Same letter", input_text[i_in])
                same_letter = True
            else:
                print("Changing letter:", input_text[i_in], "->", output_text[i_out])
                created_word = created_word[:i_in+counter] + output_text[i_out] + created_word[i_in+1+counter:]
            i_out += 1
            i_in += 1
        elif min_step == right:
            print("Adding letter", output_text[i_out])
            counter += 1
            created_word = created_word[:i_in] + output_text[i_out] + created_word[i_in:]
            i_out += 1
        elif min_step == down:
            print("Removing letter")
            created_word = created_word[:i_in+counter] + created_word[i_in+1+counter:]
            i_in += 1
            counter -= 1
        if not same_letter:
            print(before, '-->', created_word)
            print()
            print("before: ", before)
            print("current:", created_word)
            print("pattern:", output_text)
        print('--------------------------')


def main():
    # a = 'los'
    # b = 'kloc'

    # a = 'Łódź'
    # b = 'Lodz'

    a = 'kwintesencja'
    b = 'quintessence'

    # a = 'ATGAATCTTACCGCCTCG'
    # b = 'ATGAGGCTCTGGCCCCTG'

    visualization(a, b)


if __name__ == '__main__':
    main()
