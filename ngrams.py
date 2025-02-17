import re
import copy
import random
import sys
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
    text = ""

    def __init__(self, _type, _text):
        self.type = _type
        self.text = _text

        if _text in historyDict:
            historyDict[_text] += 1
        else:
            historyDict[_text] = 1


historyDict = OrderedDict()
ngramTable = OrderedDict()
ngramTable['<start>'] = OrderedDict()

numSentences = 1
gramSize = 1

files = []
text = ""


def getNextWord(grams):
    text = ""
    for gram in grams:
        text += gram

    total = 0

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


def containsEnding(sentence):
    for c in sentence:
        match c:
            case '.' | '!' | '?':
                return True

    return False


def splitGramArray(grams):
    listOfGrams = []
    currentGramList = []
    for gram in grams:
        currentGramList.append(gram)
        if gram.type == 1 and gram.text != ',':
            listOfGrams.append(copy.deepcopy(currentGramList))
            currentGramList = []

    return listOfGrams


def generateSentence():
    string = ""
    wordList = []
    for _ in range(gramSize):
        wordList.append("<start>")

    while True:
        nextWord = getNextWord(wordList)
        wordList.pop(0)
        wordList.append(nextWord)

        space = " "
        if string == "" or not nextWord[0].isalnum():
            space = ""

        string += space + nextWord

        if containsEnding(nextWord):
            break

    print(string)


def main():
    grams = []

    # load text
    for file in files:
        file = open(file)
        text = str(file.read())

        words = re.findall(r'\b[\w\']+\b|[\.\!\?\,]', text)
        numWords = len(words)

        # Get grams
        startGram = Gram(0, '<start>')

        for i in range(gramSize):
            grams.append(startGram)

        for i, word in enumerate(words):
            if word[0].isalnum():
                gram = Gram(2, word)
                grams.append(gram)

            else:
                gram = Gram(1, word)
                grams.append(gram)

                if i < numWords - 1 and word != ',':
                    for i in range(gramSize):
                        grams.append(startGram)

    # Build ngram table
    gramSentences = splitGramArray(grams)

    for sentence in gramSentences:
        for i, gram in enumerate(sentence):
            if i == 0:
                i = gramSize - 1
                continue

            texts = sentence[i - gramSize:i]
            text = ""
            for word in texts:
                text += word.text

            nextText = sentence[i].text

            if text in ngramTable:
                if nextText in ngramTable[text]:
                    ngramTable[text][nextText] += 1
                else:
                    ngramTable[text][nextText] = 1
            else:
                ngramTable[text] = OrderedDict()
                ngramTable[text][nextText] = 1

    for i in range(numSentences):
        generateSentence()
        if i < numSentences - 1:
            print("----")


if __name__ == "__main__":
    numSentences = int(sys.argv[1])
    gramSize = int(sys.argv[2])

    for i in range(len(sys.argv) - 3):
        files.append(sys.argv[3 + i])

    if files == []:
        exit()

    main()
