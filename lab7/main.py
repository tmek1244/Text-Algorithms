import re

from lab7.state import create_finite_automaton


def check(regex, string):
    automaton = create_finite_automaton(regex)

    for i in range(len(string)):
        for j in range(i, len(string)):
            re_find = True if re.fullmatch(regex, string[i:j]) else False
            print(automaton.check_string(string[i:j]))
            if re_find != automaton.check_string(string[i:j]):
                print(string[i:j])


def main():
    regex = '(a+b)*[\\d]*'
    string = 'abaab435'
    automaton = create_finite_automaton(regex)
    # print(automaton.out['$'].out['a'].out['a'].out['$'].out['b'].out['$'])
    print(automaton.check_string(string))
    # check(regex, string)


if __name__ == '__main__':
    main()
