import re
from typing import OrderedDict

'''
two tables, one for history one for words
ngram table = dict of dict
history: dist of occurence count

type:
    0 = start
    1 = end
    2 = word
'''


class Gram:
    type = 0
    text = -1

    def __init__(self, _type, _text):
        self.type = _type

        if _type == 0:
            return

        if _text in gramDict:
            self.text = list(gramDict.keys()).index(_text)
        else:
            gramDict[_text] = _text
            self.text = list(gramDict.keys()).index(_text)


gramDict = OrderedDict()

text = ""


def main():
    # load text
    file = open("test.txt")
    text = str(file.read())

    print(text)

    words = re.findall(r'\b\w+\b|[\.\!\?\,]', text)
    numWords = len(words)
    gramSize = 1

    if numWords < gramSize:
        return

    grams = []
    startGram = Gram(0, '')
    grams.append(startGram)

    for i, word in enumerate(words):

        if word[0].isalnum():
            gram = Gram(2, word)
            grams.append(gram)

        else:
            gram = Gram(1, word)
            grams.append(gram)

            if i < numWords - 1 and word != ',':
                startGram = Gram(0, '')
                grams.append(startGram)

    string = ""
    for i, gram in enumerate(grams):
        if gram.type == 1:
            string += list(gramDict.keys())[gram.text]
        elif gram.type == 2:
            if i != 0:
                string += ' '
            string += list(gramDict.keys())[gram.text]
        else:
            string += '<start>'

    print(string)


if __name__ == "__main__":
    main()
