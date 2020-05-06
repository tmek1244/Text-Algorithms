import numpy as np


def edit_distance(x, y):
    edit_table = np.empty((len(x)+1, len(y)+1))

    for i in range(len(x) + 1):
        edit_table[i, 0] = i
    for j in range(len(y) + 1):
        edit_table[0, j] = j

    for i in range(len(x)):
        for j in range(len(y)):
            edit_table[i+1][j+1] = min(edit_table[i][j+1] + 1,
                                       edit_table[i+1][j] + 1,
                                       edit_table[i][j] + (x[i] != y[j]))
    print(edit_table)
    return edit_table
