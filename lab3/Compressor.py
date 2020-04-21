import os
import time

from bitarray import bitarray


from lab3.DynamicHuffman import dynamic_huffman_tree
from lab3.Node import Node
from lab3.StaticHuffman import static_huffman_tree


def print_timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print("Time for ", func.__name__, ": ", time.perf_counter() - start)
        return result

    return inner


def string_tree_to_tree(string):
    queue = []
    while string:
        next_bit = string[0]
        string = string[1:]
        if next_bit == "1":
            queue.append(Node())
        else:
            letter = chr(int(string[:7], 2))
            string = string[7:]
            queue.append(Node(letter=letter))

    root = queue.pop(0)
    second_queue = [root]
    while second_queue:
        right_element = queue.pop(0)
        left_element = queue.pop(0)
        next_node = second_queue.pop(0)
        next_node.right = right_element
        next_node.left = left_element
        if right_element.letter is None:
            second_queue.append(right_element)
        if left_element.letter is None:
            second_queue.append(left_element)
    return root


class StaticCompressor:
    def __init__(self, function):
        self.function_to_compress = function
        self.huffman_code = None
        self.reversed_huffman_code = None

    # --------------------------------- COMPRESS -------------------------
    @staticmethod
    def pad_encoded_text(encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        padded_info = "{0:08b}".format(extra_padding)
        return padded_info + encoded_text + extra_padding * '0'

    @staticmethod
    def add_string_tree_info(string_tree):
        length_in_bits = "{0:0b}".format(len(string_tree))
        base = list("0000000000000000")
        for i in range(1, len(length_in_bits) + 1):
            base[-i] = length_in_bits[-i]
        base = ''.join(base)
        return base + string_tree

    @print_timer
    def compress(self, file):
        with open(file, "r") as input_file:
            text = input_file.read()

        root = self.function_to_compress(text)
        self.huffman_code = root.create_code()
        string_tree = root.tree_to_string()
        encoded_text = ''.join([self.huffman_code[letter] for letter in text])
        string_tree = self.add_string_tree_info(string_tree)
        encoded_text = self.pad_encoded_text(string_tree + encoded_text)

        with open("compressed_input.txt", "wb") as output_file:
            bitarray(encoded_text).tofile(output_file)

    # --------------------------------- DECOMPRESS -------------------------
    @staticmethod
    def remove_pad(encoded_text):
        padded_info = encoded_text[:8]
        padding_length = int(padded_info, 2)
        return encoded_text[8:-padding_length]

    def set_reversed_huffman_code(self, string):
        length = int(string[:16], 2)
        string = string[16:]
        string_tree = string[:length]
        self.reversed_huffman_code = \
            {v: k for k, v in string_tree_to_tree(string_tree).create_code().items()}
        return string[length:]

    @staticmethod
    def convert_bitarray_to_string(bitarray_string):
        return ''.join([str(int(x)) for x in bitarray_string])

    @print_timer
    def decompress(self, file):
        bits_array = bitarray()
        with open(file, "rb") as input_file:
            bits_array.fromfile(input_file)

        bits = self.convert_bitarray_to_string(bits_array)
        bits = self.remove_pad(bits)
        bits = self.set_reversed_huffman_code(bits)

        decoded_text = ""
        current_part = ""
        for bit in bits:
            current_part += bit
            if current_part in self.reversed_huffman_code:
                decoded_text += self.reversed_huffman_code[current_part]
                current_part = ""
        with open("output.txt", "w") as output_file:
            output_file.write(decoded_text)


def main():
    for file in ["1kB.txt", "10kB.txt", "100kB.txt", "1MB.txt"]:
        for method in [static_huffman_tree, dynamic_huffman_tree]:
            print("--------", file, "  ", method.__name__, "--------")
            file_to_compress = "data_for_tests/" + file
            compressor = StaticCompressor(method)
            compressor.compress(file_to_compress)
            compressor.decompress("compressed_input.txt")
            os.system("diff " + file_to_compress + " output.txt")
            print("compression rate:", 1 - os.path.getsize("compressed_input.txt")/os.path.getsize(file_to_compress))
            print()


if __name__ == '__main__':
    main()
