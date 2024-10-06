
import dataclasses as dc
import re
import sys

from ply import lex

# ====================================================================
# BX lexer definition

class Lexer:

    reserved = {'print', 'int', 'def', 'main', 'var', 'int', 'bool', 'true', 'false'}
    reserved = { x: x.upper() for x in reserved }

    tokens = (                 
    'AND', 
    'B_AND',
    'B_NEG',
    'B_OR',
    'COLON',
    'DIV', 
    'EQ', 
    'IDENT', 
    'IS_EQ',
    'IS_G',
    'IS_GE',
    'IS_L',
    'IS_LE',
    'IS_NEQ',
    'LBRACE',
    'LPAREN',  
    'MINUS', 
    'MOD', 
    'NEG', 
    'NUMBER', 
    'OR', 
    'PLUS', 
    'RBRACE',
    'RPAREN',  
    'SEMICOLON',
    'SHL', 
    'SHR', 
    'TIMES',  
    'XOR'
    ) + tuple(reserved.values())

    t_AND = re.escape('&')
    t_B_AND = re.escape('&&')
    t_B_NEG = re.escape('!')
    t_B_OR = re.escape('||')
    t_COLON = re.escape(':')
    t_DIV  = re.escape('/')
    t_EQ     = re.escape('=')
    t_IS_EQ = re.escape('==')
    t_IS_G = re.escape('>')
    t_IS_GE = re.escape('>=')
    t_IS_L = re.escape('<')
    t_IS_LE = re.escape('<=')
    t_IS_NEQ = re.escape('!=')
    t_LBRACE = re.escape('{')
    t_LPAREN = re.escape('(')
    t_MINUS = re.escape('-')
    t_MOD = re.escape('%')
    t_NEG = re.escape('~')
    t_OR = re.escape('|')
    t_PLUS = re.escape('+')
    t_RBRACE = re.escape('}')
    t_RPAREN = re.escape(')')
    t_SEMICOLON = re.escape(';')
    t_SHL = re.escape('<<')
    t_SHR = re.escape('>>')
    t_TIMES  = re.escape('*')
    t_XOR = re.escape('^')


    # Regular expression + processing for tokens with a semantic value
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    def t_BOOL(self,t):
        r'true|false'
        return t

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if t.value in self.reserved:
            t.type  = self.reserved[t.value]
            t.value = None #change the type for reserved values (keywords)
        return t

    def t_error(self, t):
        print(f"illegal character: `{t.value[0]}'", file = sys.stderr)
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'

    t_ignore = ' \t'            # Ignore all whitespaces
    t_ignore_comment = r'//.*'


    @classmethod
    def build(cls, **kw):
        instance = cls()
        instance.lexer = lex.lex(module = instance, **kw)
        return instance

    
    

    
