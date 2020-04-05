class SuffixNode(object):
    id = 0

    def __init__(self, text):
        self.id = SuffixNode.id
        SuffixNode.id += 1
        self.children = {}
        self.parent = None
        self.suffix_link = None
        self.i_from = 0
        self.i_to = 0
        self.text = text

    @property
    def length(self):
        return self.i_to - self.i_from

    def add(self, i_from, i_to):
        if i_from == i_to:
            print("add\n")
            return self
        child = SuffixNode(self.text)
        child.i_from = i_from
        child.i_to = i_to
        child.parent = self
        # print("add:", i_from, i_to)
        self[self.text[i_from]] = child
        return child

    def split(self, i_split):
        i_from = self.i_from
        i_to = self.i_to
        # print("split: ", i_from, i_split, i_to)
        assert i_split > i_from
        # assert i_split < i_to
        if i_split == i_to:
            return

        child = SuffixNode(self.text)
        child.i_from = self.i_from
        child.i_to = i_split
        self.i_from = i_split
        child.parent = self.parent
        child.parent[child.text[i_from]] = child
        self.parent = child
        child[self.text[i_split]] = self

    def find(self, label):
        if len(label) <= self.length:
            return label == self.label[:len(label)]
        if label[:self.length] != self.label:
            return False
        label = label[self.length:]
        if label[0] in self.children:
            return self[label[0]].find(label)
        return False

    @property
    def label(self):
        return self.text[self.i_from: self.i_to]

    def __getitem__(self, ident):
        return self.children[ident]

    def __setitem__(self, ident, child):
        self.children[ident] = child

    def __str__(self, indent=0):
        return '%s%s | id: %s\n%s' % (
            indent * '  ',
            self.label, self.id,
            ''.join(
                child.__str__(indent + 1)
                for key, child in sorted(self.children.items())
            )
        )


def McCreight(text):
    def fast_scan(node, i_from, i_to):
        assert node is not None
        length = i_to - i_from
        assert length >= 0
        if length == 0:
            return node, node.i_from
        # print("fast_scan: ", node.label, node == root)
        node = node[text[i_from]]
        while length > node.length:
            i_from += node.length
            length -= node.length
            node = node[text[i_from]]
        return node, node.i_from + length

    def slow_scan(node, i_from, i_to):
        assert node is not None
        assert i_from <= i_to
        if i_from == i_to:
            return node, node
        delta = 0
        loop = True
        try:
            node = node[text[i_from]]
            while i_from < i_to and loop:
                if node.i_from + delta < node.i_to:
                    if text[i_from] == text[node.i_from + delta]:
                        delta += 1
                        i_from += 1
                    else:
                        break
                else:
                    delta = 0
                    node = node[text[i_from + delta]]
        except KeyError:
            pass
        if delta > 0:
            # print("label:", node.label)
            node.split(node.i_from + delta)
            node = node.parent
        leaf = node.add(i_from, i_to)
        return node, leaf

    text_len = len(text)
    root = SuffixNode(text)
    head = root
    leaf = root.add(0, text_len)
    for j in range(1, text_len):
        print("------------------", j, "------------------")
        # print("text:", text[j:])
        # print(root)
        if head == root:
            print("slow scan")
            # print(root)
            # print("=========================")
            head, leaf = slow_scan(root, leaf.i_from + 1, leaf.i_to)
            # print(root)
            # print("=========================")
            continue
        parent = head.parent
        if parent == root:
            print("fast scan")
            # print(root)
            # print("=========================")
            head_sl, i = fast_scan(parent, head.i_from + 1, head.i_to)
        else:
            print("fast scan with suffix link")
            head_sl, i = fast_scan(parent.suffix_link, head.i_from, head.i_to)
        if i < head_sl.i_to:
            # s(head) is in the middle of an edge
            # print("split pierwszy: ", head_sl)
            head_sl.split(i)
            head_sl = head_sl.parent
            new_head = head_sl
            leaf = new_head.add(leaf.i_from, leaf.i_to)
        else:
            # s(head) is a node
            new_head, leaf = slow_scan(head_sl, leaf.i_from, leaf.i_to)
        head.suffix_link = head_sl
        # print("new link: from", head.id, "to", head_sl.id)
        head = new_head
        # print(root)
        # print("=========================")

    return root


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    from lab2.main import check
    file = open('1997_714 (1).txt', 'r')
    text = file.read().replace('\n', ' ')
    print(len(text))
    text = text + "#"
    # text = "dasdaasdas$"
    # print(text)
    root = McCreight(text)
    # print(root)
    # print(root.find("as"))
    print("tree builded")
    something_wrong = False
    for i in range(0, len(text), 1000):
        for j in range(i + 1, len(text), 1000):
            if not root.find(text[i:j]):
                print(text[i:j])
                something_wrong = True
    if not something_wrong:
        print("all good")
    # file.close()
