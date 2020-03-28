class TrieTree:
    def __init__(self):
        self.root = TrieNode('*')

    def add_word(self, word):
        self.root.add_word(word)

    def find_word(self, word):
        self.root.find_word(word)


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = []

    def add_word(self, word):
        if not word:
            return
        for child in self.children:
            if word[0] == child.char:
                child.add_word(word[1:])
                break
        else:
            self.children.append(TrieNode(word[0]))
            self.children[-1].add_word(word[1:])

    def find_word(self, word):
        if not word:
            return True

        for child in self.children:
            if word[0] == child.char:
                return child.find_word(word[1:])
        return False
