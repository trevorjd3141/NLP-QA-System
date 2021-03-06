"""
Provides Question types
Available Question types are the following:
Who, What, Why, Where, When, How
"""
import os

# Represents all information contained within a question
class Question:

    def __init__(self, id, text, difficulty):
        self.id = self.cleanline(id)
        self.text = self.cleanline(text)
        self.difficulty = self.cleanline(difficulty)

        # Final type values can be between Who, What, Why, When, Where, Quantity, and How.
        # That is, only the left most value of each item in potetialTypes
        # The other values are used purely for string recognition
        self.type = ''
        potentialTypes = (['Who', 'Whose'], ['Why'], ['According'],
                        ['What', 'Which'], ['When', 'What Year','How Far Back', 'How Long Ago'],
                        ['Where'], ['Quantity', 'How Much', 'How Many', 'How Far', 'How Old', 'Cost', 'How Big'], ['How'])
        for i in range(len(potentialTypes)):
            if self.containsSubstrings(text, potentialTypes[i], True):
                self.type = potentialTypes[i][0]
                break

        # Default type name is What in case the real
        # type was unable to be found
        if self.type == '':
            self.type = 'What'

        # Depending the strings contained within the text
        # and the type of question a further subtype can be
        # inferred.
        # EX: "How old is Johnny" obviously requires and numerical answer
        # Which can be inferred later if subtype is specified.
        self.subtype = ''
        if self.containsSubstrings(self.text, ['time', 'hour', 'How long']) and self.type in ('When', 'Quantity'):
            self.subtype = 'time'
        elif self.containsSubstrings(self.text, ['date', 'year']) and self.type in ('When'):
            self.subtype = 'date'
        elif self.containsSubstrings(self.text, ['age', 'old']) and self.type in ('Quantity'):
            self.subtype = 'age'
        elif self.containsSubstrings(self.text, ['cost', 'price', 'dollar']) and self.type in ('Quantity', 'What'):
            self.subtype = 'price'
        elif self.containsSubstrings(self.text, ['tall', 'distance', 'tall', 'wide', 'deep']) and self.type in ('Quantity', 'How'):
            self.subtype = 'length'
        elif self.containsSubstrings(self.text, ['weigh', 'heavy']) and self.type in ('Quantity'):
            self.subtype = 'weight'
        elif self.containsSubstrings(self.text, ['Who is']) and 6 > len(self.text.split()) > 2:
            self.subtype = 'simple who'
        elif self.containsSubstrings(self.text, ['What is']) and 6 > len(self.text.split()) > 2:
            self.subtype = 'simple what'
        elif self.containsSubstrings(self.text, ['Where is']) and 6 > len(self.text.split()) > 2:
            self.subtype = 'simple where'
        elif self.containsSubstrings(self.text, ['country', 'nation']) and self.type == 'What':
            self.subtype = 'country'
        elif self.containsSubstrings(self.text, ['province', 'territory']) and self.type == 'What':
            self.subtype = 'province'
        elif self.containsSubstrings(self.text, ['state', 'governor', 'states']) and self.type == 'What':
            self.subtype = 'state'
        elif self.containsSubstrings(self.text, ['mayor', 'city', 'town', 'village']) and self.type == 'What':
            self.subtype = 'city'
        elif self.containsSubstrings(self.text, ['type', 'what kind', 'which kind']) and self.type == 'What':
            self.subtype = 'class'
        elif self.containsSubstrings(self.text, ['work', 'volunteer']) and self.type == 'Where':
            self.subtype = 'organization'
    
    def cleanline(self, line):
        return line.split(':')[1].strip()

    # Returns true if any of the strings in matches
    # can be found in line
    #
    # lower is a variable requiring that case is not an issue
    # case should specifically be ignored when determined
    # question type but matters less when finding subtype
    def containsSubstrings(self, line, matches, lower=False):
        # Add the extra spaces to avoid cases such as 'age' in
        # 'teenage' triggering a true value
        line = ' ' + line + ' '
        if lower:
            return any(' ' + value.lower() + ' ' in line.lower() for value in matches)
        else:
            return any(' ' + value + ' ' in line for value in matches)

# Finds all question file names within directory
def getQuestionFilenames(directory):
    filenames = []
    for entry in os.scandir(directory):
        if entry.path.endswith(".questions"):
            filenames.append(entry.path)
    return filenames

# Maps question file names to a list of the texts
# of those files
def getQuestionTexts(filenames):
    texts = []
    for filename in filenames:
        file = open(filename, 'r')
        texts.append([line.strip() for line in file.readlines()])
    return texts

# Removes whitespace to keep only
# the QuestionID, Question Text, and Difficulty
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

# Creates instances of the Question class based
# upon information generated in groupQuestionTexts()
def createQuestions(questionInfo):
    return [Question(tupe[0], tupe[1], tupe[2]) for tupe in questionInfo]

def getQuestions(directory):
    questionFilenames = getQuestionFilenames(directory)
    questionTexts = getQuestionTexts(questionFilenames)
    questionInformation = groupQuestionTexts(questionTexts)
    questions = createQuestions(questionInformation)
    return questions