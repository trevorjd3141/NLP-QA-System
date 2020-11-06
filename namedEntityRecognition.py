import sys
import spacy
import os

def getStoryFilenames():
    cwd = os.getcwd()
    filenames = []
    for entry in os.scandir(cwd+'\\data'):
        if entry.path.endswith(".story"):
            filenames.append(entry.path)
    return filenames

def getStoryTexts(filenames):
    texts = []
    for filename in filenames:
        file = open(filename, 'r')
        texts.append([line.strip() for line in file.readlines()])
    return texts

# given
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

def getNamedEntities():
    storyFilenames = getStoryFilenames()
    storyTexts = getStoryTexts(storyFilenames)
    groupedStories = groupStoryInfo(storyTexts)

    # Each token fits this form (storyID, Token for the text)
    nlp = spacy.load("en_core_web_sm") 
    tokens = [NER(story, nlp) for story in groupedStories]
    return tokens

if __name__ == '__main__':
    getNamedEntities()