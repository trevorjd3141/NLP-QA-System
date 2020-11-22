import sys
import os


# def getZeroIDs(resultLines, missedIDWrite):
#     zeroIDs = []
#     for i in range(len(resultLines)):
#         if 'F-measure = 0.00' in resultLines[i]:
#             for j in range(i, 0, -1):
#                 if 'SCORING ' in resultLines[j]:
#                     # missedIDWrite.write(resultLines[j].split("SCORING ", 1))
#                     ID = ''.join([str(elem) for elem in resultLines[j].split("SCORING ", 1)])
#                     missedIDWrite.write(ID)
#                     question = getQuestion(ID, answerKey)
#                     missedIDWrite.write(question)
#                     zeroIDs.append(ID)
#                     while '---------------' not in resultLines[j]:
#                         if '\'' in resultLines[j]:
#                             missedIDWR
#                             j+=1
#                     break
#                 if '---------------' in resultLines[j]:
#                     break
#     return zeroIDs

# def getQuestions(zeroIDs, answerKeyLines, missedQWrite):
#     questions = []
#     for i in range(len(answerKeyLines)):
#         if 'QuestionID:' in answerKeyLines[i]:
#             for ID in zeroIDs:
#                 if ID in answerKeyLines[i]:
#                     question = ''.join([str(elem) for elem in answerKeyLines[i+1].split("Question: ", 1)])
#                     missedQWrite.write(question)
#                     questions.append(question)
#                     break
#     questions.sort()
#     #print(questions)
#     return questions

# resultTXT = open(sys.argv[1],"r").readlines()
# answerKey = open(sys.argv[2],"r").readlines()
# missedIDWR = open('missedIDs.txt', "w")
# missedQWR = open('missedQs.txt', "w")
# missedQSorted = open('missedQsSorted.txt', "w")
# zeroIDs = getZeroIDs(resultTXT, missedIDWR)
# sortedQuestions = getQuestions(zeroIDs, answerKey, missedQWR)
# # missedQSorted.writelines(["%s\n" % item  for item in sortedQuestions])
# missedQSorted.writelines([item  for item in sortedQuestions])
# missedIDWR.close()
# missedQWR.close()
# missedQSorted.close()

def getQuestion(questionID, answerKeyLines):
    return answerKeyLines[answerKeyLines.index('QuestionID: ' + questionID)+1]
    # for i in range(len(answerKeyLines)):
    #     if questionID in answerKeyLines[i]:
    #         question = answerKeyLines[i + 1]
    #         return question

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
        if 'F-measure = 0.00' in resultLines[i]:
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
