import time
from lab2.SuffixTree import Node

from lab2.TrieTree import TrieTree


def print_timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print("Time for ", func.__name__, ": ", time.perf_counter() - start)
        return result

    return inner


@print_timer
def create_trie_tree(text, tree: TrieTree):
    for i in range(len(text)):
        tree.add_word(text[i:])


def mcCreight(text):
    root = Node("*")
    node = Node(text)
    root.children.append(node)
    node.parent = root
    root.parent = root
    last_head = root
    head = root
    leaf = node
    # root.print_children()
    for i in range(1, len(text)):
        suffix = text[i:]

        p = last_head.label
        q = leaf.label
        label = ""
        print(suffix, ", p:", p, ", q:", q)
        if last_head == root:
            q = q[1:]
            head, label = root.slow_find(q)
        else:
            u = last_head.parent
            print(u.label)

            if u == root:
                # print("p:", p)
                p = p[1:]
                head, label = root.fast_find(p)
            else:
                head, label = u.link.fast_find(p)
            # head, label = head.slow_find(q)
            last_head.link = head
        if suffix[head.get_summary_length():]:
            leaf = Node(suffix[head.get_summary_length():])
            # print("new leaf:", leaf.label)
            leaf.parent = head
            head.children.append(leaf)
        root.print_children()
        last_head = head
        print("-------------", i, "------------------")
    return root


@print_timer
def mcCreight_slow_version(text):
    root = Node("*")
    node = Node(text)
    root.children.append(node)
    node.parent = root
    root.parent = root
    last_head = root
    head = root
    leaf = node
    # root.print_children()
    for i in range(1, len(text)):
        suffix = text[i:]

        # p = last_head.label
        # q = leaf.label
        label = ""
        # print(suffix, ", p:", p, ", q:", q)
        head, label = root.slow_find(suffix)
        if suffix[head.get_summary_length():]:
            leaf = Node(suffix[head.get_summary_length():])
            # print("new leaf:", leaf.label)
            leaf.parent = head
            head.children.append(leaf)
        # root.print_children()
        last_head = head
        # print("-------------", i, "------------------")
    return root


def check(root: Node, text):
    for i in range(len(text)):
        for j in range(i, len(text)):
            if not root.is_there(text[i:j]):
                print(root.is_there(text[i:j]), text[i:j])


def main():
    tree = TrieTree()
    # text = input("Give text: ")
    text = "asdasdadadadadadsadaduasgduyasgdyaugsdahsgdahgdajhashgdjadadasd$"
    create_trie_tree(text, tree)
    root = mcCreight_slow_version(text)
    # root.print_children()
    # print(root.is_there("dsd"))
    # check(root, text)


if __name__ == "__main__":
    main()
