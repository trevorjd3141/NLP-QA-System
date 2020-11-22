import typeQuestions
import namedEntityRecognition
import textWeighter
import sys
import os
import spacy

SENTENCEWINDOW = 3
BACKUPWINDOW = 1
SENTENCETRIM = 2

def whatAnswer(question, story, nlp):


    mostLikelySentences = textWeighter.filterQuestions(question, story[1], ranked=True)
    mostLikelySentence = mostLikelySentences[0]
    qDoc = nlp(question.text)
    qRootLemma = 0
    for token in qDoc:
        if token.dep_ == 'ROOT':
            qRootLemma = token.lemma

    # rootedSents = []
    # rootedDocs = []
    for sent in mostLikelySentences:
        doc = nlp(sent)
        for token in doc:
            if token.dep_ == 'ROOT':
                if token.lemma == qRootLemma:
                    #return sent
                    return entityMatcherWhat(sent, doc, question)
                    # rootedDocs.append(doc)
                    # rootedSents.append(sent)
                    # break

    # if len(rootedSents) > 0:
    #     return entityMatcherWhat(rootedSents, rootedDocs, question)

    return mostLikelySentence

def entityMatcherWhat(sent, sentTokens, question):
    potentialEntities = questionMatchEntity(question)
    potentialAnswers = []
    for token in sentTokens:
        if token.ent_type_ in potentialEntities:
            potentialAnswers.append(token.text)

    if len(potentialAnswers) > 0:
        return ' '.join(set(word for word in potentialAnswers if word not in question.text))
    else:
        return sent
    # for docs in sentTokens:
    #     for token in docs:
    #         if token.ent_type_ in potentialEntities:
    #             potentialAnswers.append(token.text)
    #
    # if len(potentialAnswers) > 0:
    #     return ' '.join(set(word for word in potentialAnswers if word not in question.text))
    # else:
    #     return sent[0]





# Retrieves all common words like
# 'of', 'and', and 'the' that we don't
# want to consider.
def fetchStopwords(filename):
    file = open(filename, 'r')
    return [line.strip().lower() for line in file.readlines()]

# Find the 'because' for why questions
# starting with the most likely.
def whySplit(question, story):
    indicators = ['because', 'so that', 'Because', 'so they', 'so she', 'so he', 'Due to', 'due to']
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
            elif 'so they' in ranked[i]:
                return 'so they' + sentence.split('so they')[1]
            elif 'so he' in ranked[i]:
                return 'so he' + sentence.split('so he')[1]
            elif 'so she' in ranked[i]:
                return 'so she' + sentence.split('so she')[1]
            elif 'due to' in ranked[i]:
                return 'due to' + sentence.split('due to')[1]
            elif 'Due to' in ranked[i]:
                return sentence.split(',')[0]
            elif 'Because' in ranked[i]:
                return sentence.split(',')[0]

# Loop over entire story and grab all words that
# fit the desired entity types
# This is only for 'Who', 'What', 'Where' types
# and various other subtypes
# Grab potential entity types the answer will fit
def entityMatch(question, story, nlp):
    potentialEntities = questionMatchEntity(question)

    text = textWeighter.filterQuestions(question, story[1], SENTENCEWINDOW)
    tokens = nlp(text)
    potentialAnswers = []
    for token in tokens:
        if token.ent_type_ in potentialEntities:
            potentialAnswers.append(token.text)

    if len(potentialAnswers) > 0:
        return ' '.join(set(word for word in potentialAnswers if word not in question.text))

