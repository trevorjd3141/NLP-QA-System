import typeQuestions
import namedEntityRecognition
import sys
import spacy


def classify(question, story):
    #print('classify')
    potentialEntities = questionMatchEntity(question)

    potentialAnswers = []

    storyID = story[0]
    tokens = story[1]
    for token in tokens:
        if token.ent_type_ in potentialEntities:
            potentialAnswers.append(token.text)

    if len(potentialAnswers) > 0:
        return ' '.join(potentialAnswers)
    else:
        return ''

def filterStories(storyID, stories):
    #print('filterStories')
    for story in stories:
        if story[0] == storyID:
            return story

def filterQuestions(storyID, questions):
    #print('filterQuestions')
    filteredQuestions = [question for question in questions if question.id.startswith(storyID)]
    sortedQuestions = sorted(filteredQuestions, key=lambda question: question.id)
    return sortedQuestions

def output(id, answer):
    print('QuestionID: ' + id)
    print('Answer: ' + 'blank')
    print()

def qa():
    #print('qa')
    file = open(sys.argv[1], "r")
    lines = [line.strip() for line in file.readlines()]
    directory = lines[0]
    storyIDs = lines[1:]

    questions = typeQuestions.getQuestions(directory)
    stories = namedEntityRecognition.getNamedEntities(directory)

    for id in storyIDs:
        filteredQuestions = filterQuestions(id, questions)
        story = filterStories(id, stories)

        # !! @Where would this be happening??
        if story is None or filteredQuestions is None:
            #print('ITS HERE!!')
            continue

        for question in filteredQuestions:
            answer = classify(question, story)
            output(question.id, answer)

    # Close file
    file.close()
    pass

# Return valid entity types given the question type
def questionMatchEntity(question):
    if question.type == 'Who':
        return ['PERSON', 'ORG', 'NORP']
    elif question.type == 'What':
        # ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENTAGE', 'ORDINAL']
        return []
    elif question.type == 'When':
        if question.subtype == 'time':
            return ['TIME']
        elif question.subtype == 'date':
            return ['DATE']
        return ['DATE', 'TIME', 'PERCENT', 'ORDINAL']
    elif question.type == 'Where':
        if question.subtype == 'organization':
            return ['ORG']
        return ['FAC', 'ORG', 'GPE', 'LOC', 'EVENT']
    elif question.type == 'Why':
        return []
    elif question.type == 'How':
        return []
    elif question.type == 'Quantity':
        if question.subtype == 'time':
            return ['TIME']
        elif question.subtype == 'age':
            return ['DATE', 'TIME']
        elif question.subtype == 'price':
            return ['PERCENT', 'MONEY']
        elif question.subtype == 'length':
            return ['QUANTITY']
        elif question.subtype == 'weight':
            return ['QUANTITY']
        return ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
    else:
        return []


def foo(question, possibleTokens):
    nlp = spacy.load("en_core_web_sm")
    #doc = nlp(question.text)
    doc = nlp(question)

    # get direct object and its verb from question
    for d in doc:
        if d.dep_ == 'nsubj':
            nsubj = d
            dobj=''
            root=''
        elif d.dep_ == 'dobj':
            dobj = d
            nsubj=''
            root=''
        elif d.dep_ == 'ROOT':
            root = d
            dobj=''
            nsubj=''


    # create a dictionary of possible answers
    possibleAnswers = {}
    # each time nsubj, dobj, or root appear in a token's subtree we increase it's score
    for token in possibleTokens:
        if token.text not in possibleAnswers:
            #print(token.text)
            possibleAnswers[token.text] = 0
        for s in token.subtree:
            if type(nsubj) != type(''):
                #print('n: ' + nsubj.text)
                if nsubj.lemma == s.lemma:
                    possibleAnswers[token.text] += 1
            if type(dobj) != type(''):
                #print('d: ' + dobj.text)
                if dobj.lemma == s.lemma:
                    possibleAnswers[token.text] += 1
            if type(root) != type(''):
                #print('r: ' + root.text)
                if root.lemma == s.lemma:
                    possibleAnswers[token.text] += 1

    # print(possibleAnswers)
    #
    # sorted_answers = sorted(possibleAnswers, key=possibleAnswers.get)
    #
    # print(sorted_answers)



