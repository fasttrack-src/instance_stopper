import pystache
import json

configfile = "config.json"

with open(configfile) as f:
    config = "".join(f.readlines())

config = json.loads(config)

print(config)

cron = config["cron"]

template = config["template"]
codefile = config["codefile"]
output = config["output"]

print("Reading code from file "+codefile)
with open(codefile) as f:
    lines = [line[:-1] for line in f]

count = 0
for line in lines:
    count += len(line)
print("This file has "+str(count)+" lines")


dump = json.dumps(lines)

code = '{"ZipFile" : { "Fn::Join" : ["\\n", ' + "\n"
code += dump + "]}}"

print("Writing code into template "+template)
with open(template) as f:
    lines = "".join(f.readlines())
    rend = pystache.render(lines,{"code":code,"cron":cron})

print("Outputting to file "+output)
with open(output,"w") as f:
    f.write(rend)