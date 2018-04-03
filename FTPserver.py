# Purpose of program is to parse FTP commands and to begin processing file data
# Commands are tested as a valid FTP command that is also valid for the current program state
# Characters must adhere to ascii standard
# Commands are input as strings to standard in console in Linux environment
# Correctness is output to standard output
# Example:
# Input:

# USER anonymous
#PASS foobar
#SYST
#TYPE I
#PORT 152,2,131,205,31,144
#RETR pictures/jasleen.jpg
#QUIT

#Output:
#220 COMP 431 FTP server ready.
#USER anonymous
#331 Guest access OK, send password.
#PASS foobar
#230 Guest login OK.
#SYST
#215 UNIX Type: L8.
#TYPE I
#200 Type set to I.
#PORT 152,2,131,205,31,144
#200 Port command successful (152.2.131.205,8080).
#RETR pictures/jasleen.jpg
#150 File status okay.
#250 Requested file action completed.
#QUIT
#200 Command OK.


import shutil
import sys
import socket
from pathlib import Path

portNumber = int(sys.argv[1])
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", portNumber))
server_socket.listen(1) # Allow only one connection at a time
while True:
    connectionSocket, addr=server_socket.accept()
    response="220 COMP 431 FTP server ready.\r\n"
    connectionSocket.send(response.encode())
    while True:
        received=connectionSocket.recv(4096)
        inputCommand=received.decode()
    connectionSocket.close()



#sys.stdout.write("220 COMP 431 FTP server ready.\r\n")

# Get input and break into list of separate lines
input = sys.stdin.read()
ftpInputs = input.splitlines(keepends=True)


# iterations for main loop
numberOfLines = len(ftpInputs)

#set counters for states that need to be maintained across iterations
currentState=0
fileRetrCount=1
currentLine = 0

