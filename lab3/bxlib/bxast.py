
# -------------------------------------------------------------------
#LAB 1 _____________________________________________________________________________________________________
# Parse tree / Abstract Syntax Tree


class AST:
    pass


#define the classes

class Expression(AST):
    pass


class ExpressionVar(Expression):

    def __init__(self, name : str):
        self.name = name

class ExpressionInt(Expression):

    def __init__(self, value : int):
        self.value = value

class ExpressionUniOp(Expression):  
    #operators : "opposite", "bitwise-negation"

    def __init__(self, operator : str, argument : Expression):
        self.dict = {'opposite' : 'neg',
                         'bitwise-negation' : 'not'}
        self.operator = self.dict[operator]
        self.argument = argument


class ExpressionBinOp(Expression):  
    # operators : "addition", "subtraction", "multiplication", "division", "modulus",
    # "bitwise-xor", "bitwise-or", "bitwise-and", 'logical-left-shift', 'logical-right-shift'

    def __init__(self, operator : str, left : Expression, right : Expression):
        self.operator = self.dict[operator]
        self.left = left
        self.right = right
        self.dict = {'addition' : 'add',
                    'subtraction' : 'sub',
                    'multiplication':'mul',
                    'division': 'div',
                    'modulus': 'mod',
                    'logical-right-shift': 'shr',
                    'logical-left-shift': 'shl' ,
                    'bitwise-and': 'and',
                    'bitwise-or': 'or',
                    'bitwise-xor': 'xor'}


class Statement:
    pass


class StatementVarDecl(Statement): #declare variables initially
    #only name varies here, type and init are fixed to respectively int , 0

    def __init__(self, name : str):
        self.name = name

class StatementAssign(Statement):

    def __init__(self, lvalue :str , rvalue : Expression):
        self.lvalue = lvalue
        self.rvalue = rvalue


class StatementEval(Statement):

    def __init__(self, expression : Expression):
        self.expression = expression
    
Program = list[Statement]
Block   = list[Statement]


