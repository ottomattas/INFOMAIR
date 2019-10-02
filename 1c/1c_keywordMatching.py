# Methods in AI Research
# Team project part 1c - Keyword matching algorithm
# Maarten San Giorgi, Otto Mättas, David-Paul Niland & Lonnie Bregman

from Levenshtein import distance
import re
import json

# All the keywords we can match against, used to fill the keywordList
keywordsPath = 'C:\\Users\\Maarten\\Documents\\UU master AI\\MAIR\\keywords.json'

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

# Returns true if all information is known, else false
def haveAllInformation():
    for element in information:
        if information[element] == None:
            return False

    return True

# Returns all the information we still need
def getNeededInformation():
    result = ""
    for element in information:
        if information[element] == None:
            result += element + " and "

    if result.endswith(" and "):
        result = result[:-5]

    return result

# main function
def main():

    retrieveKeywordsFromJSON()

    while not haveAllInformation():
            test = input("random input sentence (type 'exit' to quit): ")
            if test == "exit":
                break
            patternMatching(test)
            keywordMatching(test, 1, ["price", "area", "food"])
            print ("give me more information about " + getNeededInformation())

    print(information)

main()
#patternMatching("in the east part of town")
