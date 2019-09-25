# Methods in AI Research
# Team project part 1b
# Maarten San Giorgi, Otto Mättas, David-Paul Niland & Lonnie Bregman

import os
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np

# If not installed, command 'pip install keras' 
# and 'pip install tensorflow'in console
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

# Class for 
class Instance:
    def __init__(self, sentence, label):
        self.sentence = sentence
        self.label = label
    

# path to the folder with the training data
trainingDataPath = 'C:\\Users\\Maarten\\Documents\\UU master AI\\MAIR\\dstc2_traindev'

# path to the folder with the test data
testDataPath = 'C:\\Users\\Maarten\\Documents\\UU master AI\\MAIR\\dstc2_test'

# path to both folders
dataPath = 'C:\\Users\\Maarten\\Documents\\UU master AI\\MAIR'

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
def doLogisticRegression():
    
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
    testData = vectorizer.transform(testInput)
    
    classifier = LogisticRegression()
    
    # Train the data
    classifier.fit(trainingData, trainingLabels)
    
    # Test the data
    score = classifier.score(testData, testLabels)
    print("accuracy of Logistic Regression: ")
    print(score)
    
    # Test the data with user input
    input_sentence = input("Type utterance (type 'exit' to exit): ").lower() # lowercase
    inputData = vectorizer.transform({input_sentence})
    print(classifier.predict(inputData)[0])

# Do a neurel network on the data
def doNeuralNetwork():
    
    # Retrieve the data we need
    dataList = getData(dataPath)
    
    sentences = []
    for item in dataList:
        sentences.append(item.sentence)
        
    values = []
    for item in dataList:
        values.append(item.label)
        
    # Split the data into test and training data (85 to 15 percent)
    trainingInput, testInput, trainingLabels, testLabels = train_test_split(
                sentences, values, test_size=0.15)
    
    vectorizer = CountVectorizer(min_df=0, lowercase=False)
    vectorizer.fit(trainingInput)
    
    trainingData = vectorizer.transform(trainingInput)
    testData = vectorizer.transform(testInput)
    
    # Create a training model
    input_dim = trainingData.shape[1]
    model = Sequential()
    model.add(layers.Dense(10, input_dim=input_dim, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    
    # Compile the training model
    model.compile(loss='binary_crossentropy', 
                  optimizer='rmsprop', 
                  metrics=['accuracy'])
    
    print(model.summary())
    
    # Train the data
    model.fit(trainingData, trainingLabels,
                  epochs=20,
                  batch_size=128)
    
    # Test the data
    loss, accuracy = model.evaluate(testData, testLabels, verbose=False)
    print("accuracy of Neural Networking: ")
    print(accuracy)
    
    # Test the data with user input
    input_sentence = input("Type utterance (type 'exit' to exit): ").lower() # lowercase
    inputData = vectorizer.transform({input_sentence})
    print(model.predict(inputData)[0])
    
def main():
    
    doLogisticRegression()
    doNeuralNetwork()
    
main()