from shlex import split
from uuid import uuid1
from sys import argv

def list_to_gen(input_list):
    for item in input_list:
        yield item
        
        
macros = {}

def getBlock(tokens):
    out = ""
    while True:
        out+= next(tokens).lstrip(" ")
        if out.endswith("}") and out.count("{") == out.count("}"):
            break 
        else:
            out+="\n"
    return out.strip("{}")

class macro:
    def __init__(self,args,content,block=False):
        self.args=args
        self.content=content
        self.block=block
    def __str__(self,format):
        return f"({self.args}):{self.content}"
    def __repr__(self):
        return self.__str__(self)
    def run(self,passedArgs,lines):
        temp = self.content
        if self.block:
            passedArgs.append(getBlock(lines).strip("{}"))
        if len(self.args) == len(passedArgs):
            for n , arg in enumerate(passedArgs):
                temp = temp.replace(self.args[n],arg)
            return parse(text = temp)


def parse(filename="-",text=""):
    scriptFile=text
    if filename != "-":
        with open(filename) as file:
            scriptFile=file.read()
    output=[]
    script = scriptFile.split("\n")
    script = ([x for x in script if x!= "" ])
    lines = list_to_gen(script)
    for line in lines:
        tokens = line.lstrip(" ").split(" ")
        if tokens == [""]:
            continue
        elif tokens[0] == "import":
            file_name = tokens[1]
            output.append(parse(file_name))
        elif tokens[0] == "macro":
            args = split(line)[1:]
            macros[tokens[1]]=macro(args,getBlock(lines))
        elif tokens[0] in macros.keys():
            mline = split(line)
            mac = macros[tokens[0]]
            output.append(mac.run(mline,lines))
        elif tokens[0] == "block_macro":
            args = split(line)[1:]
            macros[tokens[1]]=macro(args,getBlock(lines),block=True)
        elif tokens[0] == "runtime":
            b = getBlock(lines)
            output.append(parse(text=eval(b)))
        else:
            output.append(line)

    output = ([x for x in output if x!= "" ])
    return "\n".join(output)


if len(argv) >1:
    print(parse(argv[1]))
else:
    print(parse("storm"))

