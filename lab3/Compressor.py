import os
import time

from bitarray import bitarray


from lab3.DynamicHuffman import dynamic_huffman
from lab3.StaticHuffman import static_huffman


def print_timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print("Time for ", func.__name__, ": ", time.perf_counter() - start)
        return result

    return inner


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
        encoded_text = padded_info + encoded_text + extra_padding * '0'
        return encoded_text

    @print_timer
    def compress(self, file):
        with open(file, "r") as input_file:
            text = input_file.read()

        self.huffman_code = self.function_to_compress(text)
        self.reversed_huffman_code = {v: k for k, v in self.huffman_code.items()}

        encoded_text = ''.join([self.huffman_code[letter] for letter in text])
        encoded_text = self.pad_encoded_text(encoded_text)

        with open("compressed_input.txt", "wb") as output_file:
            bitarray(encoded_text).tofile(output_file)

    # --------------------------------- DECOMPRESS -------------------------
    @staticmethod
    def remove_pad(encoded_text):
        padded_info = encoded_text[:8]
        padding_length = int(padded_info, 2)
        return encoded_text[8:-padding_length]

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
    # file_to_compress = input("Give file name from data_for_tests: ")
    for file in ["1kB.txt", "10kB.txt", "100kB.txt", "1MB.txt"]:
        for method in [dynamic_huffman, static_huffman]:
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
