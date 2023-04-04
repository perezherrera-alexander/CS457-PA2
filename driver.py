# Author: Alexander Perez-Herrera
# Date: 03/31/23
# Name: driver.py
# Purpose: Simulate an enviroment like the sqlite3 command line interface. This iteration of the program far further functionality than the previous iteration.
import sys
import os.path
import re

workingPath = os.getcwd()
useCheck = False

# Return 0 if successful, 1 if not

def main():
    if len(sys.argv) == 1:
        print("Running in interactive mode")
    elif len(sys.argv) == 2:
        print("Running in script mode")
        if(os.path.isfile(sys.argv[1])):
            print("Script file exists")
        else:
            print("Script file does not exist")
            return 1

    if len(sys.argv) == 1:
        while(True):
            inputString = input("sqlite> ")
            inputTokens = inputString.split()
            
            if inputTokens[0][0] == ".": # if the first token starts with a period, it's probably the .EXIT command
                inputTokens[0] = inputTokens[0].lower()
            elif inputTokens[-1][-1] != ";": # If the last token doesn't in a semicolon, continue getting input
                while inputTokens[-1][-1] != ";":
                    inputString = input("...> ")
                    inputTokens.extend(inputString.split())
                inputTokens[-1] = inputTokens[-1][:-1] # remove the semicolon from the last token
            else: # If the string initially ends in a semicolon, remove it
                inputTokens[-1] = inputTokens[-1][:-1]
            
            #print(inputTokens)
            recognizeInput(inputTokens)

def recognizeInput(inputTokens):
    command = inputTokens[0]
    if command == ".exit":
        print("All done.")
        quit()
    elif command == "CREATE" or command == "create":
        if(len(inputTokens) >= 3):
            createCommand(inputTokens)
        else:
            print("Error: Invalid syntax. Please try again.")
            return 1
    elif command == "DROP" or command == "drop":
        if(len(inputTokens) == 3):
            dropCommand(inputTokens)
            
        else:
            print("Error: Invalid syntax. Please try again.")
            return 1
    elif command == "SELECT" or command == "select":
        if(len(inputTokens) >= 4):
            selectCommand(inputTokens)
    elif command == "USE" or command == "use":
        if(len(inputTokens) == 2):
            #print("Use command")
            useCommand(inputTokens)
        else:
            print("Error: Invalid syntax. Please try again.")
            return 1
    elif command == "INSERT" or command == "insert":
        if(len(inputTokens) >= 4):
            insertCommand(inputTokens)
    elif command == "UPDATE" or command == "update":
        updateCommand(inputTokens)
    elif command == "DELETE" or command == "delete":
        deleteCommand(inputTokens)
    else:
        print("Errror: Invalid command. Please try again.\n")
    return 0


def createCommand(inputTokens):
    if inputTokens[1] == "DATABASE":
        initializeDatabase(inputTokens)
    elif inputTokens[1] == "TABLE":
        initializeTable(inputTokens)
    else:
        print("Error: Invalid syntax. Please try again.")
        return 1
    return 0

def initializeDatabase(inputTokens):
    global workingPath
    if(os.path.isdir(workingPath + "/" + inputTokens[2])):
        print("!Failed to create database {0} because it already exists.".format(inputTokens[2]))
        return 1
    os.mkdir(workingPath + "/" + inputTokens[2])
    print("Database {0} created.".format(inputTokens[2]))
    return 0

