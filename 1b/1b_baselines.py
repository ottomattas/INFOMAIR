# Methods in AI Research
# Team project part 1b
# Maarten San Giorgi, Otto Mättas, David-Paul Niland & Lonnie Bregman

import os
import random
import string
import json

# path to the folder with the files with the keywords
keywordPath = 'C:\\Users\\Maarten\\Documents\\UU master AI\\MAIR\\GIT project MAIR\\baseline_rules'

# path to the folder with the training data
trainingDataPath = 'C:\\Users\\Maarten\\Documents\\UU master AI\\MAIR\\dstc2_traindev'

# dictionary for the weight for each dialog act
weightDictionary = {
        "ack" : 0,
        "affirm" : 0,
        "bye" : 0,
        "confirm" : 0,
        "deny" : 0,
        "hello" : 0,
        "inform" : 0,
        "negate" : 0,
        "null" : 0,
        "repeat" : 0,
        "reqalts" : 0,
        "reqmore" : 0,
        "request" : 0,
        "restart" : 0,
        "thankyou" : 0
}

# Recursive function that receives a dialog act and removes the information
# between parentheses.
def removeParentheses(dialogAct):
    if dialogAct[-1:] == '(':
        return dialogAct[:-1]
    return removeParentheses(dialogAct[:-1])

# Function that receives an utterance and checks for certain dialog act 
# keywords which it gets from text files. If a keyword is found, it prints 
# the corresponding dialog act.
def baselineKeywords(utterance):
    
    # iterate over keyword files
    for root, dirs, files in os.walk(keywordPath):
        for file in files:
            currentFile = os.path.join(root, file)
            
            # read text file containing keywords
            with open(currentFile) as myFile:
                keywords = myFile.readlines()
            
            # iterate over keywords
            for keyword in keywords:
                keyword = keyword.rstrip() # remove \n at the end
                keyword = ' ' + keyword + ' ' # adding a space at start and end to only get seperate words
                
                # if a keyword is found, print the corresponding dialog act
                if keyword in utterance:
                    print(file)
                    return 1
                
    return 0 # if none of the keywords is found

# Calculates the weight per dialog act
def getDialogActWeights():
    
    # iterate over all folders in the path
    for root, dirs, files in os.walk(trainingDataPath):
        for directory in dirs:
            currentDir = os.path.join(root, directory)
            
            # if folder with log.json and label.json files is reached
            if 'log.json' in os.listdir(currentDir):
                
                # read log file
                with open(currentDir + '/log.json', 'r') as myfile:
                    log = myfile.read()
                
                # read label file
                with open(currentDir + '/label.json', 'r') as myfile:
                    label = myfile.read()
                    
                # parse files
                systemData = json.loads(log)
                userData = json.loads(label)
                
                # iterate over all turns in the dialog
                turn = 0
                numberOfTurns = len(systemData["turns"])
                while turn < numberOfTurns:
                    dialogAct = userData["turns"][turn]["semantics"]["cam"]
                    
                    # split acts in case one utterance contains two dialog acts
                    multipleActs = dialogAct.split("|")
                    
                    # write dialog act and utterance to the text file
                    for act in multipleActs:
                        act = removeParentheses(act)
                        if act in weightDictionary:
                            
                            # Add 1 up to the act
                            weightDictionary[act] += 1
                        
                    turn += 1
    
    # Calculate the total of counted dialog acts
    total = 0
    for count in weightDictionary.values():
        total += count
    
    # Convert the each dialog act to a number between 0 and 1 
    # by dividing by the total number of dialog acts
    previous = 0
    for act, count in weightDictionary.items():
        weight = count / total + previous
        weightDictionary[act] = weight
        previous = weight

# Function that randomly returns one of the dialog acts with probabilities
# corresponding to how often they appear in the training set.
def baselineDistribution():
    
    # random number between 0 and 1
    r = random.uniform(0, 1)
    
    # return the dialog act the random number corresponds to
    for act, weight in weightDictionary.items():
        if r <= weight:
            return act
        
    return 0
    

def main():
    
    getDialogActWeights()
    
    stop = 0
    
    while stop == 0:
        utterance = input("Type utterance (type 'exit' to exit): ").lower() # lowercase
        
        # removing punctuation
        for c in (string.punctuation):
            utterance = utterance.replace(c, "")
       
        if utterance == 'exit':
            stop = 1
        
        if stop == 0:
            utterance = ' ' + utterance + ' ' # adding a space at start and end
            
            if not baselineKeywords(utterance):
                print(baselineDistribution())
    
main()