# # http://ciir.cs.umass.edu/pubfiles/ir-239.pdf
# def score(topPassages, possibleAnswers):
#     # still need to define these
#     bestWindow = ''
#     answerScores = []
#
#     for passage in topPassages:
#         score = 0
#         for answerCandidate in possibleAnswers:
#             occurences = getOccurrences(answerCandidate, passage)
#             matchedWords = occurences[1]
#             score += occurences[0]
#             # need way of grabbing best window, might be done in getOccurences/inSingleSentence
#             # might have to be bigger than sing sentence
#             # lets say we already have it
#             score += matchedWords.len()/bestWindow.len()
#             score += .5/distanceFromCenterOfWindow(answerCandidate, bestWindow)
#
# def getOccurrences(answerCandidate, passage):
#     score = 0
#     matchingWords = []
#     for word in answerCandidate:
#         if word in passage:
#             score += 1
#             matchingWords.append(word)
#     # tuple ( bool of if one sent, sent)
#     allOneSentence = inSingleSentence(matchingWords, passage)
#     if (allOneSentence[0]):
#         score += .5
#
#     return (score, matchingWords)
#
# def inSingleSentence(words, passage):
#     # Place holder for actual sentence splitter (check spacy)
#     sentences = passage.split('.')
#     for sent in sentences:
#         allOneSent = True
#         for word in words:
#             if word not in sent.split():
#                 allOneSent = False
#                 break
#
#         if allOneSent:
#             # only supposed to get score but could be helpful later
#             return (True, sent)
#
#     # we could return the best sentence here instead of ''
#     return (False, '')
#
# def getWindow(answerCandidate, passage):
#     score = 0
#     sentence = ''
#     return (sentence, score)
#
# def distanceFromCenterOfWindow(answerCandidate, bestWindow):
#     # mentions token offset here instead of just length.. might check
#
#     return abs(round(bestWindow.len/2) - bestWindow.index(answerCandidate))
#
# # stop implementing above if Trevor's system is similar
#

# given a sentence
def dependency():
    nlp = spacy.load("en_core_web_sm")

    question = 'How tall was Jared?'
    parsedQuestionTokensAndRoot = sentenceParse(question, nlp)
    questionTokens = parsedQuestionTokensAndRoot[0]
    questionRoots = parsedQuestionTokensAndRoot[1]

    story = 'Jared was 6ft tall.'
    parsedStoryTokensAndRoot = sentenceParse(story, nlp)
    storyTokens = parsedQuestionTokensAndRoot[0]
    storyRoots = parsedQuestionTokensAndRoot[1]

    rootPairTuples = rootPairs(questionRoots, storyRoots)

    # from here it'll likely get more dependent on question type
    # if the question is just asking for a factoid, it'll likely only need the direct obj
    # let's assume this to be the case
    rTupe = rootPairTuples[0]
    sRoot = rTupe[1]
    for child in sRoot.children:
        if child.dep_ == 'dobj':
            if child.text not in question:
                return child
        if child.dep_ == 'nsubj':
            if child.text not in question:
                return child
    # if we don't find what we're looking for, just return the story sentence
    return story

def sentenceParse (sent, nlp):
    tokens = nlp(sent)
    roots = []
    for t in tokens:
        if t.dep_ == 'root':
            roots.append(t)

    return (tokens, roots)

def rootPairs(questionRoots, storyRoots):
    rootPairs = []
    for qRoot in questionRoots:
        qRootLemm = qRoot.lemma_

        for sRoot in storyRoots:
            sRootLemm = sRoot.lemma_

            if qRootLemm ==  sRootLemm:
                rootPairs.append((qRoot, sRoot))

    return rootPairs










def nltk_tree(nodes):


if __name__ == '__main__':
    dependency()
    #qa()

