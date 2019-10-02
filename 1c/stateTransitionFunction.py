def main():
    print("Hello can I help you")
    dialogue_state = 'welcome'
    
    type = 'None'
    area = 'None'
    price = 'None'
    restaurant = 'None'
    
    
    while (dialogue_state != 'exit'):
        
        user_utterance = input()
        inputData = vectorizer.transform({user_utterance})
        dialog_act = classifier.predict(inputData)[0]
        
        if type == 'None':
            type = getType
            
        elif area == 'None':
            area = getArea
        
        elif price == 'None':
            price = getPrice
            
        else:
            proposeRestaurant
        
        
        
        
        
        

        
        if dialog_act == 'inform':
            # Maarten
        if dialog_act == 'hello':
        
        if dialog_act == 'affirm':
            
        if dialog_act == 'bye':
            
        if dialog_act == 'confirm':
            
        if dialog_act == 'deny':

        if dialog_act == 'negate':
            
        if dialog_act == 'repeat':
            
        if dialog_act == 'reqalts':
            
        if dialog_act == 'reqmore':

        if dialog_act == 'request':
            
        if dialog_act == 'restart':
            
        if dialog_act == 'thankyou':
            
        if dialog_act == 'null':
  
        if dialog_act == 'ack'
        
        
def getType():
    print("What type of food do you want?")
    type = # Maarten
    return type

def getArea():
    print("What area do you want?")
    type = # Maarten
    return area
    
def getPrice():
    print("What price do you want?")
    type = # Maarten
    return price

def proposeRestaurant(type, area, price):
    
    # csv code
    
    return proposal

def getPostCode(restaurant):
    return postCode

def getNumber(restaurant):
    return number

def getAddress(restaurant):
    return address
        

        