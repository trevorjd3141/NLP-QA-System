import typeQuestions
import namedEntityRecognition
import textWeighter
import sys
import os
import spacy

SENTENCEWINDOW = 3
BACKUPWINDOW = 1

def classify(question, story, nlp):
    text = story[1]

    # Grab potential entity types the answer will fit
    text = textWeighter.filterQuestions(question, text, SENTENCEWINDOW)
    potentialEntities = questionMatchEntity(question)

    # Find the 'because' for why questions
    # starting with the most likely.
    indicators = ['because', 'so that', 'Because']
    if question.type == 'Why' and any([indicator in story[1] for indicator in indicators]):
        ranked = textWeighter.filterQuestions(question, story[1], ranked=True)
        i = 1
        
        # Make sure i never goes higher than the length
        # of the list
        for i in range(len(ranked)):
            sentence = ranked[i]
            if 'because' in ranked[i]:
                return 'because' + sentence.split('because')[1]
            elif 'so that' in ranked[i]:
                return 'so that' + sentence.split('so that')[1]
            elif 'Because' in ranked[i]:
                return sentence.split(',')[0]
    
    # Loop over entire story and grab all words that
    # fit the desired entity types
    storyID = story[0]
    tokens = nlp(text)
    potentialAnswers = []
    for token in tokens:
        if token.ent_type_ in potentialEntities:
            potentialAnswers.append(token.text)
            
    if len(potentialAnswers) > 0:
        return ' '.join(list(set(potentialAnswers)))
    else:
        return textWeighter.filterQuestions(question, story[1], BACKUPWINDOW)

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

def qa():
    file = open(sys.argv[1], "r")
    lines = [line.strip() for line in file.readlines()]
    directory = lines[0]
    storyIDs = lines[1:]

    questions = typeQuestions.getQuestions(directory)
    stories = namedEntityRecognition.getNamedEntities(directory)

    nlp = spacy.load("en_core_web_sm")
    for id in storyIDs:
        filteredQuestions = filterQuestions(id, questions)
        story = filterStories(id, stories)

        # If there are no stories or questions return early
        # not likely to happen but included for robustness
        if story is None or filteredQuestions is None:
            continue

        for question in filteredQuestions:
            answer = classify(question, story, nlp)
            output(question.id, answer)

    file.close()

if __name__ == '__main__':
    qa()