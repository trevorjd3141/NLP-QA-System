import typeQuestions
import namedEntityRecognition
import sys
import spacy


def classify(question, story):
    print('classify')
    potentialEntities = questionMatchEntity(question)

    potentialAnswers = []

    storyID = story[0]
    tokens = story[1]
    for token in tokens:
        if token.ent_ in potentialEntities:
            potentialAnswers.append(token.text)

    return random.choice(potentialAnswers)

def filterStories(storyID, stories):
    print('filterStories')
    for story in stories:
        if story[0] == storyID:
            return story

def filterQuestions(storyID, questions):
    print('filterQuestions')
    filteredQuestions = [question for question in questions if question.id.startswith(storyID)]
    sortedQuestions = sorted(filteredQuestions, key=lambda question: question.id)
    return sortedQuestions

def output(id, answer):
    print('QuestionID: ' + id)
    print('Answer: ' + 'blank')
    print()

def qa():
    print('qa')
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
            print('ITS HERE!!')
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


# def foo(question, possibleTokens):
#     nlp = spacy.load("en_core_web_sm")
#     #doc = nlp(question.text)
#     doc = nlp(question)
#
#     # get direct object and its verb from question
#     for d in doc:
#         if d.dep_ == 'nsubj':
#             nsubj = d
#             dobj=''
#             root=''
#         elif d.dep_ == 'dobj':
#             dobj = d
#             nsubj=''
#             root=''
#         elif d.dep_ == 'ROOT':
#             root = d
#             dobj=''
#             nsubj=''
#
#
#     # create a dictionary of possible answers
#     possibleAnswers = {}
#     # each time nsubj, dobj, or root appear in a token's subtree we increase it's score
#     for token in possibleTokens:
#         if token.text not in possibleAnswers:
#             possibleAnswers[token.text] = 0
#         for s in token.subtree:
#             if type(nsubj) != type(''):
#                 print('n: ' + nsubj.text)
#                 if nsubj.lemma == s.lemma:
#                     possibleAnswers[token.text] += 1
#             if type(dobj) != type(''):
#                 print('d: ' + dobj.text)
#                 if dobj.lemma == s.lemma:
#                     possibleAnswers[token.text] += 1
#             if type(root) != type(''):
#                 print('r: ' + root.text)
#                 if root.lemma == s.lemma:
#                     possibleAnswers[token.text] += 1
#
#     print(possibleAnswers['tall'])
#     print(possibleAnswers['The'])
#     sorted_answers = sorted(possibleAnswers, key=possibleAnswers.get)
#
#     print (sorted_answers)

# def fooTest():
#     nlp = spacy.load("en_core_web_sm")
#     question = 'How tall was jared?'
#     story = 'The car was red. The car was man. The man was Jared. Jared was 6ft tall.'
#     tokens = nlp(story)
#
#     foo(question, tokens)


if __name__ == '__main__':
    # fooTest()
    qa()