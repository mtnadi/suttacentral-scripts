## Open a hard-coded file and return the number of lines in the file.
filename = "data\sample7sunny_root.json"
f = open(file=filename)
allLines = f.readlines()
firstLine = False
lastLine = False
textLength = 0
for x in allLines:
    if x == '{\n':
        firstLine = True
    elif x == '}\n':
        lastLine = True
    elif firstLine == True and lastLine == False:
        textLength += 1
        if not x.strip():
            print("Space in the middle!")
    # print(textLength)

print(f"File '{filename}' is {len(allLines)} lines long,")
print(f"and there are {textLength} lines of text.")

## Figure out whether the first and last lines are empty.

## Spit out all the segment numbers in the file
