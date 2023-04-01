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
            
            #print(inputTokens)
            recognizeInput(inputTokens)

def recognizeInput(inputTokens):
    command = inputTokens[0]
    if command == ".exit":
        print("All done.")
        quit()
    elif command == "CREATE":
        createCommand(inputTokens)
    elif command == "DROP":
        dropCommand(inputTokens)
    elif command == "SELECT":
        selectCommand(inputTokens)
    elif command == "USE":
        if(len(inputTokens) == 2):
            print("Use command")
            useCommand(inputTokens)
        else:
            print("Error: Invalid syntax. Please try again.")
            return 1
    elif command == "INSERT":
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
    print("Initialize table")
    if(useCheck == False): # If no database is in use, return an error
        print("Error: No database in use. Please try again.")
        return 1
    if(os.path.isfile(workingPath + "/" + inputTokens[2])): # If the table already exists, return an error
        print("!Failed to create table {0} because it already exists.".format(inputTokens[2]))
        return 1
    else: # If the table does not exist, create it
        open((workingPath + "/" + inputTokens[2]), 'w')
        print("Table {0} created.".format(inputTokens[2]))
    return 0

def dropCommand(inputTokens):
    print("Drop command")

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
    print("Select command")

def insertCommand(inputTokens):
    print("Insert command")

if __name__ == "__main__":
    main()