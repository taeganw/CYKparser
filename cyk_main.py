def check_single_productions(letter,productions):
    results = []
    for item in productions:
        for produces in item['Produces']: #check the input letter and if it exsits as a production, add it as a result
            if letter == produces:
                results.append(item ['State'])
    if results != []:
        return results
    else:
        return None


def cross_first_productions(productions,previousProductions):
    currentItem = 0 # increment for the production for loops
    allcombinations = [] #stores all of the combinations for the round of checks
    sizeOfPrevProductions = len(previousProductions)
    
    for elements in previousProductions: # grabs the number of elements in the previous productions
        combination = [] # stores all of the combinations of the current and next results
        if elements['result'] != None: #if the current item in the productions list is not None or decleared empty
            for number in range(len(elements['result'])): #increment through the productions in the results data
                if currentItem + 1 != sizeOfPrevProductions: #if the current item is not the last item in the list
                    if previousProductions[currentItem+1]['result'] != None: # if the next production is not empty
                        
                        for elements2 in range(len(previousProductions[currentItem+1]['result'])): # for every result in the next production, cross the current values with the next
                            combination.append(previousProductions[currentItem]['result'][number] + previousProductions[currentItem+1]['result'][elements2]) #adds criss-crossed results to combination list
        allcombinations.append(combination)
        currentItem +=1     
    
    newlist = []
    listOfProductions = []
    for combination in allcombinations: # for each combination
        if combination != []: # if the combination is empty append an empty result 
            for item in range(len(combination)): # if the combination is exist, check it against production rules
                for production in productions:
                    for produces in production['Produces']:
                        if produces == combination[item]: #if the combination exist as a production result, append it to the production list
                            listOfProductions.append(production['State'])
            newlist.append({'value':combination ,'result' :listOfProductions}) # append productions to the return function
            listOfProductions = [] #reset inital production list
    print('-------------------------------------------------------')
    print(newlist) # the results of the crossing of the single productions, 2nd row of the pyramid
    print('-------------------------------------------------------')
    return newlist

def recursive_cross_productions(productions,previousProductions,length):
    combination = []
    allcombinations = []
    currentItem = 0
    sizeOfPrevProductions = len(previousProductions[length])
    for elements in previousProductions[length]: # grabs the number of elements in the previous productions
        combination = [] # stores all of the combinations of the current and next results
        if elements['result'] != None: #if the current item in the productions list is not None or decleared empty
                if currentItem + 1 != sizeOfPrevProductions: # checks to make sure the next item is not outside the bounds
                    for rows in range(length+1): #counts the number of rows currently accessible in the cyk pyramid, the extra one accounts for the inital single case
                        if previousProductions[rows][currentItem]['result'] != None: # checks to make sure the previous productions results were not None
                            for number in range(len(previousProductions[rows][currentItem]['result'])): #increment through the productions in the results data
                                if previousProductions[length-rows][currentItem+rows+1]['result'] != None:
                                    for elements2 in range(len(previousProductions[length-rows][currentItem+rows+1]['result'])): # for every result in the next production, cross the current values with the next
                                        combination.append(previousProductions[rows][currentItem]['result'][number] + previousProductions[length-rows][currentItem+rows+1]['result'][elements2])
                if combination != []: #if the combination is empty, do not append it, catches an empty case at the end of each string
                    allcombinations.append(combination)
                currentItem +=1  
    newlist = [] #list to hold the results of the cross productions
    listOfProductions = [] #temporary list to hold all results from a cross production
    for combination in allcombinations: # for each combination
        if combination != []: # if the combination is not empty
            for item in range(len(combination)): #for each combination in the row, check to see if there exsits a production for it
                for production in productions:
                    for produces in production['Produces']:
                        if produces == combination[item]: #if the combination exist as a production result, append it to the production list
                            listOfProductions.append(production['State'])
            newlist.append({'value':combination ,'result' :listOfProductions}) # append productions to the return function
            listOfProductions = [] #reset inital production list
    print('-------------------------')
    print (newlist)
    return newlist # return the new row of the pyramid. row contains the resulting cross productions to be used recursivley

def start(string,productions):
    # First round of parsing for bottom of the tree
    singleProductions = []
    for letter in string:
        singleProductions.append({"result":None, "value":letter})
    for item in singleProductions:
        item['result'] = check_single_productions(item['value'],productions) # if the productions exists for the single instance of a letter, add it as a value
    print ('-------------------------------------------------------')
    print (singleProductions)
    print ('-------------------------------------------------------')
    allProductions=[]
    previousProductions = singleProductions
    allProductions.append(previousProductions)
    length = len(singleProductions) - 2 #number of rows in the pyramid working down -1 row
    if length != -1: # checks to make sure that the string is more than 1 character long
        previousProductions = cross_first_productions(productions,previousProductions) # use previous production results as the productions 
        allProductions.append(previousProductions) 
        for x in range(length): #length is the total number of rows needed given by the length of the string
            previousProductions = recursive_cross_productions(productions,allProductions,x+1) #passes the production list, all of the previous cross production results, and the number of rows accessible within the pyramid
            allProductions.append(previousProductions) #append the results and continue until only one element exsits
    try: # the try statement catches any extreme cases that do not exist in the grammar
        print(allProductions)
        if allProductions[-1] == [] or allProductions[0][-1]['result'] == [] or allProductions[0][-1]['result'] == None : #if the root of the pyramid is empty or None the grammar does not exist
            print("******The string is not in the grammar******")
        else:
            print("******The string is in the grammar******") 
    except:
        print("***except***The string is not in the grammar******")
    return 0




# Open the grammar file and read the rules from the file
try:
    f = open("grammar.txt", "r")
except:
    print("----- Could not find the grammar.txt file -----")


# Parse a rule and store states and productions into a list
productions = []
x = 0
for items in f:
    if '#' not in items:
        print("Line: " + str(x) + " - "+ items) # parse the line by removing null characters and splitting the State from the production
        newlist = items.strip('\n').split("->")
        produces = newlist[1].replace(" ","").split('|') # split the productions into list items and remove spaces
        productions.append({"State":newlist[0].strip(), "Produces":produces})
        x += 1

# Print the grammar used for parsing the sentence
print (productions)

#enter string to be checked against the grammar
string = input("Please input your string to be checked against the grammar: ")

#input the strings and productions into the start function
start(string,productions)
