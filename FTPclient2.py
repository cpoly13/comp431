import sys

def error(token):
    print("ERROR -- "+token)

input = sys.stdin.read()
ftpReplyLines = input.splitlines(keepends=True)

numberOfLines = len(ftpReplyLines)
currentLine = 0

while currentLine < numberOfLines:
    ftpReplyLine=ftpReplyLines[currentLine]
    sys.stdout.write(ftpReplyLine)
    testString = ftpReplyLine[:-2]
    commandGood=True
    parameters=ftpReplyLine.split()

    if not parameters[0].isdigit():
        error("reply-code")
        commandGood=False

    elif int(parameters[0])<100 or int(parameters[0])>599:
        error("reply-code")
        commandGood = False

    elif len(parameters) <2:
        error("reply-text")
        commandGood=False

    if commandGood:
        for c in testString:
            if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                error("reply-text")
                commandGood=False
    if commandGood:
        if ord(ftpReplyLine[-1]) != 10 or ord(ftpReplyLine[-2]) != 13:
            error("<CRLF>")
            commandGood=False
    if commandGood:
        print("FTP reply "+parameters[0]+" accepted.  Text is : "+testString[4:])

    currentLine+=1


