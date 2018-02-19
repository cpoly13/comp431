# FTP Reply Parser
# The purpose of this program is to check FTP replies for correctness

# Example:

# Input:

# 220 COMP 431 FTP server ready.
# 331 Guest access OK, send password.
# 230Guest login OK.
# Port command successful (152.2.131.205,8080).
# 650 File status okay.

# Output:

# 220 COMP 431 FTP server ready.
# FTP reply 220 accepted. Text is : COMP 431 FTP server ready.
# 331 Guest access OK, send password.
# FTP reply 331 accepted. Text is : Guest access OK, send password.
# 230Guest login OK.
# ERROR -- reply-code
# Port command successful (152.2.131.205,8080).
# ERROR -- reply-code
# 650 File status okay.
# ERROR – reply-code

import sys


def error(token):
    print("ERROR -- " + token)


input = sys.stdin.read()
# Split by lines but keep ends to test CRLF token
ftpReplyLines = input.splitlines(keepends=True)

numberOfLines = len(ftpReplyLines)
currentLine = 0

while currentLine < numberOfLines:
    ftpReplyLine = ftpReplyLines[currentLine]
    sys.stdout.write(ftpReplyLine)

    #input line without CRLF tokens
    testString = ftpReplyLine[:-2]

    commandGood = True
    parameters = ftpReplyLine.split()

    #Valid reply code tests
    if not parameters[0].isdigit():
        error("reply-code")
        commandGood = False

    elif int(parameters[0]) < 100 or int(parameters[0]) > 599:
        error("reply-code")
        commandGood = False

    #Valid reply-text test
    elif len(parameters) < 2:
        error("reply-text")
        commandGood = False

    if commandGood:
        for c in testString:
            if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
                error("reply-text")
                commandGood = False
    #CRLF test
    if commandGood:
        if ord(ftpReplyLine[-1]) != 10 or ord(ftpReplyLine[-2]) != 13:
            error("<CRLF>")
            commandGood = False

    if commandGood:
        print("FTP reply " + parameters[0] + " accepted.  Text is : " + testString[4:])

    currentLine += 1
