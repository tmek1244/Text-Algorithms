class Node:
    def __init__(self, letter, count=1, parent=None, left=None, right=None):
        self.parent = parent
        self.letter = letter
        self.count = count
        self.left = left
        self.right = right

    def increment(self):
        self.count += 1
        right_sibling = self.get_right_sibling()
        if right_sibling and right_sibling.count < self.count:
            self.swap_with_sibling()

        if self.parent:
            self.parent.increment()

    def get_right_sibling(self):
        if not self.parent:
            return None
        return self.parent.right if self == self.parent.left else None

    def swap_with_sibling(self):
        if not self.parent:
            return
        self.parent.left, self.parent.right = self.parent.right, self.parent.left

    def print_tree(self, indentation=""):
        print(indentation, "letter:", self.letter, "count:", self.count)
        if self.left:
            self.left.print_tree(indentation + '>')
        if self.right:
            self.right.print_tree(indentation + '>')


def dynamic_huffman(text):
    root = Node("#", count=0)
    nodes = {"#": root}

    root.print_tree()
    print("----------------------------")
    for letter in text:
        if letter in nodes:
            node = nodes[letter]
            node.increment()
        else:
            updated_node = nodes["#"]
            new_node = Node(letter, parent=updated_node)
            new_hash_node = Node("#", count=0, parent=updated_node)
            del nodes["#"]
            updated_node.count = 1
            updated_node.left = new_hash_node
            updated_node.right = new_node
            nodes["#"] = new_hash_node
            nodes[letter] = new_node
            updated_node.letter = None
            updated_node.increment()

        root.print_tree()
        print("----------------------------")


if __name__ == '__main__':
    test_text = "abccce"
    dynamic_huffman(test_text)
