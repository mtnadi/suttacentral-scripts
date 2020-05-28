## Open a hard-coded file and return the number of lines in the file.

f = open(file="data\sample7sunny_root.json")

TotalLines = len(f.readlines())

print(f"Your file is {TotalLines} lines long.")
