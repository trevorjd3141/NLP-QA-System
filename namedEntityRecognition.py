import sys
import spacy
import os

def getStoryFilenames(directory):
    filenames = []
    for entry in os.scandir(directory):
        if entry.path.endswith(".story"):
            filenames.append(entry.path)
    return filenames

def getStoryTexts(filenames):
    texts = []
    for filename in filenames:
        file = open(filename, 'r')
        texts.append([line.strip() + ' ' for line in file.readlines()])
    return texts

def groupStoryInfo(texts):
    groupedStories = []
    
    for text in texts:
        storyID = ""
        storyText = ""
        for line in text:
            if line.startswith('STORYID:'):
                storyID = line.split()[1]
            elif not line.startswith(('TEXT', 'DATE', 'HEADLINE')) and len(line) > 0:
                storyText += line
        groupedStories.append([storyID, storyText])
    return groupedStories

def NER(info, nlp):
    text = info[1]
    tokens = nlp(text)
    return [info[0], tokens]

def getNamedEntities(directory):
    storyFilenames = getStoryFilenames(directory)
    storyTexts = getStoryTexts(storyFilenames)
    groupedStories = groupStoryInfo(storyTexts)

    # Each token fits this form (storyID, Token for the text)
    nlp = spacy.load("en_core_web_sm") 
    stories = [NER(story, nlp) for story in groupedStories]
    return stories