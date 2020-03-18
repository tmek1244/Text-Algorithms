import time


from lab1.KMP_matching import kmp_string_matching, prefix_function
from lab1.fa_matchnig import fa_string_matching, transition_table
from lab1.naive_matching import naive_string_matching


def count_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    print("Time for ", func.__name__, ": ", time.perf_counter() - start)
    return result


def compare():
    text_for_tests = open("ustawa.txt").read().replace('\n', ' ')
    pattern_for_tests = "paleniskowych w budynkach już u"
    result_naive = count_time(naive_string_matching, text_for_tests, pattern_for_tests)
    result_fa = count_time(fa_string_matching, text_for_tests, None, pattern_for_tests)
    result_KMP = count_time(kmp_string_matching, text_for_tests, pattern_for_tests)

    print("Same output: ", result_fa == result_KMP == result_naive)


def find_art():
    text_for_tests = open("ustawa.txt").read().replace('\n', ' ')
    pattern_for_tests = "art"
    result_naive = count_time(naive_string_matching, text_for_tests, pattern_for_tests)
    result_fa = count_time(fa_string_matching, text_for_tests, None, pattern_for_tests)
    result_KMP = count_time(kmp_string_matching, text_for_tests, pattern_for_tests)

    print("Same output: ", result_fa == result_KMP == result_naive)


def simple_test():
    text = "aaaaaabaabcaaa"
    pattern = "aab"
    print(count_time(fa_string_matching, text, None, pattern))


def find_kruszwil():
    text_for_tests = open("wikipedia-tail-kruszwil.txt").read().replace('\n', ' ')
    pattern_for_tests = "kruszwil"
    result_naive = count_time(naive_string_matching, text_for_tests, pattern_for_tests)
    count_time(transition_table, pattern_for_tests)
    result_fa = count_time(fa_string_matching, text_for_tests, transition_table(pattern_for_tests))
    count_time(prefix_function, pattern_for_tests)
    result_KMP = count_time(kmp_string_matching, text_for_tests, pattern_for_tests, prefix_function(pattern_for_tests))

    print("Same output: ", result_fa == result_KMP == result_naive)


def test_for_naive_matching():
    text_for_tests = open("wikipedia-tail-kruszwil.txt").read().replace('\n', '')
    pattern_for_tests = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    result_naive = count_time(naive_string_matching, text_for_tests, pattern_for_tests)
    result_fa = count_time(fa_string_matching, text_for_tests, transition_table(pattern_for_tests))
    result_KMP = count_time(kmp_string_matching, text_for_tests, pattern_for_tests, prefix_function(pattern_for_tests))

    print("Same output: ", result_fa == result_KMP == result_naive)


def test_for_preprocessing():
    text_for_tests = open("wikipedia-tail-kruszwil.txt").read().replace('\n', ' ')
    pattern_for_tests = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" \
                        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    count_time(transition_table, pattern_for_tests)
    count_time(prefix_function, pattern_for_tests)


if __name__ == '__main__':
    # compare()  # zadanie 2
    # find_art()  # zadanie 3 i 4
    # find_kruszwil()  # zadanie 5
    test_for_naive_matching()  # zadanie 6
    # test_for_preprocessing()  # zadnie 7
