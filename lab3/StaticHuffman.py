from lab3.Node import Node


def static_huffman_tree(text):
    letter_count = {}

    for letter in text:
        letter_count[letter] = 1 if letter not in letter_count \
            else letter_count[letter] + 1

    nodes = []
    for letter, count in sorted(letter_count.items(), key=lambda x: (x[1], x[0]), reverse=True):
        nodes.append(Node(count=count, letter=letter))
    internal_nodes = []
    leafs = sorted(nodes, key=lambda n: n.count)
    while len(leafs) + len(internal_nodes) > 1:
        head = []
        head += leafs[:min(len(leafs), 2)]
        head += internal_nodes[:min(len(internal_nodes), 2)]

        element_1, element_2 = sorted(head, key=lambda n: n.count)[:2]
        internal_nodes.append(Node(count=(element_1.count + element_2.count)
                                   , left=element_1, right=element_2))
        if len(leafs) > 0 and element_1 == leafs[0]:
            leafs = leafs[1:]
        else:
            internal_nodes = internal_nodes[1:]
        if len(leafs) > 0 and element_2 == leafs[0]:
            leafs = leafs[1:]
        else:
            internal_nodes = internal_nodes[1:]
    return internal_nodes[0]


def main():
    text_for_test = "bookkeeper"
    root = static_huffman_tree(text_for_test)
    print("dictionary: ", root.create_code())
    print("string: ", root.tree_to_string())


if __name__ == '__main__':
    main()
