#from nltk imprt Tree
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





if __name__ == '__main__':
    testing()
