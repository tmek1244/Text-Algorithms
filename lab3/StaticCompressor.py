from bitarray import bitarray


class Node:
    def __init__(self, weight, letter=None, left=None, right=None):
        self.letter = letter
        self. weight = weight
        self.left = left
        self.right = right

    def print_tree(self, indentation='', code=''):
        print(indentation, "letter:", self.letter, "weight:", self.weight, end=' ')
        if self.letter:
            print("code:", code)
        else:
            print()
        if self.left:
            self.left.print_tree(indentation + '>', code+'0')
        if self.right:
            self.right.print_tree(indentation + '>', code+'1')

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
    leafs = sorted(nodes, key=lambda n: n.weight)
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

        element_1, element_2 = sorted(head, key=lambda n: n.weight)[:2]
        internal_nodes.append(Node(element_1.weight + element_2.weight, left=element_1,
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


class StaticCompressor:
    def __init__(self):
        self.function_to_compress = static_huffman
        self.huffman_code = None
        self.reversed_huffman_code = None

    # --------------------------------- COMPRESS -------------------------
    @staticmethod
    def pad_encoded_text(encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        padded_info = "{0:08b}".format(extra_padding)
        print("padded info:", padded_info)
        encoded_text = padded_info + encoded_text + extra_padding * '0'
        return encoded_text

    def compress(self, file):
        with open(file, "r") as input_file:
            text = input_file.read()

        self.huffman_code = self.function_to_compress(text)
        self.reversed_huffman_code = {v: k for k, v in self.huffman_code.items()}

        encoded_text = ''.join([self.huffman_code[letter] for letter in text])
        encoded_text = self.pad_encoded_text(encoded_text)

        with open("compressed.txt", "wb") as output_file:
            bitarray(encoded_text).tofile(output_file)

    # --------------------------------- DECOMPRESS -------------------------
    @staticmethod
    def remove_pad(encoded_text):
        padded_info = encoded_text[:8]
        print("padded info:", padded_info)
        padding_length = int(padded_info, 2)
        return encoded_text[8:-padding_length]

    @staticmethod
    def convert_bitarray_to_string(bitarray_string):
        return ''.join([str(int(x)) for x in bitarray_string])

    def decompress(self, file):
        bits_array = bitarray()
        with open(file, "rb") as input_file:
            bits_array.fromfile(input_file)

        bits = self.convert_bitarray_to_string(bits_array)
        bits = self.remove_pad(bits)

        decoded_text = ""
        current_part = ""
        for bit in bits:
            current_part += bit
            if current_part in self.reversed_huffman_code:
                decoded_text += self.reversed_huffman_code[current_part]
                current_part = ""
        with open("decompressed.txt", "w") as output_file:
            output_file.write(decoded_text)


if __name__ == '__main__':
    compressor = StaticCompressor()
    # sample = "abracadabra"
    # root = static_huffman(sample)
    # root.print_tree()
    # print(root.create_code())
    compressor.compress("cos.txt")
    compressor.decompress("compressed.txt")
