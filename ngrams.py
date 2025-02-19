'''
Zachariah Dellimore V00980652

This program works by first creating a list of all grams in the text files the
user provides and labelling each gram as either a start, end, or word gram. It
then generates a dictionary mapping n number of grams to the next predicted 
word.

The user uses this file like this:
    python ngram.py 5 3 text.txt text2.txt ...

The first number represents the number of sentences to be generated, the second
the number of ngrams. The user then adds the variable number of text documents
to be analyzed.

two tables, one for history one for words
ngram table = dict of dict
history: dict of occurence count

type:
    0 = start
    1 = end
    2 = word
'''

import re
import copy
import random
import sys
from typing import OrderedDict



# This class holds the data for each gram
class Gram:
    type = 0
    text = ""

    def __init__(self, _type, _text):
        self.type = _type
        self.text = _text

        # Update the number of occurances the word has
        if _text in historyDict:
            historyDict[_text] += 1
        else:
            historyDict[_text] = 1


historyDict = OrderedDict()
ngramTable = OrderedDict()
ngramTable['<start>'] = OrderedDict()

# Values that will be filled out by the user
numSentences = 1
gramSize = 1

files = []
text = ""


# This file takes in a list of grams and uses the ngramTable to pick the next
# word using the weights of how many times the word has been seen after the
# given grams
def getNextWord(grams):
    text = ""
    for gram in grams:
        text += gram

    total = 0

    # Sort the key list by appearance count
    keyList = copy.deepcopy(list(ngramTable[text].keys()))
    keyList.sort(key=lambda k: ngramTable[text][k], reverse=True)

    # Get the total number of appearances
    for key in keyList:
        total += ngramTable[text][key]

    choice = random.randint(0, total)
    for key in keyList:
        choice -= ngramTable[text][key]
        if choice <= 0:
            return key

    print("Couldn't find it")
    return keyList[-1]


# return true if the string has an ending punctuation mark
def containsEnding(sentence):
    for c in sentence:
        match c:
            case '.' | '!' | '?':
                return True

    return False


# Splits a list of grams into several lists of gram arrays split on the ending
# grams
def splitGramArray(grams):
    listOfGrams = []
    currentGramList = []
    for gram in grams:
        currentGramList.append(gram)
        if gram.type == 1 and gram.text != ',':
            listOfGrams.append(copy.deepcopy(currentGramList))
            currentGramList = []

    return listOfGrams


# Generates a sentence
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
    # list of all grams to be added
    grams = []

    # load text for each file given
    for file in files:
        file = open(file)
        text = str(file.read())

        # Use regex to break up the text into words
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

            # texts is a list of grams from 1 minus the current index to
            # the ngram count minus the current index
            texts = sentence[i - gramSize:i]
            text = ""
            for word in texts:
                text += word.text

            nextText = sentence[i].text

            # Add the word occurance to the ngram table
            if text in ngramTable:
                if nextText in ngramTable[text]:
                    ngramTable[text][nextText] += 1
                else:
                    ngramTable[text][nextText] = 1
            else:
                ngramTable[text] = OrderedDict()
                ngramTable[text][nextText] = 1

    # Generate the number of sentences the user wanted
    for i in range(numSentences):
        generateSentence()
        if i < numSentences - 1:
            print("----")


if __name__ == "__main__":
    # Get the user supplied variables
    numSentences = int(sys.argv[1])
    gramSize = int(sys.argv[2])

    for i in range(len(sys.argv) - 3):
        files.append(sys.argv[3 + i])

    if files == []:
        exit()

    main()
