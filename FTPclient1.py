import socket
import sys

def error(token="request"):
    print("ERROR -- "+token)

def testServerHost(s):

    if len(s)<2:
        return False
    if s[0].isalpha() is False:
        return False
    for c in s:
        if (ord(c) <48 or ord(c)>57) and (ord(c)<65 or ord(c)>90) and (ord(c)<97 or ord(c)>122):
            return False
    return True

def testServerPort(s):
    if len(s) > 5:
        return False
    for c in s:
        if not c.isdigit():
            return False
    if int(s)>65535:
        return False
    return True

def formatPortNum(num):

    remainder=portNumber%256
    divNum=int (num/256)

    return str(divNum)+","+ str(remainder)



connected=False
portNumber=8000

for line in sys.stdin:
    sys.stdout.write(line)

    command=line.split()
    commandLength=len(command)

    if command[0] == "CONNECT":

        commandGood=True

        if commandLength < 2:
            error("server-host")
            commandGood = False

        serverInput=command[1].split(".")

        for s in serverInput:

            if not testServerHost(s):
                error("server-host")
                commandGood=False
                continue

        if not commandGood:
            continue

        if commandLength!=3:
            error("server-port")
            continue

        if not testServerPort(command[2]):
            error("server-port")
            continue

        connected=True
        print(("CONNECT accepted for FTP server at host "+command[1]+" and"
        " port "+command[2]))

        sys.stdout.write("USER anonymous\r\n")
        sys.stdout.write("PASS guest@\r\n")
        sys.stdout.write("SYST\r\n")
        sys.stdout.write("TYPE I\r\n")

        portNumber=8000

    elif command[0]=="GET":
        commandGood=True
        if commandLength != 2:
            error()
            continue
        for c in command[1]:
            if ord(c)>128:
                error("pathname")
                commandGood=False
                break
        if not commandGood:
            continue
        if not connected:
            error("expecting CONNECT")
            continue
        print("GET accepted for "+command[1])

        my_ip=socket.gethostbyname(socket.gethostname())

        ipArray = my_ip.split(".")
        formatedPortNum=formatPortNum(portNumber)
        hostAdd=ipArray[0]+','+ipArray[1]+','+ipArray[2]+','+ipArray[3]
        hostPort=hostAdd+","+formatedPortNum

        sys.stdout.write("PORT "+hostPort+"\r\n")
        portNumber=portNumber+1
        sys.stdout.write("RETR "+command[1]+"\r\n")

    elif command[0]== "QUIT":

        if len(line)!= 5:
            error()
            continue

        print("QUIT accepted, terminating FTP client")
        sys.stdout.write("QUIT\r\n")
        break

    else:
        error()
