# Author: Alexander Perez-Herrera
# Date: 03/31/23
# Name: driver.py
# Purpose: Simulate an enviroment like the sqlite3 command line interface. This iteration of the program far further functionality than the previous iteration.
import sys
import os.path

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
            
            print(inputTokens)
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
        print(record)
        #remove the word "values" from the first element
        record[0] = record[0][6:]
        print(record)
        #remove the parentheses from the first and last elements
        record[0] = record[0][1:]
        record[-1] = record[-1][:-1]
        print(record)
        #remove commas from all elements
        for i in range(0, len(record)):
            if(record[i][-1] == ","):
                record[i] = record[i][:-1]
        print(record)
        # remove the quotation marks from all elements
        for i in range(0, len(record)):
            if(record[i][0] == "'"):
                record[i] = record[i][1:]
            if(record[i][-1] == "'"):
                record[i] = record[i][:-1]
        print(record)
        #add spaces between the elements
        for i in range(0, len(record)):
            record[i] = record[i] + " "
        print(record)
        #add | symbols between all elements except the last
        for i in range(0, len(record) - 1):
            record[i] = record[i] + "|" + " "
        print(record)

        #Write the record to the table
        for i in range(0, len(record)):
            tableFile.write(record[i])
        tableFile.close()
    return 0

if __name__ == "__main__":
    main()