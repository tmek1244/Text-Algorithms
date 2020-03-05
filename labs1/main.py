import time


from labs1.KMP_matching import kmp_string_matching, prefix_function
from labs1.fa_matchnig import fa_string_matching, transition_table
from labs1.naive_matching import naive_string_matching


def count_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    print("Time for ", func.__name__, ": ", time.perf_counter() - start)
    return result


if __name__ == '__main__':
    pattern = """połączeń paleniskowych w budynkach przed
                       oddaniem ich do użytku, wyszukiwanie przerw w
                       ścianach przewodów kominowych i
                       wentylacyjnych oraz sprawdzanie połączeń
                       paleniskowych w budynkach już użytkowanych.
                       Badanie przyczyn wadliwego działania
                       przewodów kominowych i kanałów."""
    # text = "aaaaaabaabcaaa"
    text = open("ustawa.txt").read().replace('\n', ' ')
    # text = open("wikipedia-tail-kruszwil.txt").read().replace('\n', ' ')

    count_time(prefix_function, pattern)
    count_time(transition_table, pattern)
    resultNaive = count_time(naive_string_matching, text, pattern)
    resultFa = count_time(fa_string_matching, text, transition_table(pattern))
    resultKMP = count_time(kmp_string_matching, text, pattern, prefix_function(pattern))

    print("Same output: ", resultFa == resultKMP == resultNaive)
    # if resultFa == resultKMP == resultNaive:
    #     print("Same output: ", len(resultFa))
    # else:
    #     print("Wrong output")
