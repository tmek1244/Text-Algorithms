from bitarray import bitarray


def static_huffman(text):
    letter_count = {}

    for letter in text:
        letter_count[letter] = 1 if letter not in letter_count \
            else letter_count[letter] + 1

    letter_count = sorted(letter_count.items(), key=lambda x: (x[1], x[0]), reverse=True)

    huffman_code = {}

    code = "0"
    for key, _ in letter_count[:-1]:
        huffman_code[key] = code
        code = "1" + code
    huffman_code[letter_count[-1][0]] = code[1:-1] + '1'
    return huffman_code


class Compressor:
    def __init__(self, function_to_compress):
        self.function_to_compress = function_to_compress
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
        print("decompress")
        bits_array = bitarray()
        with open(file, "rb") as input_file:
            bits_array.fromfile(input_file)

        bits = self.convert_bitarray_to_string(bits_array)
        bits = self.remove_pad(bits)
        output_file = open("decompressed.txt", "w")

        print(bits)
        decoded_text = ""
        current_part = ""
        for bit in bits:
            current_part += bit
            if current_part in self.reversed_huffman_code:
                decoded_text += self.reversed_huffman_code[current_part]
                current_part = ""
        print(decoded_text)
        output_file.write(decoded_text)
        output_file.close()


if __name__ == '__main__':
    compressor = Compressor(static_huffman)
    compressor.compress("cos.txt")
    compressor.decompress("compressed.txt")
