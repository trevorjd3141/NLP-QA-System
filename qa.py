import typeQuestions
import namedEntityRecognition
import sys

def classify(question, token):
    # based on the question text and type
    # and the story provide an answer
    # return nothing for now
    return ''

def filterTokens(storyID):
    # Grabs all questions that pertain to the 
    # story in question and sorts them
    pass

def filterQuestions(storyID):
    # Grabs all questions that pertain to the 
    # question in question and sorts them
    pass

def output(id, answer):
    # Formats an id and answer to what we need
    # QuestionID: ...
    # Answer: ...
    # !! If just need to print:
    print('QuestionID: ' + id + '\n')
    # !! NOTE TO SELF:  Do we need to double return on end of answer??
    print('Answer: ' + answer + '\n')

    # # !! If we have to write to a file we'll need some 3rd file paramater
    # # !! (AND will need to OPEN and CLOSE it in qa())
    # # !! Same applies here about double returns after answer
    # # !! NOTE: If we do write to some file it will be in project folder (no return)
    # file.write('QuestionID: ' + id  + '\n'
    #            + 'Answer: ' + answer + '\n')

    pass

def qa():
    # Get the questionTypes and NREs
    # !! We're gonna have to keep ents and qs as uni vars if to be
    # !! used out of scope (i.e. when filtering)
    qs = typeQuestions.getQuestions()
    ents = namedEntityRecognition.getNamedEntities()

    # Loop over all storyIDs in input
    # !! Not sure what we're thinking of doing to grab the ID's here
    # !! But this is how I'd have grabbed them initially (this should be
    # !! changed if there's away to return from qs or ents the order together)
    inputFile = open(sys.argv[1], "r")
    fileLines = inputFile.readlines()

    # for each storyID retrieve the NRE and appropriate questions
    for id in fileLines:
        # !! not sure if better way to skip first in for-each, could set to null?
        if fileLines[0] == id:
            continue
        # !! Assured we're only catching IDs, we continue
        # !! NOTE TO SELF: check if values need to be returned/stored for these calls
        filteredQuestions = filterQuestions(id)
        filteredTokens = filterTokens(id)

        # Sort questions and go over each in its time applying appropriate rules
        # !! Not sure if above just means to pass to classifier
        ans = classify(filteredQuestions, filteredTokens)

        # Output ID with answer
        output(id, ans)

    # !! Close file
    inputFile.close()

    pass

if __name__ == '__main__':
    qa()

    # # !! This is how I was doing single iterations at a time
    # # !! If we decide to pass one ID at a time this would be the work flow
    # inputFile = open(sys.argv[1], "r")
    # fileLines = inputFile.readlines()
    # # first line is dir path
    # path = fileLines[0]
    #
    # for ID in fileLines:
    #     storyDoc = open(path + ID + '.story')
    #     questionList = open(path + ID + '.questions')