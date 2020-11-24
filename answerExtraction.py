import textWeighter
import qa

def answer(question, story, nlp):
    mostLikelySentences = textWeighter.filterQuestions(question, story[1], ranked=True)
    mostLikelySentence = rootStrictLemma(question, mostLikelySentences, nlp)
    return mostLikelySentence

def rootStrictLemma(question, mostLikelySentences, nlp):
    mostLikelySentence = mostLikelySentences[0]
    qDoc = nlp(question.text)
    qDeps = [0,0,0,0]
    for token in qDoc:
        if token.dep_ == 'ROOT':
            qRootLemma = token.lemma
            qDeps[0] = qRootLemma
        elif token.dep_ == 'dobj':
            qDeps[1] = token.lemma
        elif token.dep_ == 'nsubj':
            qDeps[2] = token.lemma
        elif token.dep_ == 'pobj':
            qDeps[3] = token.lemma
    sent = getMostLikely(qDeps, mostLikelySentences, nlp)[0]
    doc = nlp(sent)
    return entityMatcher(sent, doc, question)

def getMostLikely(qDeps, mostLikely, nlp):
    for dependency in qDeps:
        potential = []
        if dependency != 0:
            potential = lemmaCheck(dependency, mostLikely, nlp)
            if len(potential) != 0:
                mostLikely = potential.copy()
    return mostLikely

def lemmaCheck(qDep, sentences, nlp):
    p = []
    for sent in sentences:
        doc = nlp(sent)
        for token in doc:
            if token.lemma == qDep:
                p.append(sent)
    return p

def stopParse(question, mostLikelySentences, nlp):

    questionTokens = removeStops(question.text, nlp)

    bestSent = mostLikelySentences[0]
    bestSentTokens =[]
    score = 0
    for sent in mostLikelySentences:
        sentTokens = removeStops(sent, nlp)
        potScore = 0
        potSentTokens = []
        for qToken in questionTokens:
            for sToken in sentTokens:
                if qToken.similarity(sToken) > 0.5:
                    potScore += 1
                else:
                    potSentTokens.append(sToken)
        if potScore > score or (potScore == score and len(potSentTokens) > len(bestSentTokens)):
            score = potScore
            bestSentTokens = potSentTokens
            bestSent = sent

    return entityMatcher(bestSent, bestSentTokens, question)

def removeStops(sentence, nlp):
    doc = nlp(sentence)
    tokens = [token for token in doc if not token.is_stop]
    return tokens

def entityMatcher(sent, sentTokens, question):
    potentialEntities = qa.questionMatchEntity(question)
    potentialAnswers = []
    for token in sentTokens:
        if token.ent_type_ in potentialEntities:
            potentialAnswers.append(token.text)

    if len(potentialAnswers) > 0:
        return ' '.join(set(word for word in potentialAnswers if word not in question.text))
    else:
        return sent
