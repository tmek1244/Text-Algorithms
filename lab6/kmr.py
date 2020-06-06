import math
import time


def print_timer(func):
    def inner(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print("Time for ", func.__name__, ": ", time.perf_counter() - start)
        return result

    return inner


class pattern_dictionary:
    def __init__(self, text):
        self.text = text

    @print_timer
    def create_dictionary(self):
        names, _ = self.kmr()
        dictionary = {}

        for k, patterns in names.items():
            dictionary[k] = {}
            for index, pattern in enumerate(patterns[:len(self.text)]):
                if pattern in dictionary[k]:
                    dictionary[k][pattern].append(index)
                else:
                    dictionary[k][pattern] = [index]

        final_dictionary = {}
        for k, patterns in dictionary.items():
            final_dictionary[k] = {}
            for pattern, positions in patterns.items():
                final_dictionary[k][self.text[positions[0]:positions[0]+k]] = positions
        return final_dictionary

    @staticmethod
    def sort_rename(sequence):
        last_entry = None
        index = 0
        position_to_index = [None] * len(sequence)
        first_entry = {}

        for entry in sorted([(e, i) for i, e in enumerate(sequence)]):
            if last_entry and last_entry[0] != entry[0]:
                index += 1
                first_entry[index] = entry[1]

            position_to_index[entry[1]] = index
            if last_entry is None:
                first_entry[0] = entry[1]
            last_entry = entry
        return position_to_index, first_entry

    def kmr(self):
        factor = math.floor(math.log2(len(self.text)))
        max_length = 2 ** factor
        padding_length = 2 ** (factor + 1) - 1
        text = self.text
        text += "z" * padding_length

        position_to_index, first_entry = self.sort_rename(list(text))
        names = {1: position_to_index}
        entries = {1: first_entry}

        for i in range(1, factor):
            power = 2 ** (i - 1)
            new_sequence = []
            for j in range(len(self.text)):
                if j + power < len(names[power]):
                    new_sequence.append((names[power][j], names[power][j + power]))
            position_to_index, first_entry = self.sort_rename(new_sequence)
            names[power * 2] = position_to_index
            entries[power * 2] = first_entry

        return names, entries