# If all else fails resort
# to finding the most likely sentence and hopefully
# trimming it down
# For sentences like 'The fire hydrant allows
# firefighters to fight fires'
# and questions like 'what does a fire hydrant allow'
# to trim to 'allow firefighters to fight fires'
def trimParse(question, story, requirements=None):
    
    # Get all combinations of the question sentence
    splitQuestion = question.text.split(' ')
    combinations = []
    for i in range(len(splitQuestion)):
        for j in range(i+1, len(splitQuestion)+1):
            string = ' '.join(splitQuestion[i:j])
            if string[-1] in '.?!':
                string = string[:-1]
            combinations.append(string)
    combinations.sort(key=len, reverse=True)

    mostLikelySentences = textWeighter.filterQuestions(question, story[1], ranked=True)
    mostLikelySentence = mostLikelySentences[0]

    if requirements is not None:
        for sentence in mostLikelySentences:
            if any([requirement in sentence for requirement in requirements]):
                mostLikelySentence = sentence
                break

    # Go through all combinations and if that combination
    # is in the mostLikelySentence then split and return either
    # before or after that depending on the contents
    stopwords = fetchStopwords('data/stopwords.txt')
    for combination in combinations:
        # only keep combinations that have a length
        # of SENTENCETRIM without stopwords so we don't
        # have short splits or splits on stopwords
        if combination in mostLikelySentence and \
                len([word for word in combination.split(' ') if word not in stopwords]) > SENTENCETRIM:
            split = mostLikelySentence.split(combination)

            # Words that would cause the answer to come
            # before the explanation
            reverseWords = ['if', 'unless', 'but', 'By']



            if len(split[-1]) > 0 and \
                    not any([word in mostLikelySentence for word in reverseWords]) and \
                    split[-1][0] != "'":
                return split[-1]
            elif 'By' in mostLikelySentence and ',' in mostLikelySentence:
                # For cases like "By doing this, this will happen"
                # only keep the "this will happen"
                return ''.join(mostLikelySentence.split(',')[1:])
            else:
                return split[0]
    
    return mostLikelySentence

# Given a quote question find
# the asker
def findSubject(question):
    if 'According to' in question:
        return findBetween(question, 'According to', ',')
    elif 'according to' in question:
        return findBetween(question, 'according to', '?')

# Find a string between two substrings
def findBetween(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''

# Steps in order
# Split on 'why' questions
# Try and match entities
# Check if it's a quote to get more
# restrictions
# Resort to recalling most likely
# sentence
def classify(question, story, nlp):

    # WHAT: Recall: .5624 | Precision: .3226 | F-Measure: .4100
    # WHAT: Recall: .5624 | Precision: .3226 | F-Measure: .4100
    if question.type == 'What':
        return whatAnswer(question, story, nlp)

    whySplitAnswer = whySplit(question, story)
    if whySplitAnswer and len(whySplitAnswer) > 0:
        return whySplitAnswer

    entityMatchAnswer = entityMatch(question, story, nlp)
    if entityMatchAnswer and len(entityMatchAnswer) > 0:
        return entityMatchAnswer

    if question.type == 'According' and False:
        subject = findSubject(question.text)
        trimParseAnswer = trimParse(question, story, [subject] + ['said', 'say', 'suggested'])
    else:
        trimParseAnswer = trimParse(question, story)

    if trimParseAnswer and len(trimParseAnswer) > 0:
        return trimParseAnswer

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

# Find the potential entity types the answer will
# fit given the question type and subtype
def questionMatchEntity(question):
    if question.type == 'Who':
        if question.subtype == 'simple who':
            return []
        return ['PERSON', 'ORG', 'NORP']
    elif question.type == 'What':
        if question.subtype == 'price':
            return ['MONEY']
        if question.subtype == 'simple what':
            return []
        else:
            return []
    elif question.type == 'When':
        if question.subtype == 'time':
            return ['TIME']
        elif question.subtype == 'date':
            return ['DATE']
        elif question.subtype == 'simple when':
            return ['TIME', 'DATE']
        return ['DATE']
    elif question.type == 'Where':
        if question.subtype == 'organization':
            return ['ORG']
        return ['FAC', 'GPE', 'LOC']
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
            return ['DATE', 'CARDINAL']
        elif question.subtype == 'price':
            return ['MONEY']
        elif question.subtype == 'length':
            return ['QUANTITY']
        elif question.subtype == 'weight':
            return ['QUANTITY']
        return ['PERCENT', 'QUANTITY', 'CARDINAL']
    elif question.type == 'According':
        return []
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