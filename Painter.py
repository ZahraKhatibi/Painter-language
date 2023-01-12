import json
name_func = ["if",3,"drawLine",7,"drawCircle",6,"drawPoint",5,"drawEllipse",7]

def funcrunner(entrance): 
    name = ""
    i = 0
    while entrance[i] != "(" : 
        name += entrance[i]
        i += 1
    i+= 1 
    if name not in name_func:
        return("Error, tabe tarif nashodast $")

    result='{ "type" : "function call" , "function name" : "%s" , "args" : [' %(name)
    part1 = ""
    m = 0
    lst = []
    for  char_arg in entrance[i:-1]:
        if char_arg == "(":
            m += 1
        elif char_arg == ")":
            m -= 1
        if m == 0 and char_arg == ",":
            lst.append(part1)
            part1 = ""
        else:
            part1 += char_arg
    lst.append(part1)
    w = name_func.index(name)
    if len(lst) != name_func[w+1]:
        return("Error, tedad argomanhaye vorodi eshtebah ast $")

    for i in lst :
        if i == "":
            return("Error, expression khali ast $")
        result += expression(i) + ","
    result = result[:-1] + "]}"
    return result

def expression(entrance):
    part2 = ""
    lst = []
    q = 0
    for char in entrance:
        if char == "(" : 
            q += 1
        if char == ")" :
            q -= 1
        if char in "+-%*/" and q==0 :
            lst.append(part2)
            part2=""
            lst.append(char)
            continue
        part2 += char

    lst.append(part2)
    if len(lst)==1: 
        if "(" in lst[0]: 
            return funcrunner(lst[0])

        else:
            try : return str(int(lst[0]))
            except : return '"%s"'%(lst[0])
    else:
        result = ""
        part3 = ""
        for i in lst[2:]:
            part3 += i
        result += '{"type":"%s","A":%s,"B":%s}' %(lst[1],expression(lst[0]),expression(part3)) 
        return result

def func_def(entrance):
    i = 4
    name = ""
    while entrance[i] != "(":
        name += entrance[i]
        i += 1
    i += 1
    result = '{"type": "function definition","function name":"%s","args":[' %(name)
    if name in name_func:
        return("Error, tabe tekrari ast $")

    name_func.append(name)
    argomans = ""
    while entrance[i]!= ")":
        argomans += entrance[i]
        i += 1
    i += 1
    argomanlst = list(argomans.split(","))

    for arg in argomanlst:
        result+= '"' + arg + '",'
    result = result[:-1] + "]," + '"expression":'
    name_func.append(len(argomanlst))
    result += expression(entrance[i:]) 
    return result + "}"

def r_func_def(entrance1,entrance2,entrance3): 
    i = 5 
    name = ""
    argomans = ""
    while entrance1[i] != "(":
        name += entrance1[i]
        i += 1
    i += 1 
    result = '{"type": "recursive function definition", "function name": "%s", "args" : [' %(name)

    while entrance1[i] != ")" : 
        argomans += entrance1[i]
        i += 1
    i += 1 
    argomanslst = list(argomans.split(","))
    if len(argomanslst)!= 1: 
        for arg in argomanslst[:-1]:
                result += '"' + arg + '",'
        result = result[:-1] + '],' + '"recursive arg" : "%s" , "base expression" : %s ,"recursive expression": %s }' %(argslst[-1], expression(entrance2[1:]) , expression(entrance3[1:]))
    else: 
        result = result + '],' + '"recursive arg" : "%s" , "base expression" : %s ,"recursive expression": %s }' %(argslst[-1], expression(entrance2[1:]) , expression(entrance3[1:]))
    return result

def main():
    f = open("input.sp")
    s = f.read()
    f.close()
    s = '100 200\n func haa(m,n)m+n \n func main() drawCircle(0,0,150,15,15,15)'
    lines = list(s.split("\n"))
    try:
        lines.remove("") 
    except:
        pass

    try:
        h, w = lines[0].split()
    except:
        return ("Error")
    
    result = '{"height":' + h + ',"width":' + w + ',"functions":['

    line = 1
    while line < len(lines): 
        lines[line]=lines[line].replace(" ","")
        line+=1

    line=1
    while line < len(lines):
        if lines[line][:4] == "func":
            result += func_def(lines[line]) + ","
        elif lines[line][:5] == "rfunc": 
            result += r_func_def(lines[line], lines[line + 1], lines[line + 2]) + ","
            line+=2                               
        else:
            return ("Error, at the first line, we should write $")
        line+=1
    result = result[:-1]+']}'

    print(result)
    if "main" not in name_func:
        return("Error, Main function doesn't exit")

    if "Error" in result:
        X = result.index("Error")
        Y = result.index("$")
        return("Error \n %s") %(result[X+5:Y])
    return result
