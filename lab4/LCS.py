from lab4.EditDistance import edit_distance


def delta2(x, y):
    return 2*(x != y)


def lcs1(x, y):
    return (len(x) + len(y) - edit_distance(x, y, delta2))/2
