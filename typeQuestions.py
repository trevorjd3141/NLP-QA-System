"""
Provides Question types
Available Question types are the following:
Who, What, Why, Where, When, How
"""
import os

def cleanline(line):
    return line.split(':')[1].strip()

def containsSubstrings(line, matches):
    return any(value in line.lower() for value in matches)

class Question:

    def __init__(self, id, text, difficulty):
        self.id = cleanline(id)
        self.text = cleanline(text)
        self.difficulty = cleanline(difficulty)


def getQuestionFilenames():
    cwd = os.getcwd()
    filenames = []
    for entry in os.scandir(cwd+'\\data'):
        if entry.path.endswith(".questions"):
            filenames.append(entry.path)
    return filenames

def getQuestionTexts(filenames):
    texts = []
    for filename in filenames:
        file = open(filename, 'r')
        texts.append([line.strip() for line in file.readlines()])
    return texts

def groupQuestionTexts(texts):
    groupedQuestions = []
    group = []
    for text in texts:
        for line in text:
            if line.startswith(('QuestionID:', 'Question:', 'Difficulty:')):
                group.append(line)
                if len(group) == 3:
                    groupedQuestions.append(tuple(group))
                    group = []
    return groupedQuestions

def createQuestions(questionInfo):
    return [Question(tupe[0], tupe[1], tupe[2]) for tupe in questionInfo]

def getQuestions():
    questionFilenames = getQuestionFilenames()
    questionTexts = getQuestionTexts(questionFilenames)
    questionInformation = groupQuestionTexts(questionTexts)
    questions = createQuestions(questionInformation)
    return questions

if __name__ == '__main__':
    getQuestions()