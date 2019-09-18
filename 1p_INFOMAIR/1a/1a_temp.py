# Methods in AI Research
# Team project part 1a
# Maarten San Giorgi, Otto Mättas, David-Paul Niland & Lonnie Bregman

import json
import os

# Function that shows a dialog and when the Enter button is pressed shows the next one.
def showDialogs():
    
    # iterate over all folders in current directory
    path = os.getcwd()
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            currentDir = os.path.join(root, directory)
            
            # if folder contains log.json and label.json files
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
                
                # print session id and task information
                print("session-id:", systemData["session-id"])
                print(userData["task-information"]["goal"]["text"], "\n")
                
                # print dialog
                turn = 0
                numberOfTurns = len(systemData["turns"])
                while turn < numberOfTurns:
                    print("system: ", systemData["turns"][turn]["output"]["transcript"])
                    print("user: ", userData["turns"][turn]["transcription"])
                    turn += 1
                
                # wait for Enter button
                input()
        
        
# Function that writes all dialogs into one text file.
def writeDialogsToFile():
    
    # initialize text file
    file = open("allDialogs.txt", "w")
    
    # iterate over all folders in current directory
    path = os.getcwd()
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            currentdir = os.path.join(root, directory)
            
            # if folder contains log.json and label.json files
            if 'log.json' in os.listdir(currentdir):
                
                # read log file
                with open(currentdir + '/log.json', 'r') as myfile:
                    log = myfile.read()
                
                # read label file
                with open(currentdir + '/label.json', 'r') as myfile:
                    label = myfile.read()
                    
                # parse files
                systemData = json.loads(log)
                userData = json.loads(label)
                
                # write session id and task information to the text file
                file.write("session-id:")
                file.write(systemData["session-id"])
                file.write("\n")
                file.write(userData["task-information"]["goal"]["text"])
                file.write("\n")
                
                # write dialog to the text file
                turn = 0
                numberOfTurns = len(systemData["turns"])
                while turn < numberOfTurns:
                    file.write("\nsystem: ")
                    file.write(systemData["turns"][turn]["output"]["transcript"])
                    file.write("\nuser: ")
                    file.write(userData["turns"][turn]["transcription"])
                    turn += 1
                file.write("\n\n\n")
                    
showDialogs()
writeDialogsToFile()