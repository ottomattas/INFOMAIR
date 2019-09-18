# Methods in AI Research
# Team project part 1b
# Maarten San Giorgi, Otto Mättas, David-Paul Niland & Lonnie Bregman

import json
import os

# comment?
path = 'C:\\Users\\Marcel Bregman\\.spyder-py3\\dstc2_training'

# Function that receives a dialog act and removes the information between
# parentheses.
def removeParentheses(dialogAct):
    result = ""
    for c in dialogAct:
        if c == '(':
            return result
        else:
            result += c
    return result

# Function that makes a text file containing all user utterances of the
# trainig set dialogs preceded by the corresponding dialog act.
def dialogActsToFile():
    
    # initialize text file
    file = open("allDialogActs.txt", "w")
    
    # iterate over all folders in the path (?)
    for root, dirs, files in os.walk(path):
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
                        file.write(removeParentheses(act))
                        file.write(" ")
                        
                        # convert utterance to lower case
                        utterance = userData["turns"][turn]["transcription"].lower()
                        
                        file.write(utterance)
                        file.write("\n")
                        
                    turn += 1


dialogActsToFile()