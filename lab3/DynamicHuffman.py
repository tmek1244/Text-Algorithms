import time

from lab3.Node import Node


def print_timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print("Time for ", func.__name__, ": ", time.perf_counter() - start)
        return result

    return inner


def dynamic_huffman(text):
    root = Node(count=0, letter="#")
    nodes = {"#": root}

    # print("----------------------------")
    for letter in text:
        # print("Next letter: ", letter)
        if letter in nodes:
            node = nodes[letter]
            node.increment()
        else:
            updated_node = nodes["#"]
            new_node = Node(letter=letter, parent=updated_node)
            new_hash_node = Node(count=0, letter="#", parent=updated_node)
            del nodes["#"]
            updated_node.count = 0
            updated_node.left = new_hash_node
            updated_node.right = new_node
            nodes["#"] = new_hash_node
            nodes[letter] = new_node
            updated_node.letter = None
            updated_node.increment()

        # root.print_tree()
        # print("----------------------------")
    return root.create_code(), root.tree_to_string()


if __name__ == '__main__':
    test_text = "bookkeeper"
    code = dynamic_huffman(test_text)
    print(code)
