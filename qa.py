import typeQuestions
import namedEntityRecognition
import sys
import random


def classify(question, token):
    # match q type with possible ent types
    potentialEnts = questionMatchEnt(question)

    potentialAnswers = []

    # !! need to handle WHY and HOW

    for t in token[1]:
        if t.ent_ in potentialEnts:
            potentialAnswers.append(t.text)

    return random.choice(potentialAnswers)


def filterStories(storyID, stories):
    for story in stories:
        if story[0] == storyID:
            return story


def filterQuestions(storyID, questions):
    filteredQuestions = [question for question in questions if question.id.startswith(storyID)]
    sortedQuestions = sorted(filteredQuestions, key=lambda question: question.id)
    return sortedQuestions


def output(id, answer):
    print('QuestionID: ' + id)
    print('Answer: ' + answer)
    print()

    # # !! If we have to write to a file we'll need some 3rd file paramater
    # # !! (AND will need to OPEN and CLOSE it in qa())
    # # !! Same applies here about double returns after answer
    # # !! NOTE: If we do write to some file it will be in project folder (no return)
    # file.write('QuestionID: ' + id  + '\n'
    #            + 'Answer: ' + answer + '\n')
    pass


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

        # !! @Where would this be happening??
        if story is None or filteredQuestions is None:
            continue

        for question in filteredQuestions:
            answer = classify(question, story)
            output(question.id, answer)

    # Close file
    file.close()
    pass

def handleWHY(question):
    answer = 'WHY'
    # Here we could likely use syntax of the question to help solve for an answer
    return answer

def handleHOW(question):
    answer = 'HOW'
    # Here we could likely use syntax of the question to help solve for an answer
    return answer

def questionMatchEnt(question):
    # !! @Set up type and subtype distinction properly
    questionType = question.type

    if questionType == 'Who':
        EntTypes = ['PERSON', 'ORG', 'NORP']

    # !!@ figure out how this should be handled with your implementation
    if questionType == 'What' or questionType == 'Which':
        if questionType == 'Which':
            EntTypes = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART',
                        'LAW', 'LANGUAGE', 'DATE', 'ORDINAL']
        else:
            EntTypes = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART',
                        'LAW', 'LANGUAGE', 'DATE', 'TIME', 'PERCENTAGE', 'ORDINAL']

    if questionType == 'Why':
        # will have to do further parse
        EntTypes = ['WHY']

    # !!@ figure out how this should be handled with your implementation
    if questionType == 'When':

        if questionType == 'What Year':
            EntTypes = ['DATE']

        elif questionType == 'How Far Back':
            EntTypes = ['DATE', 'TIME', 'PERCENT', 'ORDINAL']

        elif questionType == 'How Long Ago':
            EntTypes = ['DATE', 'TIME', 'PERCENT', 'ORDINAL']

        # if 'When' only
        else:
            EntTypes = ['DATE', 'TIME', 'EVENT', 'PERCENT', 'ORDINAL']

    if questionType == 'Where':
        EntTypes = ['FAC', 'ORG', 'GPE', 'LOC', 'EVENT']
        # Could also include PRODUCT (in the car) or WORK_OF_ART (in Harry Potter) or LAW (in the Bill Of Rights)

    # !!@ figure out how this should be handled with your implementation
    if questionType == 'Quantity':

        if questionType == 'How Much':
            EntTypes = ['TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'CARRDINAL']

        elif questionType == 'How Many':
            EntTypes = ['TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'CARRDINAL']

        elif questionType == 'How Far':
            EntTypes = ['DATE', 'TIME', 'PERCENT', 'QUANTITY', 'ORDINAL', 'CARRDINAL']

        elif questionType == 'How Old':
            EntTypes = ['DATE', 'TIME', 'PERCENT', 'QUANTITY']

        elif questionType == 'Cost':
            EntTypes = ['DATE', 'TIME', 'PERCENT', 'QUANTITY', 'ORDINAL']

        elif questionType == 'How Big':
            EntTypes = ['QUANTITY']

        # if 'Quantity' only
        else:
            EntTypes = ['DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARRDINAL']

    if questionType == 'How':
        # will have to do further parse
        EntTypes = ['HOW']

    return EntTypes

if __name__ == '__main__':
    qa()
