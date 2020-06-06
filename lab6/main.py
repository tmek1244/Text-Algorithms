import math
import sys
import time

from lab6.kmr import pattern_dictionary
from lab6.suffix_tree import SuffixTree
from lab6.KMP_matching import kmp_string_matching

files = ["romeo-i-julia-700.txt", "zad6"]


def is_power_of_2(pattern):
    return math.log2(len(pattern)) == math.floor(math.log2(len(pattern)))


def divide_pattern(pattern):
    new_length = 2**(math.floor(math.log2(len(pattern))))
    return pattern[:new_length], pattern[-new_length:]


def find_pattern(dictionary, pattern):
    if is_power_of_2(pattern):
        return find_power_2_pattern(dictionary, pattern)

    first_part, second_part = divide_pattern(pattern)
    first_part_occurrence = find_power_2_pattern(dictionary, first_part)
    second_part_occurrence = find_power_2_pattern(dictionary, second_part)

    # print(first_part_occurrence, second_part_occurrence)
    distance = len(pattern) - len(second_part)

    if first_part_occurrence and second_part_occurrence:
        return [x for x in first_part_occurrence if x+distance in second_part_occurrence]
    return []


def find_power_2_pattern(dictionary, pattern):
    if is_power_of_2(pattern):
        if len(pattern) in dictionary:
            if pattern in dictionary[len(pattern)]:
                return dictionary[len(pattern)][pattern]
    return []


def file_size(file_name):
    import os
    info = os.stat(file_name)
    return info.st_size


def task2():
    print("TASK 2")
    text = "abbabbaaaba"
    pattern1 = "bba"
    pattern2 = "aaaaa"
    pattern3 = "abb"
    dictionary = pattern_dictionary(text).create_dictionary()
    print(dictionary)
    print("Text:", text)
    print("Pattern:", pattern1, "Positions:", find_pattern(dictionary, pattern1))
    print("Pattern:", pattern2, "Positions:", find_pattern(dictionary, pattern2))
    print("Pattern:", pattern3, "Positions:", find_pattern(dictionary, pattern3))
    print(3*'\n')


def task3():
    print("TASK 3")
    for file in files:
        with open(file, "r") as f:
            # print(f.read())
            print("File:", file)
            string = f.read()
            time1 = time.perf_counter()
            SuffixTree(string)
            print("Suffix tree time: ", time.perf_counter() - time1)
            pattern_dictionary(string).create_dictionary()
    print(3*'\n')


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def calculate_size(dictionary):
    # print(str(directory))
    for k, v in dictionary.items():
        print(sys.getsizeof(k), sys.getsizeof(v))
        print(k, v)
    print(sys.getsizeof(dictionary))
    print(len(str(dictionary)))


def task4():
    print("TASK 4")
    for file in files:
        with open(file, "r") as f:
            size_of_file = file_size(file)
            print("File:", file)
            print("File size:", size_of_file)
            dictionary = pattern_dictionary(f.read()).create_dictionary()
            # dictionary_size = calculate_size(dictionary)
            dictionary_size = get_size(dictionary)
            print("Dictionary size:", dictionary_size)
            print("Ratio:", dictionary_size/size_of_file)
            print("-------------------------")
    print(3*'\n')


def task5():
    print("TASK 5")
    text = open("romeo-i-julia-700.txt").read()
    dictionary = pattern_dictionary(text).create_dictionary()

    patterns = ['a', 'Romeo', 'Rzecz odbywa się przez większą część sztuki w Weronie, przez część piątego aktu w Mantui.']
    for pattern in patterns:
        print("Pattern: ", pattern)
        time1 = time.perf_counter()
        print("pattern number:", len(find_pattern(dictionary, pattern)))
        print("time for DBF:", time.perf_counter() - time1)

        time2 = time.perf_counter()
        print("pattern number:", len(kmp_string_matching(text, pattern)))
        print("time for KMP:", time.perf_counter() - time2)


def main():
    # task2()
    task3()
    # task4()
    # task5()


if __name__ == '__main__':
    main()
