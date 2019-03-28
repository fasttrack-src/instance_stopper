import json
from pprint import pprint
with open("test.py") as f:
    lines = [line[:-1] for line in f]

count = 0
for line in lines:
    count += len(line)

dump = json.dumps(lines)

print('"ZipFile" : { "Fn::Join" : ["\\n", ')
print(dump.replace(", ",", \n"))
print("]}")
print(count)