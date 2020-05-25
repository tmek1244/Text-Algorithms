from lab5.pattern_searching import search_patterns
import lab5.image_functions as img_fun


image_source = 'haystack.png'


def get_text(source):
    with open(source, 'r') as file:
        text = file.read().splitlines()
        return text


def align_text(text):
    max_line_length = len(max(text, key=len))
    aligned_text = []

    for line in text:
        aligned_text.append(list(line.ljust(max_line_length, '#')))
    return aligned_text


def get_and_prepare_text(source):
    return align_text(get_text(source))


def get_all_letters(text):
    chars = set()
    for line in text:
        for char in line:
            chars.add(char)
    return chars


def task2():
    text = get_and_prepare_text('haystack.txt')

    chars = get_all_letters(text)
    total = 0

    for letter in chars:
        count = search_patterns(text, [letter + letter], False)
        if count and letter != '#':
            print("Letter ", letter, ":", count)
            total += count
    print("Total: ", total)


def task3():
    text = get_and_prepare_text('haystack.txt')

    count = search_patterns(text, ['tt', 'hh'], print_output=True)
    print("Pattern 'th' total:", count)
    print("-----------------------------")
    count = search_patterns(text, ['tt', '  ', 'hh'], print_output=True)
    print("Pattern 't h' total:", count)


def search_letter_in_image(image, print_output=False):
    return lambda x: search_patterns(image, img_fun.get_patterns_columns(x, image),
                                     print_output=print_output)


def task4():
    image = img_fun.get_and_prepare_image(image_source)
    img_fun.get_letters_image(image_source)
    function = search_letter_in_image(image)
    print('Number of x: ', function(img_fun.x_coords))
    print('Number of e: ', function(img_fun.e_coords))
    print('Number of n: ', function(img_fun.n_coords))
    print('Number of t: ', function(img_fun.t_coords))


def task5():
    image = img_fun.get_and_prepare_image(image_source)
    img_fun.get_pattern_image(image_source)
    print('Number of pattern: ', search_letter_in_image(image, True)(img_fun.pattern_coords))


def check_time(text, row, col):
    row_pattern = row * 'a'
    pattern = [row_pattern for _ in range(col)]
    print("Row number:", row, ", Column number:", col)
    search_patterns(text, pattern, print_time=True)
    print()


def task6():
    text = get_and_prepare_text('haystack.txt')
    check_time(text, 100, 100)
    check_time(text, 100, 1000)
    check_time(text, 100, 10000)
    check_time(text, 100, 100000)


def divide_and_search(pieces, text, pattern):
    length = len(text)
    total_build_time = 0
    total_search_time = 0
    print("----------------------------------")
    print("Pieces:", pieces)
    for i in range(pieces):
        begin = int(i * length/pieces)
        end = min(int((i + 1) * length/pieces), length)
        _, build_time, search_time = search_patterns(text[begin:end], pattern, return_time=True)
        total_build_time += build_time
        total_search_time += search_time
    print("\nTotal build time:", total_build_time)
    print("Total search time:", total_search_time)


def task7():
    pattern = '''Consider the problem of a reader of the French dictionary " G r a n d Larousse,"
who wants all entries related to the n a m e "Marie-Curie-Sklodowska." This is
a n example of a p a t t e r n matching problem, or string matching. In this case,
the n a m e "Marie-Curie-Sklodowska" is the p a t t e r n . Generally we m a y want to
find a string called a pattern of length m inside a text of length n, where n is
greater t h a n m. T h e p a t t e r n can be described in a more complex way to denote
a set of strings and not just a single word. In many cases n is very large. In
genetics the p a t t e r n can correspond to a gene t h a t can be very long; in image'''
    text = get_and_prepare_text('haystack.txt')
    divide_and_search(1, text, pattern)
    divide_and_search(2, text, pattern)
    divide_and_search(4, text, pattern)
    divide_and_search(8, text, pattern)


def main():
    # task2()
    task3()
    # task4()
    # task5()
    # task6()
    # task7()


if __name__ == '__main__':
    main()
