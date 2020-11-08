import typeQuestions
import namedEntityRecognition
import sys
import os
import spacy

def classify(question, story):
    # Grab potential entity types the answer will fit
    potentialEntities = questionMatchEntity(question)
    
    # Loop over entire story and grab all words that
    # fit the desired entity types
    storyID = story[0]
    tokens = story[1]
    potentialAnswers = []
    for token in tokens:
        if token.ent_type_ in potentialEntities:
            potentialAnswers.append(token.text)

    if len(potentialAnswers) > 0:
        return ' '.join(potentialAnswers)
    else:
        return ''

def filterStories(storyID, stories):
    for story in stories:
        if story[0] == storyID:
            return story

def filterQuestions(storyID, questions):
    filteredQuestions = [question for question in questions if question.id.startswith(storyID)]

    # Sort questions not by ascii value as that leads to xxx-10
    # being sorted before xxx-9 but my the value of the last digits.
    sortedQuestions = sorted(filteredQuestions, key=lambda question: int(question.id.split('-')[-1]))
    return sortedQuestions

def output(id, answer):
    print('QuestionID: ' + id)
    print('Answer: ' + answer)
    print()

def qa():
    file = open(sys.argv[1], "r")
    lines = [line.strip() for line in file.readlines()]
    directory = lines[0]
    storyIDs = lines[1:]

    questions = typeQuestions.getQuestions(directory)
    stories = namedEntityRecognition.getNamedEntities(directory)

    for id in storyIDs:
        filteredQuestions = filterQuestions(id, questions)
        story = filterStories(id, stories)

        # If there are no stories or questions return early
        # not likely to happen but included for robustness
        if story is None or filteredQuestions is None:
            continue

        for question in filteredQuestions:
            answer = classify(question, story)
            output(question.id, answer)

    file.close()

# Find the potential entity types the answer will
# fit given the question type and subtype
def questionMatchEntity(question):
    if question.type == 'Who':
        if question.subtype == 'simple who':
            return ['PERSON']
        return ['PERSON', 'ORG', 'NORP']
    elif question.type == 'What':
        if question.subtype == 'price':
            return ['MONEY']
        if question.subtype == 'simple what':
            return ['PRODUCT', 'EVENT', 'DATE']
        else:
            return ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENTAGE', 'ORDINAL']
    elif question.type == 'When':
        if question.subtype == 'time':
            return ['TIME']
        elif question.subtype == 'date':
            return ['DATE']
        elif question.subtype == 'simple when':
            return ['TIME', 'DATE']
        return ['DATE', 'TIME', 'PERCENT', 'ORDINAL']
    elif question.type == 'Where':
        if question.subtype == 'organization':
            return ['ORG']
        return ['FAC', 'ORG', 'GPE', 'LOC', 'EVENT']
    elif question.type == 'Why':
        return []
    elif question.type == 'How':
        if question.subtype == 'length':
            return ['QUANTITY']
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

    print(possibleAnswers)

    sorted_answers = sorted(possibleAnswers, key=possibleAnswers.get)

    print(sorted_answers)

def fooTest():
    nlp = spacy.load("en_core_web_sm")
    question = 'How tall was Jared?'
    story = 'The car was red. The car was man. The man was Jared. Jared was 6ft tall.'
    tokens = nlp(story)

    foo(question, tokens)

if __name__ == '__main__':
    qa()