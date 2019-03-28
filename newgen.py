import pystache
import json

template = "template.json"
codefile = "test.py"
code = ""
output = "cloudformgened.json"

with open(codefile) as f:
    lines = [line[:-1] for line in f]

count = 0
for line in lines:
    count += len(line)

dump = json.dumps(lines)

code = '{"ZipFile" : { "Fn::Join" : ["\\n", ' + "\n"
code += dump.replace(", ",", \n") + "]}}"
print(count)

with open(template) as f:
    lines = "".join(f.readlines())
    rend = pystache.render(lines,{"code":code})

with open(output,"w") as f:
    f.write(rend)