    
from .bxast import *

# Syntax-level checker

class SynChecker:
    def __init__(self):
        self.vars     = set()

    # check : <ExpressionVar> : Every variable is already declared with an earlier variable declaration
    #         <StatementAssign.lvalue> : The LHS should be a variable declared earlier
    def check_declared(self,name : str ): #->bool
        if name in self.vars:
            return True
        print(f"Error: Missing variable declaration for `{name}'")
        return False
    
    def check_free(self,name:str): #bool
        if name in self.vars:
            print(f"Error: Duplicate variable declaration for `{name}'")
            return False
        self.vars.add(name) #declaring the variable in the set
        return True
    
    #Every number must fit in 63 bits, i.e., its value needs to be in [0, 2^63]
    def check_range(self, value : int): #->bool
        if value in range(0, 1 << 63):
            return True
        print(f'Error: Integer literal out of range: {value}'),
        return False

    def for_expression(self, expr:Expression): #->bool
        if isinstance(expr, ExpressionVar):
            return self.check_declared(expr.name)
        elif isinstance(expr, ExpressionInt):
            return self.check_range(expr.value)
        elif isinstance(expr, ExpressionUniOp):
            return self.for_expression(expr.argument)
        elif isinstance(expr, ExpressionBinOp):
            return (self.for_expression(expr.left) & self.for_expression(expr.right))


    def for_statement(self, stmt:Statement): #->bool
        if isinstance(stmt, StatementAssign):
            return (self.check_declared(stmt.lvalue) & self.for_expression(stmt.rvalue))
        elif isinstance(stmt, StatementVarDecl):
            return (self.check_free(stmt.name) & self.for_expression(stmt.init))
        elif isinstance(stmt, StatementEval):
            return (self.for_expression(stmt.expression))


    def for_program(self, prgm : Program): #->bool
        # check that `prgm` is syntactical correct
        b = True
        for stmt in prgm:
            b &= self.for_statement(stmt)
        return b


    def check(self, prgm : Program):
        return self.for_program(prgm)
    
