
from .bxast import *
from .lexer  import Lexer

from ply import yacc

import sys

# ====================================================================
# BX parser definition

class Parser:
    UNIOP = {
        '-' : 'opposite'        ,
        '~' : 'bitwise-negation',
        '!' : 'boolean_negation'
    }

    BINOP = {
        '+'  : 'addition'           ,
        '-'  : 'subtraction'        ,
        '*'  : 'multiplication'     ,
        '/'  : 'division'           ,
        '%'  : 'modulus'            ,
        '>>' : 'logical-right-shift',
        '<<' : 'logical-left-shift' ,
        '&'  : 'bitwise-and'        ,
        '|'  : 'bitwise-or'         ,
        '^'  : 'bitwise-xor'        ,
        '==' : 'is_equal_to'        ,
        '!=' : 'is_not_equal_to'    ,
        '<'  : 'is_lower_than'       ,
        '<=' : 'is_lower_than_or_equal' ,
        '>'  : 'is_greater_than'      ,
        '>=' : 'is_greater_than_or_equal',
        '&&' : 'boolean_and',
        '||' : 'booelan_or' }

    tokens = Lexer.tokens
    
    start = 'prgm'

    precedence = (
                ('left', 'B_OR'),
                ('left', 'B_AND'),
                ('left', 'OR'),
                ('left', 'XOR'),
                ('left', 'AND'),
                ('nonassoc', 'IS_EQ', 'IS_NEQ'),
                ('nonassoc', 'IS_L', 'IS_LE','IS_G', 'IS_GE'),
                ('left', 'SHR', 'SHL'),
                ('left', 'PLUS','MINUS'), # left-assoc., low precedence
                ('left', 'TIMES', 'DIV', 'MOD'), # left-assoc., medium precedence
                ('right', 'UMINUS', 'B_NEG'), # right-assoc., high precedence
                ('right', 'NEG'))
    
     
    def p_expr_var(self, p):
        """expr : IDENT""" 
        p[0] = ExpressionVar(name = p[1])

    def p_expr_int(self, p):
        """expr : NUMBER"""
        p[0] = ExpressionInt(value = p[1])

    def p_expr_bool(self,p):
        """expr : BOOL"""
        p[0] = ExpressionBool(value = p[1])

    def p_expr_uniop(self,p):
        """expr : MINUS expr %prec UMINUS
                | NEG expr
                | B_NEG expr"""
        p[0] = ExpressionUniOp(self.UNIOP[p[1]], p[2])

    def p_expr_binop(self,p):
        """expr : expr PLUS  expr
        | expr MINUS expr
        | expr TIMES  expr
        | expr DIV expr
        | expr MOD expr
        | expr SHR expr
        | expr SHL expr
        | expr AND expr
        | expr OR expr
        | expr XOR expr

        | expr IS_EQ expr
        | expr IS_NEQ expr
        | expr IS_L expr
        | expr IS_LE expr
        | expr IS_G expr
        | expr IS_GE expr
        
        | expr B_AND expr
        | expr B_OR expr
        """
        p[0] = ExpressionBinOp(self.BINOP[p[2]], p[1], p[3])

    def p_expression_group(self, p):
        """expr : LPAREN expr RPAREN"""
        p[0] = p[2]
    
    def p_stmt_vardecl(self, p):
        """stmt : VAR IDENT EQ expr COLON INT SEMICOLON"""
        p[0] = StatementVarDecl(p[2], p[4])

    def p_stmt_print(self, p):
        """stmt : PRINT LPAREN expr RPAREN SEMICOLON"""
        p[0] = StatementEval(p[3])
    
    def p_stmt_assign(self, p):
        """stmt : IDENT EQ expr SEMICOLON"""
        p[0] = StatementAssign(p[1] , p[3])

    def p_stmts(self, p):
        """stmts :
                 | stmts stmt"""
        if len(p) == 1: # empty case
            p[0] = []
        else: # nonempty case
            p[0] = p[1]
            p[0].append(p[2])

    def p_stmt(self, p):
        """stmts : stmts error SEMICOLON"""
        p[0] = p[1]

    def p_prgm(self, p):
        """prgm : DEF MAIN LPAREN RPAREN LBRACE stmts RBRACE"""
        p[0] = p[6]

    def p_error(self,p):
        print("Error while parsing ", p)


    @classmethod
    def build(cls):
        instance = cls()
        instance.parser = yacc.yacc(module = instance)
        instance.lexer  = Lexer.build()
        return instance

    @classmethod
    def parse(cls, program : str):
        instance = cls.build()

        ast = instance.parser.parse(
            program,
            lexer    = instance.lexer.lexer,
            tracking = True,
        )

        return ast
