import time

from lab3.Node import Node


def print_timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print("Time for ", func.__name__, ": ", time.perf_counter() - start)
        return result

    return inner


def string_tree_to_dictionary(string):
    queue = []
    while string:
        print(string)
        next_bit = string[0]
        string = string[1:]
        if next_bit == "1":
            queue.append(Node())
        else:
            letter = chr(int(string[:7], 2))
            string = string[7:]
            queue.append(Node(letter=letter))

    root = queue.pop(0)
    second_queue = [root]
    while second_queue:
        right_element = queue.pop(0)
        left_element = queue.pop(0)
        next_node = second_queue.pop(0)
        next_node.right = right_element
        next_node.left = left_element
        if right_element.letter is None:
            second_queue.append(right_element)
        if left_element.letter is None:
            second_queue.append(left_element)
    return root.create_code()


def static_huffman(text):
    letter_count = {}

    for letter in text:
        letter_count[letter] = 1 if letter not in letter_count \
            else letter_count[letter] + 1

    letter_count = sorted(letter_count.items(), key=lambda x: (x[1], x[0]), reverse=True)

    nodes = []
    for letter, weight in letter_count:
        nodes.append(Node(weight, letter=letter))
    internal_nodes = []
    leafs = sorted(nodes, key=lambda n: n.count)
    while len(leafs) + len(internal_nodes) > 1:
        head = []
        if len(leafs) >= 2:
            head += leafs[:2]
        elif len(leafs) == 1:
            head += leafs[:1]
        # head += leafs[:min(len(leafs), 2)]

        if len(internal_nodes) >= 2:
            head += internal_nodes[:2]
        elif len(internal_nodes) == 1:
            head += internal_nodes[:1]
        # head += internal_nodes[:min(len(internal_nodes), 2)]

        element_1, element_2 = sorted(head, key=lambda n: n.count)[:2]
        internal_nodes.append(Node(element_1.count + element_2.count, left=element_1,
                                   right=element_2))
        if len(leafs) > 0 and element_1 == leafs[0]:
            leafs = leafs[1:]
        else:
            internal_nodes = internal_nodes[1:]
        if len(leafs) > 0 and element_2 == leafs[0]:
            leafs = leafs[1:]
        else:
            internal_nodes = internal_nodes[1:]
    return internal_nodes[0].create_code(), internal_nodes[0].tree_to_string()


def main():
    text_for_test = "bookkeeper"
    dictionary, string = static_huffman(text_for_test)
    print("dictionary: ", dictionary)
    print("string: ", string)
    print(dictionary == string_tree_to_dictionary(string))


if __name__ == '__main__':
    main()
