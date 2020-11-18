import sys
import os

# Grab the names of all story filetypes
def getStoryFilenames(directory):
    filenames = []
    for entry in os.scandir(directory):
        if entry.path.endswith(".story"):
            filenames.append(entry.path)
    return filenames

# For each story file name map that stories
# text to a list
def getStoryTexts(filenames):
    texts = []
    for filename in filenames:
        file = open(filename, 'r')
        texts.append([line.strip() + ' ' for line in file.readlines()])
    return texts

# Separate the storyID and the actual text
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

def getNamedEntities(directory):
    storyFilenames = getStoryFilenames(directory)
    storyTexts = getStoryTexts(storyFilenames)
    stories = groupStoryInfo(storyTexts)

    # Each story fits this form
    # (storyID, text)
    return stories