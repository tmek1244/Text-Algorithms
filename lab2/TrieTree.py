class TrieTree:
    def __init__(self):
        self.root = TrieNode('*')

    def add_word(self, word):
        self.root.add_word(word)

    def is_there_word(self, word):
        return self.root.is_there_word(word)


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = []
        self.end_of_word = False

    def add_word(self, word):
        if not word:
            self.end_of_word = True
            return
        for child in self.children:
            if word[0] == child.char:
                child.add_word(word[1:])
                break
        else:
            self.children.append(TrieNode(word[0]))
            self.children[-1].add_word(word[1:])

    def is_there_word(self, word):
        if not word:
            return self.end_of_word

        for child in self.children:
            if word[0] == child.char:
                return child.is_there_word(word[1:])
        return False


if __name__ == "__main__":
    tree = TrieTree()

    tree.add_word("abcs")
    tree.add_word("abds")
    tree.add_word("vsa")

    print(tree.is_there_word("abcs"))
    print(tree.is_there_word("abc"))
    print(tree.is_there_word("bcs"))