def initializeTable(inputTokens):
    global workingPath
    global useCheck
    tableParameters = []
    #print("Initialize table")
    if(useCheck == False): # If no database is in use, return an error
        print("Error: No database in use. Please try again.")
        return 1
    if(os.path.isfile(workingPath + "/" + inputTokens[2])): # If the table already exists, return an error
        print("!Failed to create table {0} because it already exists.".format(inputTokens[2]))
        return 1
    else: # If the table does not exist, create it
        tableFile = open((workingPath + "/" + inputTokens[2]), 'w')
        print("Table {0} created.".format(inputTokens[2]))
    #Copy the table parameters into a list
    for i in range(3, len(inputTokens)):
        tableParameters.append(inputTokens[i])
    #print(tableParameters)
    #Remove the parentheses from the first and last elements
    tableParameters[0] = tableParameters[0][1:]
    tableParameters[-1] = tableParameters[-1][:-1]
    #print(tableParameters)
    # Remove the commas from the middle elements
    for i in range(0, len(tableParameters) - 2):
        if(tableParameters[i][-1] == ","):
            tableParameters[i] = tableParameters[i][:-1]
    #print(tableParameters)
    # Add spaces between the elements
    for i in range(0, len(tableParameters)):
        tableParameters[i] = tableParameters[i] + " "
    #print(tableParameters)
    # Add | symbols between every other element
    for i in range(1, len(tableParameters) - 1, 2):
        tableParameters[i] = tableParameters[i] + "|" + " "
    #print(tableParameters)
    tableFile.writelines(tableParameters)
    tableFile.close()
    return 0

def dropCommand(inputTokens):
    print("Functionality not yet implemented.")
    #if inputTokens[1] == "DATABASE":
        #os.rmdir(workingPath + "/" + inputTokens[2])
    return 1

def useCommand(inputTokens):
    global workingPath
    global useCheck
    #print(workingPath + "/" + inputTokens[1])
    #print(os.path.isdir(workingPath + "/" + inputTokens[1]))
    if(os.path.isdir(workingPath + "/" + inputTokens[1])):
        workingPath = workingPath + "/" + inputTokens[1]
        useCheck = True
        print("Using database {0}.".format(inputTokens[1]))
    else:
        print("Database {0} does not exist.".format(inputTokens[1]))
        return 1
    return 0

def selectCommand(inputTokens):
    #print("Select command")
    selectParam = []
    fromIndex = 0
    for i in range(0, len(inputTokens)):
        if(inputTokens[i] == "from"):
            fromIndex = i
            for j in range(1, i):
                selectParam.append(inputTokens[j])
    tableName = inputTokens[fromIndex + 1]
    #print(selectParam)
    #print(fromIndex)
    if(selectParam[0] == "*"): # print all columns
        if(os.path.isfile(workingPath + "/" + tableName)):
            tableFile = open(workingPath + "/" + tableName, 'r')
            print(tableFile.read())
    else: # print specific columns
        print("Functionality not yet implemented.")

        

    return 0

def insertCommand(inputTokens):
    global workingPath
    global useCheck
    if(useCheck == False):
        print("Error: No database in use. Please try again.")
        return 1
    if(os.path.isfile(workingPath + "/" + inputTokens[2])):
        tableFile = open(workingPath + "/" + inputTokens[2], 'a')
        tableFile.write("\n")

        #Clean up the input string
        record = []
        for i in range(3, len(inputTokens)):
            record.append(inputTokens[i])
        #print(record)
        #remove the word "values" from the first element
        record[0] = record[0][6:]
        #print(record)
        #remove the parentheses from the first and last elements
        record[0] = record[0][1:]
        record[-1] = record[-1][:-1]
        #print(record)
        #remove commas from all elements
        for i in range(0, len(record)):
            if(record[i][-1] == ","):
                record[i] = record[i][:-1]
        #print(record)
        # remove the quotation marks from all elements
        for i in range(0, len(record)):
            if(record[i][0] == "'"):
                record[i] = record[i][1:]
            if(record[i][-1] == "'"):
                record[i] = record[i][:-1]
        #print(record)
        #add spaces between the elements
        for i in range(0, len(record)):
            record[i] = record[i] + " "
        #print(record)
        #add | symbols between all elements except the last
        for i in range(0, len(record) - 1):
            record[i] = record[i] + "|" + " "
        #print(record)

        #Write the record to the table
        for i in range(0, len(record)):
            tableFile.write(record[i])
        tableFile.close()
    else:
        print("Table {0} does not exist.".format(inputTokens[2]))
        return 1
    return 0


