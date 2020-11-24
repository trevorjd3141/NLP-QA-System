import sys

# resultReader was used to identify what questions were still
# being missed completely, match them to their respective
# question, answer, and response. This allowed for
# quicker and more precise assessments

def getQuestion(questionID, answerKeyLines):
    return answerKeyLines[answerKeyLines.index('QuestionID: ' + questionID)+1]

def getMissed(resultLines, missedIDWrite):
    dict = {
        "Where": 0,
        "When": 0,
        "What": 0,
        "Who": 0,
        "Why": 0,
        "How": 0,
        "According": 0,
    }
    for i in range(len(resultLines)):
        if 'Precision = 0.0' in resultLines[i]:
        #if 'F-measure = 0.00' in resultLines[i]:
            for j in range(i, 0, -1):
                if 'SCORING ' in resultLines[j]:
                    # missedIDWrite.write(resultLines[j].split("SCORING ", 1))
                    ID = ''.join([str(elem) for elem in resultLines[j].split("SCORING ", 1)])
                    missed.write(ID)
                    question = getQuestion(ID, answerKey)
                    updateDict(question, dict)
                    missed.write(question)
                    while j < len(resultLines) and '---------------' not in resultLines[j]:
                        if '\'' in resultLines[j]:
                            missed.write(resultLines[j])
                        j += 1
                    missed.write('\n')
                    break
                if '---------------' in resultLines[j]:
                    break
    for k, v in dict.items():
        missed.write(k + ': ' + str(v) + '\n')


def updateDict(question, dict):
    if question.split(' ')[1] in dict:
        dict[question.split(' ')[1]] += 1


resultTXT = open(sys.argv[1],"r").readlines()
answerKey = open(sys.argv[2],"r").readlines()
missed = open('missed.txt', "w")
getMissed(resultTXT, missed)
missed.close()
