"""
PHASE 2: SYNTAX ANALYZER (PARSER)
Recursive Descent Parser - builds AST from tokens
"""

from lexer import TokenType
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
        self.errors = []
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
    
    def peek(self, offset=1):
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def expect(self, token_type):
        if self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        else:
            self.error(f"Expected {token_type.name}, got {self.current_token.type.name}")
            return None
    
    def error(self, message):
        line = self.current_token.line if self.current_token else "EOF"
        self.errors.append(f"Syntax Error at line {line}: {message}")
    
    def parse(self):
        # Parse function declarations first
        functions = []
        while self.current_token.type == TokenType.FUNC:
            func = self.parse_function_decl()
            if func:
                functions.append(func)
        
        # Parse main program statements
        statements = self.parse_stmt_list()
        
        if self.current_token.type != TokenType.EOF:
            self.error("Unexpected tokens after program end")
        
        return Program(functions, statements)
    
    def parse_stmt_list(self):
        statements = []
        while self.current_token.type not in [TokenType.EOF, TokenType.RBRACE]:
            stmt = self.parse_stmt()
            if stmt:
                statements.append(stmt)
            else:
                # Error recovery: skip to next semicolon or brace
                while self.current_token.type not in [TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF]:
                    self.advance()
                if self.current_token.type == TokenType.SEMICOLON:
                    self.advance()
        return statements
    
    def parse_stmt(self):
        token_type = self.current_token.type
        
        if token_type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR]:
            return self.parse_decl_stmt()
        elif token_type == TokenType.IDENTIFIER:
            # Could be assignment or function call statement
            if self.peek() and self.peek().type == TokenType.LPAREN:
                # Function call as statement
                line = self.current_token.line
                func_call = self.parse_function_call()
                self.expect(TokenType.SEMICOLON)
                return func_call
            else:
                return self.parse_assign_stmt()
        elif token_type == TokenType.IF:
            return self.parse_if_stmt()
        elif token_type == TokenType.LOOP:
            return self.parse_loop_stmt()
        elif token_type == TokenType.SHOW:
            return self.parse_print_stmt()
        elif token_type == TokenType.TELL:
            return self.parse_input_stmt()
        elif token_type == TokenType.RETURN:
            return self.parse_return_stmt()
        elif token_type == TokenType.LBRACE:
            return self.parse_block()
        else:
            self.error(f"Unexpected token {token_type.name}")
            return None
    
    def parse_decl_stmt(self):
        line = self.current_token.line
        var_type = self.current_token.value
        self.advance()
        
        if not self.expect(TokenType.IDENTIFIER):
            return None
        identifier = self.tokens[self.pos - 1].value
        
        init_value = None
        if self.current_token.type == TokenType.ASSIGN:
            self.advance()
            init_value = self.parse_expr()
        
        self.expect(TokenType.SEMICOLON)
        return DeclStmt(var_type, identifier, init_value, line)
    
    def parse_assign_stmt(self):
        line = self.current_token.line
        identifier = self.current_token.value
        self.advance()
        
        if not self.expect(TokenType.ASSIGN):
            return None
        
        expr = self.parse_expr()
        self.expect(TokenType.SEMICOLON)
        return AssignStmt(identifier, expr, line)
    
    def parse_if_stmt(self):
        line = self.current_token.line
        self.advance()  # consume 'if'
        
        if not self.expect(TokenType.LPAREN):
            return None
        condition = self.parse_condition()
        if not self.expect(TokenType.RPAREN):
            return None
        
        if_block = self.parse_block()
        
        elif_parts = []
        while self.current_token.type == TokenType.ELIF:
            self.advance()
            if not self.expect(TokenType.LPAREN):
                break
            elif_cond = self.parse_condition()
            if not self.expect(TokenType.RPAREN):
                break
            elif_block = self.parse_block()
            elif_parts.append((elif_cond, elif_block))
        
        else_block = None
        if self.current_token.type == TokenType.ELSE:
            self.advance()
            else_block = self.parse_block()
        
        return IfStmt(condition, if_block, elif_parts, else_block, line)
    

    
    def parse_print_stmt(self):
        line = self.current_token.line
        self.advance()  # consume 'show'
        
        # Parse expression list (comma-separated)
        expressions = []
        expressions.append(self.parse_expr())
        
        while self.current_token.type == TokenType.COMMA:
            self.advance()  # consume ','
            expressions.append(self.parse_expr())
        
        self.expect(TokenType.SEMICOLON)
        return PrintStmt(expressions, line)
    
    def parse_input_stmt(self):
        line = self.current_token.line
        self.advance()  # consume 'tell'
        
        if not self.expect(TokenType.IDENTIFIER):
            return None
        identifier = self.tokens[self.pos - 1].value
        
        self.expect(TokenType.SEMICOLON)
        return InputStmt(identifier, line)
    
    def parse_block(self):
        if not self.expect(TokenType.LBRACE):
            return None
        
        statements = self.parse_stmt_list()
        
        if not self.expect(TokenType.RBRACE):
            return None
        
        return Block(statements)
    
    def parse_condition(self):
        return self.parse_logical_or()
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        
        while self.current_token.type == TokenType.OR:
            op = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right, line)
        
        return left
    
    def parse_logical_and(self):
        left = self.parse_relational()
        
        while self.current_token.type == TokenType.AND:
            op = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_relational()
            left = BinaryOp(left, op, right, line)
        
        return left
    
    def parse_relational(self):
        if self.current_token.type == TokenType.NOT:
            op = self.current_token.value
            line = self.current_token.line
            self.advance()
            operand = self.parse_relational()
            return UnaryOp(op, operand, line)
        
        if self.current_token.type == TokenType.LPAREN:
            self.advance()
            cond = self.parse_condition()
            self.expect(TokenType.RPAREN)
            return cond
        
        left = self.parse_expr()
        
        if self.current_token.type in [TokenType.EQ, TokenType.NEQ, TokenType.LT, 
                                        TokenType.GT, TokenType.LTE, TokenType.GTE]:
            op = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_expr()
            return BinaryOp(left, op, right, line)
        
        return left
    
    def parse_expr(self):
        return self.parse_additive()
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right, line)
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        
        while self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.current_token.value
            line = self.current_token.line
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right, line)
        
        return left
    
    def parse_unary(self):
        if self.current_token.type == TokenType.MINUS:
            op = self.current_token.value
            line = self.current_token.line
            self.advance()
            operand = self.parse_unary()
            return UnaryOp(op, operand, line)
        
        return self.parse_primary()
    
    def parse_primary(self):
        token = self.current_token
        
        if token.type == TokenType.IDENTIFIER:
            # Check if it's a function call
            if self.peek() and self.peek().type == TokenType.LPAREN:
                return self.parse_function_call()
            else:
                self.advance()
                return Identifier(token.value, token.line)
        
        elif token.type == TokenType.INTEGER_LITERAL:
            self.advance()
            return Literal(token.value, 'int', token.line)
        
        elif token.type == TokenType.FLOAT_LITERAL:
            self.advance()
            return Literal(token.value, 'float', token.line)
        
        elif token.type == TokenType.CHAR_LITERAL:
            self.advance()
            return Literal(token.value, 'char', token.line)
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            self.error(f"Unexpected token in expression: {token.type.name}")
            return None

    def parse_function_decl(self):
        """Parse function declaration"""
        line = self.current_token.line
        self.advance()  # consume 'func'
        
        # Return type
        if self.current_token.type not in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR, TokenType.VOID]:
            self.error("Expected return type (int, float, char, or void)")
            return None
        return_type = self.current_token.value
        self.advance()
        
        # Function name
        if not self.expect(TokenType.IDENTIFIER):
            return None
        func_name = self.tokens[self.pos - 1].value
        
        # Parameters
        if not self.expect(TokenType.LPAREN):
            return None
        
        parameters = self.parse_param_list()
        
        if not self.expect(TokenType.RPAREN):
            return None
        
        # Function body
        body = self.parse_block()
        
        return FunctionDecl(return_type, func_name, parameters, body, line)
    
    def parse_param_list(self):
        """Parse function parameter list"""
        parameters = []
        
        if self.current_token.type in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR]:
            param = self.parse_param()
            if param:
                parameters.append(param)
            
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                param = self.parse_param()
                if param:
                    parameters.append(param)
        
        return parameters
    
    def parse_param(self):
        """Parse a single parameter"""
        if self.current_token.type not in [TokenType.INT, TokenType.FLOAT, TokenType.CHAR]:
            self.error("Expected parameter type")
            return None
        
        param_type = self.current_token.value
        self.advance()
        
        if not self.expect(TokenType.IDENTIFIER):
            return None
        param_name = self.tokens[self.pos - 1].value
        
        return (param_type, param_name)
    
    def parse_function_call(self):
        """Parse function call"""
        line = self.current_token.line
        func_name = self.current_token.value
        self.advance()
        
        if not self.expect(TokenType.LPAREN):
            return None
        
        arguments = self.parse_arg_list()
        
        if not self.expect(TokenType.RPAREN):
            return None
        
        return FunctionCall(func_name, arguments, line)
    
    def parse_arg_list(self):
        """Parse function call arguments"""
        arguments = []
        
        if self.current_token.type != TokenType.RPAREN:
            arg = self.parse_expr()
            if arg:
                arguments.append(arg)
            
            while self.current_token.type == TokenType.COMMA:
                self.advance()
                arg = self.parse_expr()
                if arg:
                    arguments.append(arg)
        
        return arguments
    
    def parse_return_stmt(self):
        """Parse return statement"""
        line = self.current_token.line
        self.advance()  # consume 'return'
        
        expression = None
        if self.current_token.type != TokenType.SEMICOLON:
            expression = self.parse_expr()
        
        self.expect(TokenType.SEMICOLON)
        return ReturnStmt(expression, line)

    def parse_loop_stmt(self):
        """Parse loop statement - either range-based or conditional"""
        line = self.current_token.line
        self.advance()  # consume 'loop'
        
        # Check if it's a conditional loop: loop (condition) {}
        if self.current_token.type == TokenType.LPAREN:
            self.advance()  # consume '('
            condition = self.parse_condition()
            if not self.expect(TokenType.RPAREN):
                return None
            block = self.parse_block()
            # Return a conditional loop (while-style)
            return ConditionalLoopStmt(condition, block, line)
        
        # Otherwise, it's a range-based loop: loop from ... to ...
        # Expect 'from'
        if not self.expect(TokenType.FROM):
            return None
        
        # Variable name
        if not self.expect(TokenType.IDENTIFIER):
            return None
        var_name = self.tokens[self.pos - 1].value
        
        # Check if next token is '=' or 'to'
        use_existing_var = False
        start_expr = None
        
        if self.current_token.type == TokenType.ASSIGN:
            # New syntax: loop from i = 0 to 10
            self.advance()  # consume '='
            start_expr = self.parse_expr()
        elif self.current_token.type == TokenType.TO:
            # New syntax: loop from i to 10 (uses existing variable)
            use_existing_var = True
        else:
            self.error(f"Expected '=' or 'to' after loop variable")
            return None
        
        # Expect 'to'
        if not self.expect(TokenType.TO):
            return None
        
        # End expression
        end_expr = self.parse_expr()
        
        # Optional 'step'
        step_expr = None
        if self.current_token.type == TokenType.STEP:
            self.advance()
            step_expr = self.parse_expr()
        
        # Block
        block = self.parse_block()
        
        return LoopStmt(var_name, start_expr, end_expr, step_expr, block, line, use_existing_var)
