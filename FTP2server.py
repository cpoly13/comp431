# Purpose of program is to determine if a command received
# as a text string is a valid FTP command and characters adhere to ascii standard
# Commands are input as strings to standard in console in Linux enviroment
# Correctness is output to standard output

# Example1: INPUT: USER Chris OUTPUT: Command ok
# Example2: INPUT: PASSabc OUTPUT: ERROR -- Command

import shutil
import sys

# start by getting input and break into list of separate lines,
from pathlib import Path

sys.stdout.write("220 COMP 431 FTP server ready.\r\n")
input = sys.stdin.read()
ftpInputs = input.splitlines(keepends=True)


# get number of lines to use as number of iterations for main loop
numberOfLines = len(ftpInputs)
#set counters for states that need to be maintained across iterations
fileRetrCount=1
currentState=0
currentLine = 0

# Main program body executes for each line of input,
# and tests for line adhering to FTP command protocol
# Outputs appropriate message as to whether command is valid
# For each loop the invariant holds that one line of input is being analyzed
# for correctness. Each iteration moves on to the next FTP command line
while currentLine < numberOfLines:

    # set specific ftp command line
    ftpInput = ftpInputs[currentLine]
    # string without end CRLF for testing characters within ascii exluding CR, LF
    testString = ftpInput[:-2]

    sys.stdout.write(ftpInput)
    # Split tokens to be tested individually for correctness depending on location
    command = ftpInput.split()
    # for testing that number of tokens are correct for command
    listLength = len(command)
    commandOk = True

    if ftpInput[0] == " ":
        sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
        commandOk = False

    # USER command tests
    if command[0].lower() == "user":

        if listLength < 2:
            if ftpInput[4] == ' ':
                sys.stdout.write("Syntax error in parameter.\r\n")
            else:
                sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
            commandOk = False
        else:
            for c in testString:
                if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                    sys.stdout.write("Syntax error in parameter.\r\n")
                    commandOk = False
                    break
            if ord(ftpInput[-1]) != 10 or ord(ftpInput[-2]) != 13:
                sys.stdout.write("Syntax error in parameter.\r\n")
                commandOk = False
        if commandOk == True:
            currentState=1
            sys.stdout.write("331 Guest access OK, send password.\r\n")

    # PASS command tests
    elif command[0].lower() == "pass":
        if currentState == 1:
            if listLength < 2:
                if ftpInput[4] == ' ':
                    sys.stdout.write("Syntax error in parameter.\r\n")
                else:
                    sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
                commandOk = False
            else:
                for c in testString:
                    if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                        sys.stdout.write("Syntax error in parameter.\r\n")
                        commandOk = False
                        break
                if ord(ftpInput[-1]) != 10 or ord(ftpInput[-2]) != 13:
                    sys.stdout.write("Syntax error in parameter.\r\n")
                    commandOk = False
            if commandOk == True:
                sys.stdout.write("230 Guest login OK.\r\n")
                currentState=2

        elif currentState == 0:
            sys.stdout.write("530 Not logged in.\r\n")
        else:
            sys.stdout.write("503 Bad sequence of commands.\r\n")



    # TYPE command tests
    elif command[0].lower() == "type":
        if currentState>=2:
            if listLength < 2:
                sys.stdout.write("Syntax error in parameter.\r\n")
                commandOk = False
            else:
                if command[1] == "A":
                    index = ftpInput.find('A')
                    if len(ftpInput) != index + 3 or ord(ftpInput[index + 1]) != 13 or ord(ftpInput[index + 2]) != 10:
                        sys.stdout.write("Syntax error in parameter.\r\n")
                        commandOk = False
                    else:
                        sys.stdout.write("200 Type set to A.\r\n")
                elif command[1] == "I":
                    index = ftpInput.find('I')
                    if len(ftpInput) != index + 3 or ord(ftpInput[index + 1]) != 13 or ord(ftpInput[index + 2]) != 10:
                        sys.stdout.write("Syntax error in parameter.\r\n")
                        commandOk = False
                    else:
                        sys.stdout.write("200 Type set to I.\r\n")
                else:
                    sys.stdout.write("Syntax error in parameter.\r\n")
                    commandOk = False
        else:
            sys.stdout.write("530 Not logged in.\r\n")

    # SYST command tests
    elif command[0].lower() == "syst":
        if currentState>=2:
            if listLength != 1:
                sys.stdout.write("Syntax error in parameter.\r\n")
                commandOk = False
            elif len(ftpInput) != 6:
                sys.stdout.write("Syntax error in parameter.\r\n")
                commandOk = False
            elif ord(ftpInput[4]) != 13 or ord(ftpInput[5]) != 10:
                sys.stdout.write("Syntax error in parameter.\r\n")
                commandOk = False
            else:
                sys.stdout.write("UNIX Type: L8.\r\n")
        else:
            sys.stdout.write("530 Not logged in.\r\n")

    # NOOP command tests
    elif command[0].lower() == "noop":
        if currentState>=2:
            if listLength != 1:
                sys.stdout.write("Syntax error in parameter.\r\n")
                commandOk = False
            elif len(ftpInput) != 6:
                sys.stdout.write("Syntax error in parameter.\r\n")
                commandOk = False
            elif ord(ftpInput[4]) != 13 or ord(ftpInput[5]) != 10:
                sys.stdout.write("Syntax error in parameter.\r\n")
                commandOk = False
            else:
                sys.stdout.write("200 Command OK.\r\n")
        else:
            sys.stdout.write("530 Not logged in.\r\n")



    # QUIT command tests
    elif command[0].lower() == "quit":
        if listLength != 1:
            sys.stdout.write("Syntax error in parameter.\r\n")
            commandOk = False
        elif len(ftpInput) != 6:
            sys.stdout.write("Syntax error in parameter.\r\n")
            commandOk = False
        elif ord(ftpInput[4]) != 13 or ord(ftpInput[5]) != 10:
            sys.stdout.write("Syntax error in parameter.\r\n")
            commandOk = False
        else:
            currentState=-1
            sys.stdout.write("200 Command OK.\r\n")

    # PORT command tests
    elif command[0].lower() == "port":
        if currentState>=2:
            if listLength < 2:
                if ftpInput[4] == ' ':
                    sys.stdout.write("Syntax error in parameter.\r\n")
                else:
                    sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
                commandOk = False
            else:
                for c in testString:
                    if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                        sys.stdout.write("Syntax error in parameter.\r\n")
                        commandOk = False
                        break
                if ord(ftpInput[-1]) != 10 or ord(ftpInput[-2]) != 13:
                    sys.stdout.write("Syntax error in parameter.\r\n")
                    commandOk = False
                elif len(command[1].split(","))!= 6:
                    sys.stdout.write("Syntax error in parameter.\r\n")
                    commandOk=False
                else:
                    ipNumbers=command[1].split(",")
                    for x in range(0,5):

                        if not ipNumbers[x].isdigit():
                            sys.stdout.write("Syntax error in parameter.\r\n")
                            commandOk=False
                            break

            if commandOk == True:
                portAddress=int(ipNumbers[4])*256+int(ipNumbers[5])
                ipAddress=(ipNumbers[0]+"."+ipNumbers[1]+"."+ipNumbers[2]+"."+ipNumbers[3]
                +"."+str(portAddress))
                currentState=3
                sys.stdout.write("200 Port command successful ("+ipAddress+")\r\n")
        else:
            sys.stdout.write("530 Not logged in.\r\n")



    #RETR command tests and file copy if correct syntax
    elif command[0].lower() == "retr":
        if currentState==3:
            if listLength < 2:
                if ftpInput[4] == ' ':
                    sys.stdout.write("Syntax error in parameter.\r\n")
                else:
                    sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
                commandOk = False
            else:
                for c in testString:
                    if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                        sys.stdout.write("Syntax error in parameter.\r\n")
                        commandOk = False
                        break
                if ord(ftpInput[-1]) != 10 or ord(ftpInput[-2]) != 13:
                    sys.stdout.write("Syntax error in parameter.\r\n")
                    commandOk = False
            if commandOk == True:
                if command[1][0]=="/" or ord(command[1][0])==92:
                    command[1]=command[1][1:]
                try:
                    my_file=Path(command[1])
                    if not my_file.is_file():
                        raise Exception
                    sys.stdout.write("150 File status okay.\r\n")
                    shutil.copyfile(command[1],"retr_files/file"+str(fileRetrCount))
                    fileRetrCount=fileRetrCount+1
                    currentState=2
                    sys.stdout.write("250 Requested file action completed.\r\n")
                except:
                    sys.stdout.write("550 File not found or access denied.\r\n")
        elif currentState <2:
            sys.stdout.write("530 Not logged in.\r\n")
        else:
            sys.stdout.write("503 Bad sequence of commands.\r\n")
    else:
        sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
        commandOk = False

    if currentState==-1:
        break
    currentLine += 1
