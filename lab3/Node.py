class Node:
    def __init__(self, count=1, letter=None, parent=None, left=None, right=None):
        self.parent = parent
        self.letter = letter
        self.count = count
        self.left = left
        self.right = right

    def create_code(self, code='', huffman_code=None):
        if huffman_code is None:
            huffman_code = {}
        if self.letter:
            huffman_code[self.letter] = code
        if self.left:
            self.left.create_code(code+'0', huffman_code)
        if self.right:
            self.right.create_code(code+'1', huffman_code)
        return huffman_code

    def increment(self):
        self.count += 1
        if self.parent and self.parent.parent and self.parent.parent.right and self.parent.parent.left:
            parent_sibling = self.parent.parent.right if self.parent.parent.left == self.parent \
                else self.parent.parent.left
            if self.check_and_swap(parent_sibling):
                self.parent.increment()
                return
            if parent_sibling == self.parent.parent.right:
                if self.check_and_swap(parent_sibling.right):
                    self.parent.increment()
                    return
                if self.check_and_swap(parent_sibling.left):
                    self.parent.increment()
                    return

        right_sibling = self.get_right_sibling()
        if right_sibling and right_sibling.count < self.count:
            self.swap_with_sibling()
        if self.parent:
            self.parent.increment()

    def check_and_swap(self, node):
        if node and node.count < self.count:
            self.swap_with_other_node(node)
            return True
        return False

    def get_right_sibling(self):
        if not self.parent:
            return None
        return self.parent.right if self == self.parent.left else None

    def swap_with_sibling(self):
        if not self.parent:
            return
        self.parent.left, self.parent.right = self.parent.right, self.parent.left

    def swap_with_other_node(self, node):
        if self.parent.left == self:
            self.parent.left = node
        else:
            self.parent.right = node
        if node.parent.left == node:
            node.parent.left = self
        else:
            node.parent.right = self
        self.parent, node.parent = node.parent, self.parent

    def print_tree(self):
        queue = [(self, "")]
        while len(queue) > 0:
            next_node = queue[0]
            queue = queue[1:]
            node = next_node[0]
            if node.right:
                queue.append((node.right, next_node[1] + ">"))
            if node.left:
                queue.append((node.left, next_node[1] + ">"))
            print(next_node[1], next_node[0])

    def tree_to_string(self):
        queue = [self]
        result = ""

        while len(queue) > 0:
            next_node = queue[0]
            queue = queue[1:]
            cos = "1"
            if next_node.letter:
                tmp = next_node.letter
                cos = "0" + str(bin(ord(tmp)))[2:]
                if len(cos) < 8:
                    cos = (8 - len(cos)) * '0' + cos
            result += cos
            if next_node.right:
                queue.append(next_node.right)
            if next_node.left:
                queue.append(next_node.left)
        return result

    def __str__(self):
        return ''.join(["letter: ", str(self.letter), " count: ", str(self.count)])
