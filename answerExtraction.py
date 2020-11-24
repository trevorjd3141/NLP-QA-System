#from nltk imprt Tree
import textWeighter
import qa
import spacy

# def getAnswer(potentialAnswers, question):
#     distAns = []
#     for pAnswer in potentialAnswers:
#         distAns.append(distance(pAnswer, question))
#     answer = min(distAns)[1]
#     return answer
#
# def distance(answer, question):
#     score = 0.0
#     answer = ''
#     return (score, answer)

# def getTree(sentence):
#     doc = nlp(sentence)
#     tree = to_nltk_tree(doc.sent.root)
#     return tree

# def to_nltk_tree(node):
#     if node.n_lefts + node.n_rights > 0:
#         return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
#     else:
#         return node.orth_



# def testing():
#     potentialAnswer = ['he used his hands to dig by the tree', 'the boys were stuck in the cave', 'trapped, they wished to make an ice cave']
#     question = 'What did they use to dig the ice cave?'
#     #getAnswer(potentialAnswer, question)
#     testing2(potentialAnswer, question)
#
#
# def testing2(potentialAnswer, question):
#     doc = nlp(question)
#     #print ('question')
#     for token in doc:
#         if token.dep_ == 'ROOT':
#             qRootLemma = token.lemma
#
#     for sent in potentialAnswer:
#         doc = nlp(sent)
#         for token in doc:
#             if token.dep_ == 'ROOT':
#                 if token.lemma == qRootLemma:
#                     print(sent)


def answer(question, story, nlp):
    mostLikelySentences = textWeighter.filterQuestions(question, story[1], ranked=True)
    mostLikelySentence = mostLikelySentences[0]
    # mostLikelySentence = stopParse(question, mostLikelySentences, nlp)
    mostLikelySentence = rootStrictLemma(question, mostLikelySentences, nlp)
    return mostLikelySentence

    #return entityMatcher(mostLikelySentence, nlp(mostLikelySentence), question)

def rootStrictLemma(question, mostLikelySentences, nlp):
    mostLikelySentence = mostLikelySentences[0]
    qDoc = nlp(question.text)
    # qRootLemma = 0
    # qDobjLemma = 0
    # qNsubjLemma = 0
    # qPobjLemma = 0
    qDeps = [0,0,0,0]
    for token in qDoc:
        if token.dep_ == 'ROOT':
            qRootLemma = token.lemma
            qDeps[0] = qRootLemma
        elif token.dep_ == 'dobj':
            qDeps[1] = token.lemma
        elif token.dep_ == 'nsubj':
            qDeps[2] = token.lemma
        elif token.dep_ == 'pobj':
            qDeps[3] = token.lemma
    sent = getMostLikely(qDeps, mostLikelySentences, nlp)[0]
    doc = nlp(sent)
    return entityMatcher(sent, doc, question)

def getMostLikely(qDeps, mostLikely, nlp):
    for dependency in qDeps:
        potential = []
        if dependency != 0:
            potential = lemmaCheck(dependency, mostLikely, nlp)
            if len(potential) != 0:
                mostLikely = potential.copy()
    return mostLikely

    #[t for t in doc if not token.is_stop]
def lemmaCheck(qDep, sentences, nlp):
    p = []
    for sent in sentences:
        doc = nlp(sent)
        for token in doc:
            if token.lemma == qDep:
                p.append(sent)
    return p

    #
    # def lemmaCheck(qDep, mostLikelySentences):
    #     p = []
    #     for sent in mostLikelySentences:
    #         doc = nlp(sent)
    #         for token in doc:
    #             if token.lemma == qLemma:
    #                 p.append(sent)
    #                 return entityMatcher(sent, doc, question)
    #
    # return mostLikelySentences[0]

def stopParse(question, mostLikelySentences, nlp):

    questionTokens = removeStops(question.text, nlp)

    bestSent = mostLikelySentences[0]
    bestSentTokens =[]
    score = 0
    for sent in mostLikelySentences:
        sentTokens = removeStops(sent, nlp)
        potScore = 0
        potSentTokens = []
        for qToken in questionTokens:
            for sToken in sentTokens:
                if qToken.similarity(sToken) > 0.5:
                    potScore += 1
                else:
                    potSentTokens.append(sToken)
        if potScore > score or (potScore == score and len(potSentTokens) > len(bestSentTokens)):
            score = potScore
            bestSentTokens = potSentTokens
            bestSent = sent

    return entityMatcher(bestSent, bestSentTokens, question)

def removeStops(sentence, nlp):
    doc = nlp(sentence)
    tokens = [token for token in doc if not token.is_stop]
    return tokens

def entityMatcher(sent, sentTokens, question):
    potentialEntities = qa.questionMatchEntity(question)
    potentialAnswers = []
    for token in sentTokens:
        if token.ent_type_ in potentialEntities:
            potentialAnswers.append(token.text)

    if len(potentialAnswers) > 0:
        return ' '.join(set(word for word in potentialAnswers if word not in question.text))
    else:
        return sent

qText = 'If water is left in an opened container for 24 hours, what happens to many of the chemicals?'
text = 'You can leave water in an open container for 24 hours, and many of the chemicals will evaporate'


nlp = spacy.load('en_core_web_md')
#doc = nlp(text)
p = ''
# for ent in doc.ents:
#     print(ent.text + ': ' + ent.label_)
doc = nlp(qText)
for token in doc:
    #p += (token.text + ': ' + token.ent_type_ + ' ')
    p += (token.text + '/' + token.dep_ + ' ')

doc = nlp(text)
for token in doc:
    #p += (token.text + ': ' + token.ent_type_ + ' ')
    p += (token.text + '/' + token.dep_ + ' ')

# #     if token.text == 'summer':
# #         print('summer ancestors')
# #         print([token.text for token in token.ancestors])
#      if token.text == 'seals':
#          print('seals/ head: ' + token.head.text + ' / lefts: ')
#          print([token.text for token in token.lefts])
#          print(' / rights: ')
#          print([token.text for token in token.rights])
print(p)
# #print(token.text + ' ' + token.dep_ for token in doc)