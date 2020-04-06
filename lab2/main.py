import time

from lab2.SuffixTree import Node
from lab2.TrieTree import TrieTree
from lab2.mcCreight import McCreight


def print_timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print("Time for ", func.__name__, ": ", time.perf_counter() - start)
        return result

    return inner


@print_timer
def create_trie_tree(text):
    tree = TrieTree()
    for i in range(len(text)):
        tree.add_word(text[i:])


@print_timer
def mcCreight_slow_version(text):
    root = Node("*")
    node = Node(text)
    root.children.append(node)
    node.parent = root
    root.parent = root
    for i in range(1, len(text)):
        suffix = text[i:]

        head, label = root.slow_find(suffix)
        if suffix[head.get_summary_length():]:
            leaf = Node(suffix[head.get_summary_length():])
            leaf.parent = head
            head.children.append(leaf)
    return root


def check(root: Node, text):
    for i in range(len(text)):
        for j in range(i, len(text)):
            if not root.is_there(text[i:j]):
                print(root.is_there(text[i:j]), text[i:j])


@print_timer
def mcCreight_fast_version(text):
    McCreight(text)


def get_text(which_text):
    if which_text == 1:
        return "bbb$"
    if which_text == 2:
        return "aabbabd"
    if which_text == 3:
        return "ababcd"
    if which_text == 4:
        return "abcbccd"
    if which_text == 5:
        file = open('randomWords.txt', 'r')
        text = file.read().replace('\n', ' ')
        # print(len(text))
        text = text + "#"
        return text


def main():
    text = get_text(int(input("which text: ")))
    create_trie_tree(text)
    mcCreight_slow_version(text)
    mcCreight_fast_version(text)

    # root.print_children()
    # print(root.is_there("dsd"))
    # check(root, text)


if __name__ == "__main__":
    main()
