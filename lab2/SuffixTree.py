class Node:
    def __init__(self, label):
        self.label = label
        self.children = []
        self.parent = None
        self.link = None

    def get_child_with_first_letter(self, letter):
        if not letter:
            return None
        for child in self.children:
            if child.label[0] == letter[0]:
                return child
        return None

    def get_longest_prefix(self, label):
        common_prefix = ""
        i = 0
        while i < len(label) and i < len(self.label):
            if self.label[i] == label[i]:
                common_prefix += label[i]
            else:
                break
            i += 1
        return common_prefix

    def break_path(self, label):
        child = self.get_child_with_first_letter(label[0])
        new_node = Node(child.get_longest_prefix(label))
        self.children.remove(child)
        self.children.append(new_node)
        new_node.parent = self
        new_node.children.append(child)
        child.parent = new_node
        child.label = child.label[len(new_node.label):]
        return new_node, label[len(new_node.label):]  # , new_child

    def fast_find(self, label):
        if not label:
            return self, ""
        child = self.get_child_with_first_letter(label[0])
        if not child:
            return self, ""
        if len(child.label) < len(label):
            return child.fast_find(label[len(child.label):])
        if len(child.label) == len(label):
            return child, ""
        return self.break_path(label)

    def slow_find(self, label):
        if not label:
            return self, label
        child = self.get_child_with_first_letter(label[0])
        if not child:
            return self, label
        for i in range(1, len(child.label)):
            if child.label[i] != label[i]:
                return self.break_path(label)
        return child.slow_find(label[len(child.label):])

    def print_children(self, marker=""):
        marker += ">"
        print(marker, self.label)
        for child in self.children:
            child.print_children(marker)

    def get_summary_length(self):
        if self.parent == self:
            return 0
        return len(self.label) + self.parent.get_summary_length()

    def is_there(self, text):
        if not text:
            return True
        child = self.get_child_with_first_letter(text[0])
        if not child:
            return False
        if len(text) <= len(child.label):
            return text == child.label[:len(text)]
        if text[:len(child.label)] != child.label:
            return False
        return child.is_there(text[len(child.label):])

