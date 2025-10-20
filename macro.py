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
    return out

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
            # print("-------")
            # print(passedArgs[-1])
            # print("-------")
            # print("+++++++")
            # print(self.content)
            # print("+++++++")
            # print("=======")
            # print(passedArgs)
            # print("=======")
        if len(self.args) == len(passedArgs):
            for n , arg in enumerate(passedArgs):
                temp = temp.replace(self.args[n],arg)
            return parse(text = temp)




def j(text):
    return " ".join(text)


def parse(filename="-",files=[],text=""):
    if filename in files:
        return "error recursive import"
    scriptFile=text
    if filename != "-":
        with open(filename) as file:
            scriptFile=file.read()
    output=[]
    script = scriptFile.split("\n")
    # script = [ j(split(x)) for x in script  ]
    script = ([x for x in script if x!= "" ])
    lines = list_to_gen(script)
    for line in lines:
        tokens = line.lstrip(" ").split(" ")
        # tokens = split(line)
        # print(">>> ",tokens)
        if tokens == [""]:
            continue
        elif tokens[0] == "import":
            file_name = tokens[1]
            output.append(parse(file_name,files))
            # print(f"importing {file_name}")
        elif tokens[0] == "macro":
            # print(f"found macro {line}")
            args = split(line)[1:]
            macros[tokens[1]]=macro(args,getBlock(lines).strip("{}"))
        elif tokens[0] in macros.keys():
            mline = split(line)
            # print(f"found {mline}")
            # print(macros[tokens[0]].args)
            mac = macros[tokens[0]]
            output.append(mac.run(mline,lines))
        elif tokens[0] == "block_macro":
            # print(f"found block macro {line}")
            args = split(line)[1:]
            macros[tokens[1]]=macro(args,getBlock(lines).strip("{}"),block=True)
        elif tokens[0] == "runtime":
            # print("found runtime")
            
            b = getBlock(lines).strip("{}")
            # print("========")
            # print(b)
            # print("========")
            output.append(parse(text=eval(b)))
            
        else:
            output.append(line)

    output = ([x for x in output if x!= "" ])
    return "\n".join(output)


if len(argv) >1:
    print(parse(argv[1]))
else:
    print(parse("storm"))
# print(parse("strings"))
# parse("storm")
