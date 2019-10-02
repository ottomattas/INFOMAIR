# Methods in AI Research
# Team project part 1c
# Maarten San Giorgi, Otto Mättas, David-Paul Niland & Lonnie Bregman

from Levenshtein import distance
import re
import os
import json
import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Class for a training sentence instance
class Instance:
    def __init__(self, sentence, label):
        self.sentence = sentence
        self.label = label

# path to both folders
dataPath = 'C:\\Users\\Maarten\\Documents\\UU master AI\\MAIR'

# Path to the csv file
csvPath = dataPath + '\\restaurantinfo.csv'

# All the keywords we can match against, used to fill the keywordList
keywordsPath = dataPath + '\\keywords.json'

# List of keywords to match, filled later in the code
keywordList = {}

# List of requestable keywords to match, filled later in the code
requestableList = []

requestIndex = {"addr":5,
                "area":2,
                "food":3,
                "phone":4,
                "pricerange":1,
                "postcode":6,
                "signature":0,
                "name":0,
                }

# Possible patterns to match
patternList = {"in the (.*) part of town":["area"],
               "want (.*) food":["price", "food"],
               "a (.*) restaurant":["price", "food"],
               "an (.*) restaurant":["price", "food"],
               "looking for (.*) food":["price", "food"],
               "what about (.*) food":["price", "food"],
               "serve (.*) food":["price", "food"],
               "serving (.*) food":["price", "food"],
               "with (.*) food":["price", "food"],
               "in (.*) area":["area"],
               "a (.*) priced":["price"],
               "give me (.*) food":["price", "food"],
               "(\b.*\b) food":["price", "food"],
               "(\b.*\b) restaurant":["price", "food"],
               "(\b.*\b) priced":["price"]}

# A dictionary to hold the data for known information
information = {"food":None, "price":None, "area":None, "requestables":[]}

# Retrieve the JSON data from the keywords file and add them to the keywordList
def retrieveKeywordsFromJSON():
    
    with open(keywordsPath) as keywordsJSON:
        file = keywordsJSON.read()
    
    keywordData = json.loads(file)
    for foodtype in keywordData["informable"]["food"]:
        keywordList[foodtype] = "food"
    for price in keywordData["informable"]["pricerange"]:
        keywordList[price] = "price"
    for area in keywordData["informable"]["area"]:
        keywordList[area] = "area"
    for requestable in keywordData["requestable"]:
        keywordList[requestable] = "requestables"

# Check if the utterance is some sort of acknowledgement with knowing the dialogAct
def isAcknowledgement(dialogAct):
    if dialogAct == 'ack' or dialogAct == 'affirm' or dialogAct == 'confirm' or dialogAct == 'thankyou':
        return True
    return False

# Match keywords against words (for certain types), using the Levenshtein with a certain threshold.
def keywordMatching(sentence, grade, types, vectorizer, classifier):
    
    words = sentence.split()
    
    for word in words:
        for keyword in keywordList:
            dist = distance(word.lower(), keyword.lower())
            if dist < grade and keywordList[keyword] in types:
                if "requestable" in types:
                    if dist == 0:
                        information[keywordList[keyword]].append(keyword)
                    else:
                        check = input("You said " + word + ". Did you mean " + keyword + "?\n")
                        if isAcknowledgement(getDialogAct(vectorizer, classifier, check)):
                            information[keywordList[keyword]].append(keyword)
                        else:
                            continue
                else:
                    if dist == 0:
                        information[keywordList[keyword]] = keyword
                    else:
                        check = input("You said " + word + ". Did you mean " + keyword + "?\n")
                        if isAcknowledgement(getDialogAct(vectorizer, classifier, check)):
                            information[keywordList[keyword]] = keyword
                        else:
                            continue

# Match patterns against a sentence
def patternMatching(sentence, vectorizer, classifier):
    
    for pattern in patternList:
        search = re.search(pattern.lower(), sentence.lower())
        if search:
            keywordMatching(search.group(1), 3, patternList[pattern], vectorizer, classifier)

# Reads a csv file with all the restaurants in it and selects the fitting restaurants
def readFromCSV():
    
    possibleRestaurants = []
    
    # read the csv file
    with open(csvPath) as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        lineCount = 0
        for line in csv_reader:
            
            # Skip the first line
            if lineCount == 0:
                lineCount += 1
                
            # Add all the restaurants that match on price, area and food
            else:
                if len(line) > 3:
                    if (line[1] == information["price"] and line[2] == information["area"] 
                    and line[3] == information["food"]):
                        possibleRestaurants.append(line)
                lineCount += 1
    
    # Return all the found restaurants as a list
    return possibleRestaurants

# Recursive function that receives a dialog act and removes the information
# between parentheses.
def removeParentheses(dialogAct):
    if dialogAct[-1:] == '(':
        return dialogAct[:-1]
    return removeParentheses(dialogAct[:-1])

# Calculates the weight per dialog act
def getData(path):
    
    dataList = []
    
    # iterate over all folders in the path
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
                    sentence = userData["turns"][turn]["transcription"]
                    
                    # split acts in case one utterance contains two dialog acts
                    multipleActs = dialogAct.split("|")
                    
                    # write dialog act and utterance to the text file
                    for act in multipleActs:
                        act = removeParentheses(act)
                        newInstance = Instance(sentence, act)
                        dataList.append(newInstance)
                        
                    turn += 1
    
    return dataList