print(json.dumps(json.loads((main())),indent=2))
print(main())

#*******************************************************************************#

from turtle import *
import json
from math import sin,cos,pi

entrance = main() 
entrance = json.loads(entrance) 
t = Turtle() 
screen = Screen()
screen.screensize(entrance["height"],entrance["width"])
screen.colormode(255)
entrance = entrance["functions"]
funcdict = {}

for func in entrance:
    funcdict[func["function name"]] = func
def argomans(arg): 
    try:
        arg=int(arg)
    except:
        pass
    if type(arg) == type(1):
        return arg
    elif arg['type'] == 'function call':
        return perform_func(arg['function name'], arg['args'])
    else:
        if arg['type'] == '+':
            return  argomans(arg['A']) +  argomans(arg['B'])
        elif arg['type'] == '-':
            return  argomans(arg['A']) -  argomans(arg['B'])
        elif arg['type'] == '*':
            return  argomans(arg['A']) *  argomans(arg['B'])
        elif arg['type'] == '/':
            return  argomans(arg['A']) /  argomans(arg['B'])
        elif arg['type'] == '%':
            return  argomans(arg['A']) %  argomans(arg['B'])

def perform_r_func(fulldict,args):
    base = str(fulldict['base expression'])
    rec = str(fulldict['recursive expression'])
    i=0
    while i<len(args)-1:
        base=base.replace("'"+fulldict['args'][i]+"'",str(argomans(args[i])))
        i+=1
    base = base.replace("'",'"')
    base = json.loads(base)
    r = argomans(base)
    i=0
    while i < len(args) - 1:
        rec=rec.replace("'"+fulldict['args'][i]+"'",str(argomans(args[i])))
        i+=1
    
    for i in range(1,argomans(args[-1])+1):
        rec2 = rec.replace("'r'", str(r))
        rec2 = rec2.replace("'n'",str(i))
        rec2 = rec2.replace("'",'"')
        rec2 = json.loads(rec2)
        r = argomans(rec2)
        rec2 = str(rec2)
    return r

def perform_func(name,args):
    finarg = {}
    i=0
    global t
    if name == "if":
        if  argomans(args[0]) != 0: 
            return  argomans(args[1])
        else:
            return  argomans(args[2])
    if name == "drawLine":
        t.penup()
        t.goto( argomans(args[0]), argomans(args[1]))
        t.pencolor(argomans(args[4]),argomans(args[5]), argomans(args[6]))
        t.pendown()
        t.goto(argomans(args[2]),argomans(args[3]))
        return 0

    elif name=="drawPoint":
        t.pencolor( argomans(args[2]), argomans(args[3]), argomans(args[4]))
        t.penup()
        t.goto( argomans(args[0]), argomans(args[1]))
        t.pendown()
        t.circle(1)
        return 0

    elif name=="drawCircle":
        t.penup()
        t.goto( argomans(args[0]), argomans(args[1])- argomans(args[2]))
        t.pencolor( argomans(args[3]), argomans(args[4]), argomans(args[5]))
        t.pendown()
        t.circle( argomans(args[2]))
        return 0

    elif name=="Ellipse":
        def ellipse(t, x, y, w, h,r,g,b):
            t.penup()
            t.pencolor(r,g,b)
            t.goto(x + w / 2, y + h / 2)
            t.pendown()
            penx, peny = t.pos()
            for i in range(360):
                penx += cos(i * pi / 180) * w / 180
                peny += sin(i * pi / 180) * h / 180
                t.goto(penx, peny)
            t.penup()
            return 0
        return ellipse(t, argomans(args[0]), argomans(args[1]), argomans(args[2]), argomans(args[3]), argomans(args[4]),  argomans(args[5]), argomans(args[6]))

    if funcdict[name]['type']=="recursive function definition":
        return perform_r_func(name,args)

    entrance = str(funcdict[name]['expression'])
    while i < len(args):
        entrance = entrance.replace("'"+funcdict[name]['args'][i]+"'",str( argomans(args[i])))
        i += 1

    result = ''
    for i in entrance:
        if i!="'":
            result += i
        else:
            result += '"'
    entrance = result
    entrance = json.loads(entrance)
    return  argomans(entrance)
print(perform_func('main',[]))
getscreen().getcanvas().postscript(file="img.ps")