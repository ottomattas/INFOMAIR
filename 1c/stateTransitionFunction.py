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

# Class for 
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
               "(\b.*\b) restaurant":["price", "food"]}

# A dictionary to hold the data for known information
information = {"food":None, "price":None, "area":None}

# List of possible recommandable restaurants
restaurants = []

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

# Match keywords against words (for certain types), using the Levenshtein with a certain threshold.
def keywordMatching(sentence, grade, types):
    
    words = sentence.split()
    
    for word in words:
        for keyword in keywordList:
            dist = distance(word.lower(), keyword.lower())
            if dist < grade and keywordList[keyword] in types:
                if dist == 0:
                    information[keywordList[keyword]] = keyword
                else:
                    check = input("You said " + word + ". Did you mean " + keyword + "?(yes/no)\n")
                    if (check == "yes"):
                        information[keywordList[keyword]] = keyword
                    else:
                        continue

# Match patterns against a sentence
def patternMatching(sentence):
    
    for pattern in patternList:
        search = re.search(pattern.lower(), sentence.lower())
        if search:
            keywordMatching(search.group(1), 3, patternList[pattern])

# Reads a csv file with all the restaurants in it and selects the fitting restaurants
def readFromCSV(pricerange, area, food):
    
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
                    if line[1] == pricerange and line[2] == area and line[3] == food:
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

def stateTransition():
    state = 'getInfo'
    restCount = 0
    restaurants = []
    
    vectorizer, classifier = trainLogisticRegression()
    
    print("Welcome! How can I help you?")
    
    while (state != 'exit'):
        
        # classify the user utterance
        userUtterance = input()
        inputData = vectorizer.transform({userUtterance})
        dialogAct = classifier.predict(inputData)[0]
        
        # Check if there are already restaurants found and
        # if all the information is gathered
        if len(restaurants) == 0 and haveAllInformation():
            restaurants = readFromCSV()
        
        # you can always exit the dialog with saying goodbye
        if dialogAct == 'bye':
            state = 'exit'
        
        elif state == 'getInfo':
            if dialogAct == 'inform':
                patternMatching(userUtterance)
                keywordMatching(userUtterance, 1, ["price", "area", "food"])
                
            if information["food"] == None:
                print("What type of food do you want?")
                
            elif information["area"] == None:
                print("What area do you want?")
            
            elif information["price"] == None:
                print("What price do you want?")
                
            else:
                state = 'firstProposal'
            
        
        elif state == 'firstProposal':
            restaurant = restaurants[restCount]
            print("How about ", restaurant, "?")
            state = 'nextProposal'
            
        elif state == 'nextProposal':
            if dialogAct == 'confirm':
                print("Thank you. Goodbye!")
                state = 'exit'
                
            elif dialogAct == 'deny' or dialogAct == 'negate' or dialogAct == 'reqmore':
                if restCount + 1 < len(restaurants):
                    restCount += 1    
                    restaurant = restaurants[restCount]
                print("OK, how about ", restaurant, "?")
            
            
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
        