# Main program body executes for each line of input
# Outputs appropriate message and executes appropriate action
# For each loop the invariant holds that one line of input is being analyzed
# for correctness.
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

    # USER command actions
    if command[0].lower() == "user":

        if listLength < 2:
            if ftpInput[4] == ' ':
                sys.stdout.write("501 Syntax error in parameter.\r\n")
            else:
                sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
            commandOk = False
        else:
            for c in testString:
                if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                    sys.stdout.write("501 Syntax error in parameter.\r\n")
                    commandOk = False
                    break
            if ord(ftpInput[-1]) != 10 or ord(ftpInput[-2]) != 13:
                sys.stdout.write("501 Syntax error in parameter.\r\n")
                commandOk = False
        if commandOk == True:
            currentState=1
            sys.stdout.write("331 Guest access OK, send password.\r\n")

    # PASS command actions
    elif command[0].lower() == "pass":

        if listLength < 2:
            if ftpInput[4] == ' ':
                sys.stdout.write("501 Syntax error in parameter.\r\n")
            else:
                sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
            commandOk = False
        else:
            for c in testString:
                if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                    sys.stdout.write("501 Syntax error in parameter.\r\n")
                    commandOk = False
                    break
            if ord(ftpInput[-1]) != 10 or ord(ftpInput[-2]) != 13:
                sys.stdout.write("501 Syntax error in parameter.\r\n")
                commandOk = False
        if commandOk == True:
            if currentState == 1:
                sys.stdout.write("230 Guest login OK.\r\n")
                currentState=2

            elif currentState == 0:
                sys.stdout.write("530 Not logged in.\r\n")
            else:
                sys.stdout.write("503 Bad sequence of commands.\r\n")

    # TYPE command actions
    elif command[0].lower() == "type":

        if listLength < 2:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        else:
            if command[1] == "A":
                index = ftpInput.find('A')
                if len(ftpInput) != index + 3 or ord(ftpInput[index + 1]) != 13 or ord(ftpInput[index + 2]) != 10:
                    sys.stdout.write("501 Syntax error in parameter.\r\n")
                    commandOk = False
                else:
                    if currentState >= 2:
                        sys.stdout.write("200 Type set to A.\r\n")
                    else:
                        sys.stdout.write("530 Not logged in.\r\n")

            elif command[1] == "I":
                index = ftpInput.find('I')
                if len(ftpInput) != index + 3 or ord(ftpInput[index + 1]) != 13 or ord(ftpInput[index + 2]) != 10:
                    sys.stdout.write("501 Syntax error in parameter.\r\n")
                    commandOk = False
                else:
                    if currentState >= 2:
                        sys.stdout.write("200 Type set to I.\r\n")
                    else:
                        sys.stdout.write("530 Not logged in.\r\n")
            else:
                sys.stdout.write("501 Syntax error in parameter.\r\n")
                commandOk = False

    # SYST command actions
    elif command[0].lower() == "syst":

        if listLength != 1:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        elif len(ftpInput) != 6:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        elif ord(ftpInput[4]) != 13 or ord(ftpInput[5]) != 10:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        else:
            if currentState >= 2:
                sys.stdout.write("215 UNIX Type: L8.\r\n")
            else:
                sys.stdout.write("530 Not logged in.\r\n")

    # NOOP command actions
    elif command[0].lower() == "noop":

        if listLength != 1:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        elif len(ftpInput) != 6:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        elif ord(ftpInput[4]) != 13 or ord(ftpInput[5]) != 10:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        else:
            if currentState >= 2:
                sys.stdout.write("200 Command OK.\r\n")
            else:
                sys.stdout.write("530 Not logged in.\r\n")

    # QUIT command actions
    elif command[0].lower() == "quit":
        if listLength != 1:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        elif len(ftpInput) != 6:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        elif ord(ftpInput[4]) != 13 or ord(ftpInput[5]) != 10:
            sys.stdout.write("501 Syntax error in parameter.\r\n")
            commandOk = False
        else:
            currentState=-1
            sys.stdout.write("200 Command OK.\r\n")

    # PORT command actions
    elif command[0].lower() == "port":

        if listLength < 2:
            if ftpInput[4] == ' ':
                sys.stdout.write("501 Syntax error in parameter.\r\n")
            else:
                sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
            commandOk = False
        else:
            for c in testString:
                if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                    sys.stdout.write("501 Syntax error in parameter.\r\n")
                    commandOk = False
                    break
            if ord(ftpInput[-1]) != 10 or ord(ftpInput[-2]) != 13:
                sys.stdout.write("501 Syntax error in parameter.\r\n")
                commandOk = False
            elif len(command[1].split(","))!= 6:
                sys.stdout.write("501 Syntax error in parameter.\r\n")
                commandOk=False
            else:
                ipNumbers=command[1].split(",")
                for x in range(0,5):

                    if not ipNumbers[x].isdigit():
                        sys.stdout.write("501 Syntax error in parameter.\r\n")
                        commandOk=False
                        break
                    elif int(ipNumbers[x])<0 or int(ipNumbers[x])>255:
                        sys.stdout.write("501 Syntax error in parameter.\r\n")
                        commandOk = False
                        break

        if commandOk == True:
            if currentState >= 2:
                portAddress=int(ipNumbers[4])*256+int(ipNumbers[5])
                ipAddress=(ipNumbers[0]+"."+ipNumbers[1]+"."+ipNumbers[2]+"."+ipNumbers[3]
                +","+str(portAddress))
                currentState=3
                sys.stdout.write("200 Port command successful ("+ipAddress+").\r\n")
            else:
                sys.stdout.write("530 Not logged in.\r\n")



    #RETR command actions and file copy if correct syntax
    elif command[0].lower() == "retr":

        if listLength < 2:
            if ftpInput[4] == ' ':
                sys.stdout.write("501 Syntax error in parameter.\r\n")
            else:
                sys.stdout.write("500 Syntax error, command unrecognized.\r\n")
            commandOk = False
        else:
            for c in testString:
                if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                    sys.stdout.write("501 Syntax error in parameter.\r\n")
                    commandOk = False
                    break
            if ord(ftpInput[-1]) != 10 or ord(ftpInput[-2]) != 13:
                sys.stdout.write("501 Syntax error in parameter.\r\n")
                commandOk = False
        if commandOk == True:
            if currentState == 3:
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

    # For QUIT command
    if currentState==-1:
        break
    currentLine += 1
