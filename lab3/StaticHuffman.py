from lab3.Node import Node


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

    return internal_nodes[0].create_code()
