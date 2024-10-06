import json
import pprint
import sys


#global variables
temp = {}
counter = 0


#define the classes

class Expression:
    pass


class ExpressionVar(Expression):

    def __init__(self, name : str):
        self.name = name

    def get_instr(self, t_res : int): #returns the instruction which result is in the temporary t
        t_stored = temp[self.name]
        return f'\t   {{"opcode": "copy", "args": ["%{t_stored}"], "result": "%{t_res}"}},\n'


class ExpressionInt(Expression):

    def __init__(self, value : int):
        self.value = value

    def get_instr(self, t_res : int): #returns the instruction which result is in the temporary t
        return f'\t   {{"opcode": "const", "args": [{self.value}], "result": "%{t_res}"}},\n'


class ExpressionUniOp(Expression):  
    #operators : "opposite", "bitwise-negation"

    def __init__(self, operator : str, argument : Expression):
        self.operator = operator
        self.argument = argument
    
    def get_instr(self, t_res : int):
        global counter
        t_arg = counter #generate a new temporary for the argument
        counter+=1
        instr_arg = (self.argument).get_instr(t_arg) #get the list of instructions for the argument
        if self.operator == "opposite":
            opcode = "neg" #arithmetic negation
        else:
            opcode = "not" #bitwise negation
        return instr_arg + f'\t   {{"opcode": "{opcode}", "args": ["%{t_arg}"], "result": "%{t_res}"}},\n'


class ExpressionBinOp(Expression):  
    # operators : "addition", "substraction", "multiplication", "division", "modulus",
    # "bitwise-xor", "bitwise-or", "bitwise-and"

    def __init__(self, operator : str, left : Expression, right : Expression):
        self.operator = operator
        self.left = left
        self.right = right

    def get_instr(self, t_res : int):
        global counter
        t_l = counter #generate a new temporary for the left argument
        t_r = counter+1 #generate a new temporary for the right argument
        counter+=2
        instr_left = (self.left).get_instr(t_l) #get the list of instructions for the left argument
        instr_right = (self.right).get_instr(t_r) #get the list of instructions for the right argument
        if (self.operator)[0] == "b": #bit operations
            opcode = (self.operator)[8:] #"xor","or","and"
        else:
            opcode = (self.operator)[:3] # "add", "sub","mul","div","mod"
        return instr_left + instr_right  + f'\t   {{"opcode": "{opcode}", "args": ["%{t_l}", "%{t_r}"], "result": "%{t_res}"}},\n'


class Statement:
    pass


class StatementVarDecl(Statement): #declare variables initially
    #only name varies here, type and init are fixed to respectively int , 0

    def __init__(self, name : str):
        self.name = name

    def get_instr(self): #store in the dictionary the temporary corresponding to the variable
        global counter
        t = counter
        counter +=1
        temp[self.name] = t
        return ''

class StatementAssign(Statement):

    def __init__(self, lvalue :str , rvalue : Expression):
        self.lvalue = lvalue
        self.rvalue = rvalue

    def get_instr(self):
        t_res = temp[self.lvalue] #get the temporary where to store the result
        return self.rvalue.get_instr(t_res)


class StatementEval(Statement):

    def __init__(self, expression : Expression):
        self.expression = expression
    
    def get_instr(self):
        global counter
        t = counter  #generate a new temporary to print
        counter +=1 
        instr_exp = (self.expression).get_instr(t) #get the instructions for the expression
        return instr_exp + f'\t   {{"opcode" : "print", "args": ["%{t}"], "result": null}},\n'




#write a recursive loader function transforming a JSON object into 
# the corresponding element of the class hierarchy

def json_to_name(js_obj):
    return js_obj[1]['value']

def json_to_expr(js_obj):
    if js_obj[0] == '<expression:var>':
        name = json_to_name(js_obj[1]['name'])
        return ExpressionVar(name)
    if js_obj[0] == '<expression:int>':
        value = js_obj[1]['value']
        return ExpressionInt(value)
    if js_obj[0] == '<expression:uniop>':
        operator = json_to_name(js_obj[1]['operator'])
        argument = json_to_expr(js_obj[1]['argument']) # recursive call
        return ExpressionUniOp(operator, argument)
    if js_obj[0] == '<expression:binop>':
        operator = json_to_name(js_obj[1]['operator'])
        left = json_to_expr(js_obj[1]['left']) # recursive call
        right = json_to_expr(js_obj[1]['right']) # recursive call
        return ExpressionBinOp(operator, left , right)
    raise ValueError(f'Unrecognized <expression>: {js_obj[0]}')

def json_to_stat(js_obj):
    if js_obj[0] == '<statement:vardecl>':
        name = json_to_name(js_obj[1]['name'])
        return StatementVarDecl(name)
    if js_obj[0] == '<statement:assign>':
        lvalue = json_to_name(js_obj[1]['lvalue'][1]['name'])
        rvalue = json_to_expr(js_obj[1]['rvalue'])
        return StatementAssign(lvalue, rvalue)
    if js_obj[0] == '<statement:eval>': 
        expression = json_to_expr(js_obj[1]['expression'][1]['arguments'][0])
        return StatementEval(expression)
    raise ValueError(f'Unrecognized <statement>: {js_obj[0]}')



def transform_to_tac(data):

    body = data['ast'][0][1]['body']
    with open("astfile.json", 'w') as file:
        file.write('[ { "proc": "@main", \n\t"body": [\n')
        for x in body:
            if x == body[-1]:  #to get rid of the coma for the last instruction
                file.write((json_to_stat(x).get_instr())[:-2])
            else:
                file.write(json_to_stat(x).get_instr())
        file.write('\n\t]\n  }\n]')



def main():

    with open('bitops.bx.json', 'r') as stream:

    #with open(sys.argv[1], 'r') as stream:
        data = json.load(stream)

    transform_to_tac(data)


if __name__ == "__main__":
    main()




