import re
import copy
import random
from typing import OrderedDict

'''
two tables, one for history one for words
ngram table = dict of dict
history: dict of occurence count

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

        if _text in historyDict:
            historyDict[_text] += 1
            self.text = list(historyDict.keys()).index(_text)
        else:
            historyDict[_text] = 1
            self.text = list(historyDict.keys()).index(_text)


historyDict = OrderedDict()
ngramTable = OrderedDict()
ngramTable['<start>'] = OrderedDict()

text = ""


def getText(i):
    return list(historyDict.keys())[i]


def getNextWord(text):
    total = 0
    commonText = ""

    keyList = copy.deepcopy(list(ngramTable[text].keys()))
    keyList.sort(key=lambda k: ngramTable[text][k], reverse=True)

    for key in keyList:
        total += ngramTable[text][key]

    choice = random.randint(0, total)
    for key in keyList:
        choice -= ngramTable[text][key]
        if choice <= 0:
            return key

    print("Couldn't find it")
    return keyList[-1]


def main():
    # load text
    file = open("test.txt")
    text = str(file.read())

    words = re.findall(r'\b[\w\']+\b|[\.\!\?\,]', text)
    numWords = len(words)
    gramSize = 1

    if numWords < gramSize:
        return

    # Get grams
    grams = []
    startGram = Gram(0, '<start>')
    grams.append(startGram)

    for i, word in enumerate(words):
        if word[0].isalnum():
            gram = Gram(2, word)
            grams.append(gram)

        else:
            gram = Gram(1, word)
            grams.append(gram)

            if i < numWords - 1 and word != ',':
                startGram = Gram(0, '<start>')
                grams.append(startGram)

    # Build ngram table
    for i, gram in enumerate(grams):
        if i == len(grams) - 1:
            break

        text = getText(grams[i].text)
        nextText = getText(grams[i+1].text)

        if text in ngramTable:
            if nextText in ngramTable[text]:
                ngramTable[text][nextText] += 1
            else:
                ngramTable[text][nextText] = 1
        else:
            ngramTable[text] = OrderedDict()
            ngramTable[text][nextText] = 1

    string = ""
    prev = "<start>"
    while True:
        prev = getNextWord(prev)

        space = " "
        if string == "" or not prev[0].isalnum():
            space = ""

        string += space + prev

        if (not prev[0].isalnum() and not prev[0] == ','):
            break

    print(string)


if __name__ == "__main__":
    main()
