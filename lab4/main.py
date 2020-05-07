from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from spacy.lang.pl import Polish


from lab4.EditDistance import edit_distance, delta1
from lab4.LCS import lcs1


if __name__ == '__main__':
    # print(edit_distance('ATGAATCTTACCGCCTCG', 'ATGAGGCTCTGGCCCCTG', delta1))
    # print(lcs1('cbabac', 'abcabba'))
    npl = Polish()
    tokenizer = Tokenizer(npl.vocab)

    tokens = tokenizer("lab4/romeo-i-julia-700.txt")
    print(tokens)
