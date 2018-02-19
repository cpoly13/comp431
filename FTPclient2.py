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

    parameters=ftpReplyLine.split()

    if not parameters[0].isdigit():
        error("reply-code")
        continue
    if parameters[0]<100 or parameters[0]>599:
        error("reply-code")
        continue

    if len(parameters) <2:
        error("reply-text")
        continue
    for c in testString:
        if ord(c) > 127 or (ord(c) == 13 or ord(c) == 10):
            error("reply-text")
            continue
    if ord(ftpReplyLine[-1]) != 10 or ord(ftpReplyLine[-2]) != 13:
        error("<CRLF>")
        continue

    currentLine+=1


