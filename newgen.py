import pystache
import json

cron = "cron(0 11 * * ? *)"
# cron = "this is a test"

template = "template.json"
codefile = "Final.py"
output = "cloudformgened.json"

with open(codefile) as f:
    lines = [line[:-1] for line in f]

count = 0
for line in lines:
    count += len(line)

dump = json.dumps(lines)

code = '{"ZipFile" : { "Fn::Join" : ["\\n", ' + "\n"
code += dump + "]}}"

with open(template) as f:
    lines = "".join(f.readlines())
    rend = pystache.render(lines,{"code":code,"cron":cron})

with open(output,"w") as f:
    f.write(rend)