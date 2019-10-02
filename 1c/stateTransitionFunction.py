# Methods in AI Research
# Team project part 1c
# Maarten San Giorgi, Otto Mättas, David-Paul Niland & Lonnie Bregman

def stateTransition():
    foodType = 'None'
    area = 'None'
    price = 'None'
    restaurant = 'None'
    state = 'getInfo'
    
    print("Welcome! How can I help you?")
    
    while (state != 'exit'):
        
        # classify the user utterance
        userUtterance = input()
        inputData = vectorizer.transform({userUtterance})
        dialogAct = classifier.predict(inputData)[0]
        
        # you can always exit the dialog with saying goodbye
        if dialogAct == 'bye':
            state = 'exit'
        
        elif state == 'getInfo':
            if dialogAct == 'inform':
                # extract type and/or area and/or price from utterance
                
            if foodType == 'None':
                print("What type of food do you want?")
                
            elif area == 'None':
                print("What area do you want?")
            
            elif price == 'None':
                print("What price do you want?")
                
            else:
                state = 'firstProposal'
            
        
        elif state == 'firstProposal':
            restaurant = # pick a restaurant from the CSV file
            print("How about ", restaurant, "?")
            state = 'nextProposal'
            
        elif state == 'nextProposal':
            if dialogAct == 'confirm':
                print("Thank you. Goodbye!")
                state = 'exit'
                
            elif dialogAct == 'deny' or dialogAct == 'negate' or dialogAct == 'reqmore':
                restaurant = # pick a different restaurant from the CSV file
                print("OK, how about ", restaurant, "?")
            
            
            
            
stateTransition()          
        
        
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
        