def updateCommand(inputTokens):
    global workingPath
    global useCheck
    tablePath = workingPath + "/" + inputTokens[1]
    if(useCheck == False):
        print("Error: No database in use. Please try again.")
        return 1
    tableName = inputTokens[1]
    paramToChange = inputTokens[3] #name, price (set clause)
    paramToChangeCondition = inputTokens[5] #'Gizmo' (set clause)
    searchParam = inputTokens[7] #name (where clause)
    searchParamCondition = inputTokens[9] #'SuperGizmo' (where clause)


    # remove the quotation marks from the condition
    if(paramToChangeCondition[0] == "'"):
        paramToChangeCondition = paramToChangeCondition[1:]
    if(paramToChangeCondition[-1] == "'"):
        paramToChangeCondition = paramToChangeCondition[:-1]
    # remove the quotation marks from the condition
    if(searchParamCondition[0] == "'"):
        searchParamCondition = searchParamCondition[1:]
    if(searchParamCondition[-1] == "'"):
        searchParamCondition = searchParamCondition[:-1]

    #Print all of these variables to the console with labels
    #print("Table name: {0}".format(tableName))
    #print("Parameter to change: {0}".format(paramToChange))
    #print("Parameter to change condition: {0}".format(paramToChangeCondition))
    #print("Search parameter: {0}".format(searchParam))
    #print("Search parameter condition: {0}".format(searchParamCondition))

    modifiedCount = 0

    if(os.path.isfile(workingPath + "/" + inputTokens[1])):
        tableFile = open(workingPath + "/" + inputTokens[1], 'r')
        tableLines = tableFile.readlines()
        tableFile.close()

        #attribueID = 0

        wOccurence = tableLines[0].find(searchParam)
        if(wOccurence != -1):
            wCounter = tableLines[0].count("|", 0, wOccurence)
            wCounter += 1
        #print("Where clause found in column {0}.".format(wCounter))
        setOccurence = tableLines[0].find(paramToChange)
        if(setOccurence != -1):
            setCounter = tableLines[0].count("|", 0, setOccurence)
            setCounter += 1
        #print("Set clause found in column {0}.".format(setCounter))

        #testString = "test1 | test2 | test3"
        #tester = testString.find("|")
        #print(testString)
        #print(tester)

        #print("TESTING")
        #print("searchParamCondition: {0}".format(searchParamCondition))
        #print(tableLines[5])
        booler = tableLines[5].find((searchParamCondition + " "))
        #print(booler)

        for i in range(1, len(tableLines)):
            #locate the search parameter in the line
            if(tableLines[i].find((" " + searchParamCondition)) != -1):
                #print("Found {0} in line {1}.".format((" " + searchParamCondition), i))
                temp = tableLines[i]
                whereToStartSearching = 0
                for j in range(1, setCounter):
                    #print("setCounter: {0}".format(setCounter))
                    #print("temp: {0}".format(temp))
                    whereToStartSearching += temp.find("|") + 1
                    #print("temp index: {0}".format(whereToStartSearching))
                    temp = temp[whereToStartSearching:]
                whereToStartSearching += 1
                endOfEntry = tableLines[i].find(" ", whereToStartSearching)
                #print("whereToStartSearching: {0}".format(whereToStartSearching))
                #print("endOfEntry: {0}".format(endOfEntry))
                tableLines[i] = tableLines[i].replace(tableLines[i][whereToStartSearching:endOfEntry], paramToChangeCondition)
                modifiedCount += 1
                

        tableFile = open(workingPath + "/" + inputTokens[1], 'w')
        tableFile.writelines(tableLines)
        tableFile.close()
        if(modifiedCount == 1):
            print("{0} record modified.".format(modifiedCount))
        else:
            print("{0} records modified.".format(modifiedCount))
        #print("Modified {0} records.".format(modifiedCount))
        # print tableLines to the console one line at a time
        #for i in range(0, len(tableLines)):
            #print(tableLines[i])
        #print(tableLines)

        #tableFile = open(workingPath + "/" + inputTokens[1], 'w')
        #for i in range(0, len(tableLines)):
        #    if(tableLines[i].find(searchParam) != -1):
        #        tableLines[i] = tableLines[i].replace(searchParam, paramToChange)
        #tableFile.writelines(tableLines)
        #tableFile.close()
    else:
        print("Table {0} does not exist.".format(tableName))
        return 1
    return 0