# Do a Logistic Regression on the data
def trainLogisticRegression():
    
    # Retrieve the data we need
    dataList = getData(dataPath)
    
    sentences = []
    for item in dataList:
        sentences.append(item.sentence)
        
    values = []
    for item in dataList:
        values.append(item.label)
    
    # Split the data 15 to 85 percent training and test data
    trainingInput, testInput, trainingLabels, testLabels = train_test_split(
                sentences, values, test_size=0.15)
    
    vectorizer = CountVectorizer(min_df=0, lowercase=False)
    vectorizer.fit(trainingInput)
    
    trainingData = vectorizer.transform(trainingInput)
    
    classifier = LogisticRegression()
    
    # Train the data
    classifier.fit(trainingData, trainingLabels)
    
    return vectorizer, classifier

# Returns true if all information is known, else false
def haveAllInformation():
    for element in information:
        if information[element] == None:
            return False
    
    return True

# try matching the keywords for finding a restaurant
def findKeywords(userUtterance, vectorizer, classifier):
    patternMatching(userUtterance, vectorizer, classifier)
    keywordMatching(userUtterance, 1, ["price", "area", "food"], vectorizer, classifier)

# try finding a request
def findRequests(userUtterance, vectorizer, classifier):
    patternMatching(userUtterance, vectorizer, classifier)
    keywordMatching(userUtterance, 1, ["requestable"], vectorizer, classifier)
    
def clearInformation():
    for element in information:
        information[element] = None

def getDialogAct(vectorizer, classifier, utterance):
    inputData = vectorizer.transform({utterance})
    dialogAct = classifier.predict(inputData)[0]
    return dialogAct

def stateTransition():
    state = 'getInfo'
    restCount = 0
    restaurants = []
    
    vectorizer, classifier = trainLogisticRegression()
    
    print("Welcome to the A-team restaurant finder!")
    
    while (state != 'exit'):
        
        # classify the user utterance
        userUtterance = input()
        print("")
        inputData = vectorizer.transform({userUtterance})
        dialogAct = classifier.predict(inputData)[0]
        
        findKeywords(userUtterance, vectorizer, classifier)
        
        # Check if there are already restaurants found and
        # if all the information is gathered
        if len(restaurants) == 0 and haveAllInformation():
            restaurants = readFromCSV()
        
        # you can always exit the dialog with saying goodbye/bye
        if dialogAct == 'bye':
            print("Thanks for using the A-team restaurant finder!")
            return
        
        # you can restart the conversation from scratch
        if dialogAct == 'restart':
            clearInformation()
            print("Okay, we will start over.")
            stateTransition()
            return
        
        elif state == 'getInfo':              
            if information["food"] == None:
                print("What type of food do you want?")
                
            elif information["area"] == None:
                print("What area do you want?")
            
            elif information["price"] == None:
                print("What price do you want?")
                
            else:
                print("Is a " + information["price"] + " " + information["food"] +
                    " restaurant in the " + information["area"] + " part of town "
                    + "what you are looking for?")
                answer = input("")
                print("")
                if isAcknowledgement(getDialogAct(vectorizer, classifier, answer)):                    
                    state = 'firstProposal'
                else:
                    print("please change your preferences.")
        
        if state == 'firstProposal':
            if len(restaurants) > 0:
                restaurant = restaurants[restCount][0]
                print("How about ", restaurant, "?")
                state = 'waitingForRequest'
            else:
                print("I can't find a " + information["price"] + " " + information["food"] +
                    " restaurant in the " + information["area"] + " part of town. \n"
                    + "try changing your preferences.")
                state = 'getInfo'
        
        elif state == 'waitingForRequest':       
            if isAcknowledgement(dialogAct):
                print("Okay. Do you have any (other) requests?")
                answer = input("")
                dialogAct = getDialogAct(vectorizer, classifier, answer)
                print("")
                if dialogAct == 'negate' or dialogAct == 'deny':
                    print("Okay, goodbye!")
                    return
                elif isAcknowledgement(dialogAct):
                    print ("please tell me")
            elif dialogAct == 'reqmore' or dialogAct == 'negate' or dialogAct == 'deny':
                state = 'nextProposal'
            if dialogAct == 'request':
                findRequests(userUtterance, vectorizer, classifier)
                if len(information["requestables"]) == 0:
                    print("I did not understand your request, could you repeat it?")
                else:
                    print(information)
                    for request in information["requestables"]:
                        print(request + ": " + restaurants[restCount][requestIndex[request]])
                
        if state == 'nextProposal':            
            if restCount + 1 < len(restaurants):
                restCount += 1    
                restaurant = restaurants[restCount][0]
                print("OK, how about ", restaurant, "?")
            else:
                print("There are no more " + information["price"] + " " + information["food"] +
                " restaurants in the " + information["area"] + " part of town")
            
            
def main():
    retrieveKeywordsFromJSON()
    
    stateTransition() 

main()
        
        # I left these here for your reference of what dialog acts exist:
        
#        if dialog_act == 'hello':
#        
#        if dialog_act == 'affirm':
#            
#        if dialog_act == 'bye':
#            
#        if dialog_act == 'confirm':
#            
#        if dialog_act == 'deny':
#
#        if dialog_act == 'negate':
#            
#        if dialog_act == 'repeat':
#            
#        if dialog_act == 'reqalts':
#            
#        if dialog_act == 'reqmore':
#
#        if dialog_act == 'request':
#            
#        if dialog_act == 'restart':
#            
#        if dialog_act == 'thankyou':
#            
#        if dialog_act == 'null':
#  
#        if dialog_act == 'ack'
        