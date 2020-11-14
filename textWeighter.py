"""
Eliminates all but the top k rated sentences to 
weed out sentences that are extremely unlikely to have the answer.
"""
import string
import math
from collections import defaultdict

# Retrieves all common words like
# 'of', 'and', and 'the' that we don't
# want to consider.
def fetchStopwords(filename):
    file = open(filename, 'r')
    return [line.strip().lower() for line in file.readlines()]

# Filters a text into a list of filtered words
def filterSplitText(text, stopwords):
    return [''.join(char for char in word.lower() if char not in string.punctuation) for word in text.split() if word not in stopwords]

# Turns a list into a frequency dictionary of words
def getFrequency(text):
    freq = defaultdict(int)
    for word in text:
        freq[word] += 1
    return freq

# Creates a signatureVector from a frequencyDict and vocab
def createVector(vocab, freqDict):
    # create signature vector
    vec = [0] * len(vocab)
    for i in range(len(vocab)):
        vec[i] += freqDict[vocab[i]]
    return vec

# Gives a value for the similarity of two texts
def cosineDistance(x, y):
    ProductXY = 0
    squaredSumX = 0
    squaredSumY = 0
    for i in range(len(x)):
        ProductXY += x[i] * y[i]
        squaredSumX += x[i] * x[i]
        squaredSumY += y[i] * y[i]
    if squaredSumX and squaredSumY:
        return ProductXY / (math.sqrt(squaredSumX) * math.sqrt(squaredSumY))
    else:
        return 0

# Main
def filterQuestions(question, story, k=3, ranked=False):

    # Get stopwords
    stopwords = fetchStopwords('data/stopwords.txt')

    # Get vocab
    words = filterSplitText(story, stopwords)
    vocab = list(set(words))

    # Filter story
    sentences = [sentence for sentence in story.split('. ')]
    filteredSentences = [filterSplitText(sentence, stopwords) for sentence in sentences]

    # Filter question
    filteredQuestion = filterSplitText(question.text, stopwords)

    scores = []
    for i in range(len(filteredSentences)):
        sentence = filteredSentences[i]
        sentenceVector = createVector(vocab, getFrequency(sentence))

        questionVector = createVector(vocab, getFrequency(filteredQuestion))
        
        score = cosineDistance(sentenceVector, questionVector)
        scores.append((score, i))
    scores.sort(key = lambda score: score[0])

    if ranked:
        return [sentences[pair[1]] for pair in scores]
    else:
        winners = scores[-k:]
        winners = [pair[1] for pair in winners]
        newStory = '. '.join([sentences[i] for i in range(len(sentences)) if i in winners])
        return newStory