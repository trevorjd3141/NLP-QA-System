#from nltk imprt Tree
import textWeighter
import qa
import spacy
nlp = spacy.load('en_core_web_sm')

def getAnswer(potentialAnswers, question):
    distAns = []
    for pAnswer in potentialAnswers:
        distAns.append(distance(pAnswer, question))
    answer = min(distAns)[1]
    return answer

def distance(answer, question):
    score = 0.0
    answer = ''


    return (score, answer)

# def getTree(sentence):
#     doc = nlp(sentence)
#     tree = to_nltk_tree(doc.sent.root)
#     return tree


# def to_nltk_tree(node):
#     if node.n_lefts + node.n_rights > 0:
#         return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
#     else:
#         return node.orth_



def testing():
    potentialAnswer = ['he used his hands to dig by the tree', 'the boys were stuck in the cave', 'trapped, they wished to make an ice cave']
    question = 'What did they use to dig the ice cave?'
    #getAnswer(potentialAnswer, question)
    testing2(potentialAnswer, question)


def testing2(potentialAnswer, question):
    doc = nlp(question)
    #print ('question')
    for token in doc:
        if token.dep_ == 'ROOT':
            qRootLemma = token.lemma

    for sent in potentialAnswer:
        doc = nlp(sent)
        for token in doc:
            if token.dep_ == 'ROOT':
                if token.lemma == qRootLemma:
                    print(sent)


def answer(question, story, nlp):
    mostLikelySentences = textWeighter.filterQuestions(question, story[1], ranked=True)
    mostLikelySentence = mostLikelySentences[0]
    qDoc = nlp(question.text)
    qRootLemma = 0
    for token in qDoc:
        if token.dep_ == 'ROOT':
            qRootLemma = token.lemma

    # rootedSents = []
    # rootedDocs = []
    for sent in mostLikelySentences:
        doc = nlp(sent)
        for token in doc:
            if token.dep_ == 'ROOT':
                if token.lemma == qRootLemma:
                    #return sent
                    return entityMatcher(sent, doc, question)
                    # rootedDocs.append(doc)
                    # rootedSents.append(sent)
                    # break

    # if len(rootedSents) > 0:
    #     return entityMatcherWhat(rootedSents, rootedDocs, question)

    return mostLikelySentence

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
    # for docs in sentTokens:
    #     for token in docs:
    #         if token.ent_type_ in potentialEntities:
    #             potentialAnswers.append(token.text)
    #
    # if len(potentialAnswers) > 0:
    #     return ' '.join(set(word for word in potentialAnswers if word not in question.text))
    # else:
    #     return sent[0]