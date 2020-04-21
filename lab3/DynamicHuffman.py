from lab3.Node import Node


def dynamic_huffman_tree(text):
    root = Node(count=0, letter="#")
    nodes = {"#": root}

    for letter in text:
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

    return root


if __name__ == '__main__':
    test_text = "bookkeeper"
    tree_root = dynamic_huffman_tree(test_text)
    print(tree_root.create_code(), tree_root.tree_to_string())
