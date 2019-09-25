# Methods in AI Research
# Team project part 1b
# Maarten San Giorgi, Otto Mättas, David-Paul Niland & Lonnie Bregman

import os
import random
import string

path = 'C:\\Users\\Marcel Bregman\\.spyder-py3\\keyword files'

# Function that receives an utterance and checks for certain dialog act 
# keywords which it gets from text files. If a keyword is found, it prints 
# the corresponding dialog act.
def baselineKeywords(utterance):
    
    # iterate over keyword files
    for root, dirs, files in os.walk(path):
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

# Function that randomly returns one of the dialog acts with probabilities
# corresponding to how often they appear in the training set.
def baselineDistribution():
    
    # hard coded weights for dialog acts corresponding to how often they appear
    # in the training set
    total = 15611
    ack_weight = (19/total)
    affirm_weight = (555/total) + ack_weight
    bye_weight = (169/total) + affirm_weight
    confirm_weight = (126/total) + bye_weight
    deny_weight = (10/total) + confirm_weight
    hello_weight = (54/total) + deny_weight
    inform_weight = (5970/total) + hello_weight
    negate_weight = (188/total) + inform_weight
    null_weight = (994/total) + negate_weight
    repeat_weight = (25/total) + null_weight
    reqalts_weight = (1100/total) + repeat_weight
    reqmore_weight = (4/total) + reqalts_weight
    request_weight = (4255/total) + reqmore_weight
    restart_weight = (7/total) + request_weight
    thank_weight = (2135/total) + restart_weight
    
    # random number between 0 and 1
    r = random.uniform(0, 1)
    
    # return the dialog act the random number corresponds to
    if r <= ack_weight:
        return 'ack'
    if r <= affirm_weight:
        return 'affirm'
    if r <= bye_weight:
        return 'bye'
    if r <= confirm_weight:
        return 'confirm'
    if r <= deny_weight:
        return 'deny'
    if r <= hello_weight:
        return 'hello'
    if r <= inform_weight:
        return 'inform'
    if r <= negate_weight:
        return 'negate'
    if r <= null_weight:
        return 'null'
    if r <= repeat_weight:
        return 'repeat'
    if r <= reqalts_weight:
        return 'reqalts'
    if r <= reqmore_weight:
        return 'reqmore'
    if r <= request_weight:
        return 'request'
    if r <= restart_weight:
        return 'restart'
    if r <= thank_weight:
        return 'thank'
    
    return 0
    

def main():
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