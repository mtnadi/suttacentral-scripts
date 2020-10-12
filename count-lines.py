file_no = "21"
## Open a hard-coded file and return the number of lines in the file.
filename = "data\sample7sunny_root.json"
filename = f"../bilara-data/translation/en/brahmali/vinaya/pli-tv-pvr/pli-tv-pvr{file_no}_translation-en-brahmali.json"
f = open(file=filename)
allLines = f.readlines()
firstLine = False
lastLine = False
textLength = 0
segments = []
for x in allLines:
    if x == '{\n':
        firstLine = True
    elif x.strip() == '}':
        lastLine = True
    elif firstLine == True and lastLine == False:
        textLength += 1
        if not x.strip():
            print("Space in the middle!")
        else:
            segments.append(x.strip().rstrip(",").split(": ", 1)[0])
    # print(textLength)

print(f"File '{filename}' is {len(allLines)} lines long,")
print(f"and there are {textLength} lines of text.")

## Figure out whether the first and last lines are empty.

## Spit out all the segment numbers in the file
#for segment in segments:
#    print(segment)
filename = f"../bilara-data/root/pli/ms/vinaya/pli-tv-pvr/pli-tv-pvr{file_no}_root-pli-ms.json"
f = open(file=filename)
allLines = f.readlines()
firstLine = False
lastLine = False
textLength = 0
root_segments = []
for x in allLines:
    if x == '{\n':
        firstLine = True
    elif x.strip() == '}':
        lastLine = True
    elif firstLine == True and lastLine == False:
        textLength += 1
        if not x.strip():
            print("Space in the middle!")
        else:
            root_segments.append(x.strip().rstrip(",").split(": ", 1)[0])

print(f"File '{filename}' is {len(allLines)} lines long,")
print(f"and there are {textLength} lines of text.")

if segments == root_segments:
    print("Segments are all the same")
else:
    print("Segments are not in synch")
