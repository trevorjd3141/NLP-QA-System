import sys
import os

# def getZeroIDs(resultLines, missedIDWrite):
#     for line in resultLines:
#         if 'F-measure = 0.00' in line:
#             for i in range(line.inde)
def getZeroIDs(resultLines, missedIDWrite):
    zeroIDs = []
    for i in range(len(resultLines)):
        if 'F-measure = 0.00' in resultLines[i]:
            for j in range(i, 0, -1):
                if 'SCORING ' in resultLines[j]:
                    # missedIDWrite.write(resultLines[j].split("SCORING ", 1))
                    ID = ''.join([str(elem) for elem in resultLines[j].split("SCORING ", 1)])
                    missedIDWrite.write(ID)
                    zeroIDs.append(ID)
                    break
                if '---------------' in resultLines[j]:
                    break
    return zeroIDs

def getQuestions(zeroIDs, answerKeyLines, missedQWrite):
    questions = []
    for i in range(len(answerKeyLines)):
        if 'QuestionID:' in answerKeyLines[i]:
            for ID in zeroIDs:
                if ID in answerKeyLines[i]:
                    question = ''.join([str(elem) for elem in answerKeyLines[i+1].split("Question: ", 1)])
                    missedQWrite.write(question)
                    questions.append(question)
                    break
    questions.sort()
    #print(questions)
    return questions


resultTXT = open(sys.argv[1],"r").readlines()
answerKey = open(sys.argv[2],"r").readlines()
missedIDWR = open('missedIDs.txt', "w")
missedQWR = open('missedQs.txt', "w")
missedQSorted = open('missedQsSorted.txt', "w")
zeroIDs = getZeroIDs(resultTXT, missedIDWR)
sortedQuestions = getQuestions(zeroIDs, answerKey, missedQWR)
# missedQSorted.writelines(["%s\n" % item  for item in sortedQuestions])
missedQSorted.writelines([item  for item in sortedQuestions])
missedIDWR.close()
missedQWR.close()
missedQSorted.close()