def deleteCommand(inputTokens):
    global workingPath
    global useCheck
    tablePath = workingPath + "/" + inputTokens[1]
    if(useCheck == False):
        print("Error: No database in use. Please try again.")
        return 1
    tableName = inputTokens[2]
    paramater = inputTokens[4] # What attribute to search through
    parameterCondition = inputTokens[5] # what condition to use on recordToRemove
    recordToRemove = inputTokens[6] # What value to remove

    #print("tableName: {0}".format(tableName))
    #print("paramater: {0}".format(paramater))
    #print("parameterCondition: {0}".format(parameterCondition))
    #print("recordToRemove: {0}".format(recordToRemove))

    # remove the quotation marks from recordToRemove
    if(recordToRemove[0] == "'"):
        recordToRemove = recordToRemove[1:]
    if(recordToRemove[-1] == "'"):
        recordToRemove = recordToRemove[:-1]

    if(os.path.isfile(workingPath + "/" + tableName)):
        tableFile = open(workingPath + "/" + tableName, 'r')
        tableLines = tableFile.readlines()
        tableFile.close()
        
        paramaterOccurence = tableLines[0].find(paramater)
        # Find the number of pipes before the paramater
        if(paramaterOccurence != -1):
            paramaterCounter = tableLines[0].count("|", 0, paramaterOccurence)
            paramaterCounter += 1
        #print("Paramater found in column {0}.".format(paramaterCounter))

        iOffset = 0 # Used to offset the index of the line being searched as lines are removed
        recordsRemoved = 0

        for i in range(1, len(tableLines)):
            #Find the starting index of the paramter in the column specified by paramaterCounter
            newI = i - iOffset
            #print("Value of i: {0}".format(i))
            temp = tableLines[newI]
            whereToStartSearching = 0
            for j in range(1, paramaterCounter):
                whereToStartSearching += temp.find("|") + 1
                temp = temp[whereToStartSearching:]
            whereToStartSearching += 1
            endOfEntry = tableLines[newI].find(" ", whereToStartSearching)
            #print("whereToStartSearching: {0}".format(whereToStartSearching))
            #print("endOfEntry: {0}".format(endOfEntry))
            if(parameterCondition == "="):
                if(tableLines[newI][whereToStartSearching:endOfEntry] == recordToRemove):
                    #print("Found {0} in line {1}.".format(recordToRemove, newI))
                    tableLines.pop(newI)
                    iOffset += 1
                    recordsRemoved += 1
            elif(parameterCondition == ">"):
                tempSubstring = tableLines[newI][whereToStartSearching:endOfEntry]
                tempSubstringFloat = float(tempSubstring)
                recordToRemoveFloat = float(recordToRemove)
                if(tempSubstringFloat > recordToRemoveFloat):
                    #print("Found {0} in line {1}.".format(recordToRemove, newI))
                    tableLines.pop(newI)
                    iOffset += 1
                    recordsRemoved += 1
            elif(parameterCondition == "<"):
                print("Functionality not yet implemented.")

            if(recordsRemoved == 1):
                print("{0} record deleted.".format(recordsRemoved))
            else:
                print("{0} records deleted.".format(recordsRemoved))

            # write the modified table to the file
            tableFile = open(workingPath + "/" + tableName, 'w')
            tableFile.writelines(tableLines)
            tableFile.close()

            



if __name__ == "__main__":
    main()