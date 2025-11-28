"""
Abstract Syntax Tree (AST) Node Definitions
"""

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, functions, statements):
        self.functions = functions  # List of FunctionDecl
        self.statements = statements  # Main program statements

class DeclStmt(ASTNode):
    def __init__(self, var_type, identifier, init_value=None, line=0):
        self.var_type = var_type
        self.identifier = identifier
        self.init_value = init_value
        self.line = line

class AssignStmt(ASTNode):
    def __init__(self, identifier, expression, line=0):
        self.identifier = identifier
        self.expression = expression
        self.line = line

class IfStmt(ASTNode):
    def __init__(self, condition, if_block, elif_parts, else_block, line=0):
        self.condition = condition
        self.if_block = if_block
        self.elif_parts = elif_parts  # List of (condition, block) tuples
        self.else_block = else_block
        self.line = line

class LoopStmt(ASTNode):
    def __init__(self, var_name, start_expr, end_expr, step_expr, block, line=0, use_existing_var=False):
        self.var_name = var_name
        self.start_expr = start_expr  # Can be None if using existing variable
        self.end_expr = end_expr
        self.step_expr = step_expr  # Can be None (default 1)
        self.block = block
        self.line = line
        self.use_existing_var = use_existing_var  # True if variable already declared

class ConditionalLoopStmt(ASTNode):
    def __init__(self, condition, block, line=0):
        self.condition = condition
        self.block = block
        self.line = line

class PrintStmt(ASTNode):
    def __init__(self, expressions, line=0):
        self.expressions = expressions  # List of expressions
        self.line = line

class InputStmt(ASTNode):
    def __init__(self, identifier, line=0):
        self.identifier = identifier
        self.line = line

class ReturnStmt(ASTNode):
    def __init__(self, expression=None, line=0):
        self.expression = expression
        self.line = line

class FunctionDecl(ASTNode):
    def __init__(self, return_type, name, parameters, body, line=0):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters  # List of (type, name) tuples
        self.body = body
        self.line = line

class FunctionCall(ASTNode):
    def __init__(self, name, arguments, line=0):
        self.name = name
        self.arguments = arguments  # List of expressions
        self.line = line
        self.return_type = None  # Set during semantic analysis

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right, line=0):
        self.left = left
        self.operator = operator
        self.right = right
        self.line = line
        self.result_type = None  # Set during semantic analysis

class UnaryOp(ASTNode):
    def __init__(self, operator, operand, line=0):
        self.operator = operator
        self.operand = operand
        self.line = line
        self.result_type = None

class Identifier(ASTNode):
    def __init__(self, name, line=0):
        self.name = name
        self.line = line
        self.var_type = None  # Set during semantic analysis

class Literal(ASTNode):
    def __init__(self, value, lit_type, line=0):
        self.value = value
        self.lit_type = lit_type  # 'int', 'float', 'char'
        self.line = line
