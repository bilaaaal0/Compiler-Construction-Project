"""
PHASE 1: LEXICAL ANALYZER (LEXER)
Converts source code into tokens
"""

import re
from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    INT = auto()
    FLOAT = auto()
    CHAR = auto()
    VOID = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    LOOP = auto()
    FROM = auto()
    TO = auto()
    STEP = auto()
    SHOW = auto()
    TELL = auto()
    RETURN = auto()
    FUNC = auto()
    
    # Identifiers and Literals
    IDENTIFIER = auto()
    INTEGER_LITERAL = auto()
    FLOAT_LITERAL = auto()
    CHAR_LITERAL = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.errors = []
        
        self.keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'char': TokenType.CHAR,
            'void': TokenType.VOID,
            'if': TokenType.IF,
            'elif': TokenType.ELIF,
            'else': TokenType.ELSE,
            'loop': TokenType.LOOP,
            'from': TokenType.FROM,
            'to': TokenType.TO,
            'step': TokenType.STEP,
            'show': TokenType.SHOW,
            'tell': TokenType.TELL,
            'return': TokenType.RETURN,
            'func': TokenType.FUNC,
        }
    
    def current_char(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset=1):
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        # Single line comment: //
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            return True
        return False
    
    def read_number(self):
        start_col = self.column
        num_str = ''
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    self.errors.append(f"Lexical Error at {self.line}:{self.column}: Invalid number format")
                    break
                is_float = True
            num_str += self.current_char()
            self.advance()
        
        if is_float:
            return Token(TokenType.FLOAT_LITERAL, float(num_str), self.line, start_col)
        else:
            return Token(TokenType.INTEGER_LITERAL, int(num_str), self.line, start_col)
    
    def read_identifier(self):
        start_col = self.column
        id_str = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            id_str += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(id_str, TokenType.IDENTIFIER)
        return Token(token_type, id_str, self.line, start_col)
    
    def read_char_literal(self):
        start_col = self.column
        self.advance()  # Skip opening '
        
        if not self.current_char():
            self.errors.append(f"Lexical Error at {self.line}:{start_col}: Unterminated char literal")
            return None
        
        char_value = self.current_char()
        self.advance()
        
        if self.current_char() != "'":
            self.errors.append(f"Lexical Error at {self.line}:{start_col}: Char literal must be single character")
            return None
        
        self.advance()  # Skip closing '
        return Token(TokenType.CHAR_LITERAL, char_value, self.line, start_col)
    
    def tokenize(self):
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.skip_comment():
                continue
            
            char = self.current_char()
            col = self.column
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
            
            # Identifiers and Keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Char literals
            elif char == "'":
                token = self.read_char_literal()
                if token:
                    self.tokens.append(token)
            
            # Two-character operators
            elif char == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQ, '==', self.line, col))
                self.advance()
                self.advance()
            elif char == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NEQ, '!=', self.line, col))
                self.advance()
                self.advance()
            elif char == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LTE, '<=', self.line, col))
                self.advance()
                self.advance()
            elif char == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GTE, '>=', self.line, col))
                self.advance()
                self.advance()
            elif char == '&' and self.peek_char() == '&':
                self.tokens.append(Token(TokenType.AND, '&&', self.line, col))
                self.advance()
                self.advance()
            elif char == '|' and self.peek_char() == '|':
                self.tokens.append(Token(TokenType.OR, '||', self.line, col))
                self.advance()
                self.advance()
            
            # Single-character operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, col))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line, col))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, col))
                self.advance()
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, '%', self.line, col))
                self.advance()
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, col))
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LT, '<', self.line, col))
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GT, '>', self.line, col))
                self.advance()
            elif char == '!':
                self.tokens.append(Token(TokenType.NOT, '!', self.line, col))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, col))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, col))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, col))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, col))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, col))
                self.advance()
            
            else:
                self.errors.append(f"Lexical Error at {self.line}:{col}: Unknown character '{char}'")
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens, self.errors
