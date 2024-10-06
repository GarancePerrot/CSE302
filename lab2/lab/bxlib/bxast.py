
# -------------------------------------------------------------------
#LAB 1 _____________________________________________________________________________________________________
# Parse tree / Abstract Syntax Tree

class Type:
    def __init__(self, ty):
        self.ty = ty

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

class ExpressionBool(Expression):
    def __init__(self, value:bool):
        self.value = value
    

class ExpressionUniOp(Expression):  
    #operators : "opposite", "bitwise-negation"

    OP =  {'opposite' : 'neg',
            'bitwise-negation' : 'not',
            'boolean_negation' : 'b_neg'}

    def __init__(self, operator : str, argument : Expression):
        self.operator = self.OP[operator]
        self.argument = argument


class ExpressionBinOp(Expression):  
    # operators : "addition", "subtraction", "multiplication", "division", "modulus",
    # "bitwise-xor", "bitwise-or", "bitwise-and", 'logical-left-shift', 'logical-right-shift'

    OP = {
        'addition' : 'add',
        'subtraction' : 'sub',
        'multiplication':'mul',
        'division': 'div',
        'modulus': 'mod',
        'logical-right-shift': 'shr',
        'logical-left-shift': 'shl' ,
        'bitwise-and': 'and',
        'bitwise-or': 'or',
        'bitwise-xor': 'xor',
        'is_equal_to' : 'is_eq',
        'is_not_equal_to' : 'is_neq' ,
        'is_lower_than' : 'is_l' ,
        'is_lower_than_or_equal' : 'is_le' ,
        'is_greater_than' : 'is_g',
        'is_greater_than_or_equal' : 'is_ge',
        'boolean_and' : 'b_and',
        'booelan_or' : 'b_or'
    }

    def __init__(self, operator : str, left : Expression, right : Expression):
        self.operator = self.OP[operator]
        self.left = left
        self.right = right


class Statement(AST):
    pass


class StatementVarDecl(Statement): #declare variables initially

    def __init__(self, name : str, init: Expression):
        self.name = name
        self.init = init

class StatementAssign(Statement):

    def __init__(self, lvalue :str , rvalue : Expression):
        self.lvalue = lvalue
        self.rvalue = rvalue


class StatementEval(Statement):

    def __init__(self, expression : Expression):
        self.expression = expression
    
Program = list[Statement]
Block   = list[Statement]


