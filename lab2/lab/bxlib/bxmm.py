from .bxast import *

# ====================================================================
# Maximal munch

class MM:
    def __init__(self):
        self.counter = 0
        self.temp    = {}
        self.tac = []

    @staticmethod
    def mm(prgm: Program):
        mm = MM()
        return mm.for_program(prgm)

    def for_program(self, prgm: Program):
        for stmt in prgm:
            self.for_statement(stmt)
        tac = [x for x in self.tac if x != None]
        pg = [dict(
            proc = '@main',
            body = tac,
        )]
        return pg




    def for_statement(self, stmt: Statement):

        if isinstance(stmt, StatementVarDecl):
            t_res = self.counter
            self.counter +=1
            self.temp[stmt.name] = t_res
            self.tac.append(self.for_expression(stmt.init, t_res))
        
        elif isinstance(stmt,StatementAssign):
            t_res = self.temp[stmt.lvalue] #get the temporary where to store the result
            self.tac.append(self.for_expression(stmt.rvalue , t_res))
        
        elif isinstance(stmt,StatementEval):
            t = self.counter  #generate a new temporary to print
            self.counter +=1 
            instr_exp = self.for_expression(stmt.expression , t) #get the instructions for the expression
            self.tac.append(instr_exp)
            self.tac.append({"opcode" : "print", "args": ["%"+str(t)], "result": None})

    def for_expression(self, expr: Expression , t_res : int):

        if isinstance(expr, ExpressionVar):
            t_stored = self.temp[expr.name]
            self.tac.append({"opcode": "copy", "args": ["%"+str(t_stored)], "result": "%"+str(t_res)})
        
        elif isinstance(expr, ExpressionInt):
            #returns the instruction which result is in the temporary t
            self.tac.append({"opcode": "const", "args": [expr.value], "result": "%"+str(t_res)})

        elif isinstance(expr, ExpressionBool):
            self.tac.append({"opcode": "const", "args": [0], "result": "%"+str(t_res)})
            
            #self.tac.append({"opcode": "const", "args": [0 or 1], "result": "%"+str(t_res)})
            
        elif isinstance(expr, ExpressionUniOp):
            t_arg = self.counter #generate a new temporary for the argument
            self.counter+=1
            instr_arg = self.for_expression(expr.argument , t_arg) #get the list of instructions for the argument
            opcode = expr.operator
            self.tac.append(instr_arg)
            self.tac.append({"opcode": str(opcode), "args": ["%"+str(t_arg)], "result": "%"+str(t_res)})

        elif isinstance(expr, ExpressionBinOp):
            t_l = self.counter #generate a new temporary for the left argument
            t_r = self.counter+1 #generate a new temporary for the right argument
            self.counter+=2
            instr_left = self.for_expression(expr.left, t_l) #get the list of instructions for the left argument
            instr_right = self.for_expression(expr.right, t_r) #get the list of instructions for the right argument
            opcode = expr.operator
            self.tac.append(instr_left)
            self.tac.append(instr_right)
            self.tac.append({"opcode": str(opcode), "args": ["%"+str(t_l), "%"+str(t_r)], "result": "%"+str(t_res)})



