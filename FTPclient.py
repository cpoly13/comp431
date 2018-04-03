# Purpose of program is to read standard input lines from a user and if valid output a valid FTP command
# Inputs are tested for validity and if not valid appropriate error message displays
# Commands are input as strings
# Correctness is output to standard output

# Example:

# Input:

# CONNECT swift.cs.unc.edu 9000
# GET pictures/jasleen.jpg
# CONNECT capefear.cs.unc.edu 21
# GET index.html
# QUIT

# Output:

# CONNECT swift.cs.unc.edu 9000
# CONNECT accepted for FTP server at host swift.cs.unc.edu and port 9000
# USER anonymous
# PASS guest@
# SYST
# TYPE I
# GET pictures/jasleen.jpg
# GET accepted for pictures/jasleen.jpg
# PORT 152,2,129,144,31,64
# RETR pictures/jasleen.jpg
# CONNECT capefear.cs.unc.edu 21
# CONNECT accepted for FTP server at host capefear.cs.unc.edu and port 21
# USER anonymous
# PASS guest@
# SYST
# TYPE I
# GET index.html
# GET accepted for index.html
# PORT 152,2,129,144,31,65
# RETR index.html
# QUIT
# QUIT accepted, terminating FTP client
# QUIT

import socket
import sys


def error(token="request"):
    print("ERROR -- " + token)


# test server host inputs (delimited by ".") for correct syntax, a-z,A-Z,0-9 etc.
def testServerHost(s):
    if len(s) < 2:
        return False
    if s[0].isalpha() is False:
        return False
    for c in s:
        if (ord(c) < 48 or ord(c) > 57) and (ord(c) < 65 or ord(c) > 90) and (ord(c) < 97 or ord(c) > 122):
            return False
    return True


# test server port number for correct format and range
def testServerPort(s):
    if len(s) > 5:
        return False
    for c in s:
        if not c.isdigit():
            return False
    if int(s[0]) == 0:
        return False
    if int(s) > 65535:
        return False
    return True

def error(token):
    print("ERROR -- " + token)

def outPutServerResponse(s):
    input = s
    # Split by lines but keep ends to test CRLF token
    ftpReplyLines = input.splitlines(keepends=True)

    numberOfLines = len(ftpReplyLines)
    currentLine = 0

    while currentLine < numberOfLines:
        ftpReplyLine = ftpReplyLines[currentLine]
        sys.stdout.write(ftpReplyLine)

        # input line without CRLF tokens
        testString = ftpReplyLine[:-2]

        commandGood = True
        parameters = ftpReplyLine.split()

        # Valid reply code tests
        if not parameters[0].isdigit():
            error("reply-code")
            commandGood = False

        elif int(parameters[0]) < 100 or int(parameters[0]) > 599:
            error("reply-code")
            commandGood = False

        # Valid reply-text test
        elif len(parameters) < 2:
            error("reply-text")
            commandGood = False

        if commandGood:
            for c in testString:
                if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                    error("reply-text")
                    commandGood = False
        # CRLF test
        if commandGood:
            if ord(ftpReplyLine[-1]) != 10 or ord(ftpReplyLine[-2]) != 13:
                error("<CRLF>")
                commandGood = False

        if commandGood:
            print("FTP reply " + parameters[0] + " accepted.  Text is : " + testString[4:])

        currentLine += 1


# Convert to decimal values contained in high and low order bytes of
# 16 bit binary representation of an integer in 2's compliment
def formatPortNum(num):
    remainder = portNumber % 256
    divNum = int(num / 256)

    return str(divNum) + "," + str(remainder)


connected = False
# default starting port number
welcomePortNumber = int(sys.argv[1])
portNumber = 8000

for line in sys.stdin:
    # echo line to see input before output message
    sys.stdout.write(line)

    command = line.split()
    commandLength = len(command)
    # CONNECT command tests and outputs
    # CONNECT must be first valid input
    if command[0] == "CONNECT":

        commandGood = True

        if commandLength < 2:
            error("server-host")
            commandGood = False

        serverInput = command[1].split(".")

        for s in serverInput:

            if not testServerHost(s):
                error("server-host")
                commandGood = False
                continue

        if not commandGood:
            continue

        if commandLength != 3 or line[-2] == " ":
            error("server-port")
            continue

        if not testServerPort(command[2]):
            error("server-port")
            continue
        # Valid connection, set connection as active
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.connect((command[1],int(command[2])))
                response=s.recv(4096)
                responseString=response.decode()
                print(("CONNECT accepted for FTP server at host " + command[1] + " and"
                                                                                 " port " + command[2]))
                outPutServerResponse(responseString)
                connected = True

                while True:
                    #dostuff
                    print("do stuff")
                    break
            except:
                print("CONNECT failed")
                connected=False
                break


        if connected == True:
            # FTP Outputs
            sys.stdout.write("USER anonymous\r\n")
            sys.stdout.write("PASS guest@\r\n")
            sys.stdout.write("SYST\r\n")
            sys.stdout.write("TYPE I\r\n")

            #reset port number on each new connection
            portNumber = 8000

    # GET command tests and outputs
    elif command[0] == "GET":
        commandGood = True
        if commandLength != 2:
            error()
            continue
        for c in command[1]:
            if ord(c) > 128:
                error("pathname")
                commandGood = False
                break
        if not commandGood:
            continue
        if not connected:
            error("expecting CONNECT")
            continue
        print("GET accepted for " + command[1])

        #gets local ip address
        my_ip = socket.gethostbyname(socket.gethostname())

        ipArray = my_ip.split(".")
        formatedPortNum = formatPortNum(portNumber)
        hostAdd = ipArray[0] + ',' + ipArray[1] + ',' + ipArray[2] + ',' + ipArray[3]
        hostPort = hostAdd + "," + formatedPortNum
        #FTP Outputs
        sys.stdout.write("PORT " + hostPort + "\r\n")
        #Increment port number with every FTP PORT command
        portNumber = portNumber + 1
        sys.stdout.write("RETR " + command[1] + "\r\n")

    #QUIT command tests and output
    elif command[0] == "QUIT":

        if len(line) != 5:
            error()
            continue

        if not connected:
            error("expecting CONNECT")
            continue
        print("QUIT accepted, terminating FTP client")
        sys.stdout.write("QUIT\r\n")
        #ends program
        break

    else:
        error()
