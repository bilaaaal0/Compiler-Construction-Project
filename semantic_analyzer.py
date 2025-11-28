"""
PHASE 3: SEMANTIC ANALYZER
Type checking, scope management, declaration-before-use validation
"""

from ast_nodes import *
from symbol_table import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
    
    def error(self, message, line=0):
        self.errors.append(f"Semantic Error at line {line}: {message}")
    
    def has_return_statement(self, node):
        """Check if a block or statement contains a return statement"""
        if isinstance(node, ReturnStmt):
            return True
        elif isinstance(node, Block):
            for stmt in node.statements:
                if self.has_return_statement(stmt):
                    return True
        elif isinstance(node, IfStmt):
            # Check if all branches have return
            if self.has_return_statement(node.if_block):
                return True
            for _, elif_block in node.elif_parts:
                if self.has_return_statement(elif_block):
                    return True
            if node.else_block and self.has_return_statement(node.else_block):
                return True
        elif isinstance(node, LoopStmt) or isinstance(node, ConditionalLoopStmt):
            # Loops might have return statements
            if hasattr(node, 'block') and self.has_return_statement(node.block):
                return True
        return False
    
    def analyze(self, ast):
        self.visit(ast)
        return self.symbol_table, self.errors
    
    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method')
    
    def visit_Program(self, node):
        # First pass: register all functions
        for func in node.functions:
            param_types = [param[0] for param in func.parameters]
            success, result = self.symbol_table.insert(
                func.name,
                'function',
                func.line,
                initialized=True,
                is_function=True,
                param_types=param_types,
                return_type=func.return_type
            )
            if not success:
                self.error(result, func.line)
        
        # Second pass: analyze function bodies
        for func in node.functions:
            self.visit(func)
        
        # Analyze main program
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_DeclStmt(self, node):
        # Check if variable already declared in current scope
        success, result = self.symbol_table.insert(
            node.identifier, 
            node.var_type, 
            node.line,
            initialized=(node.init_value is not None)
        )
        
        if not success:
            self.error(result, node.line)
            return
        
        # Type check initialization if present
        if node.init_value:
            init_type = self.visit(node.init_value)
            if not self.is_type_compatible(node.var_type, init_type):
                self.error(
                    f"Type mismatch: cannot assign {init_type} to {node.var_type}",
                    node.line
                )
    
    def visit_AssignStmt(self, node):
        # Check if variable is declared
        entry = self.symbol_table.lookup(node.identifier)
        if not entry:
            self.error(f"Variable '{node.identifier}' not declared", node.line)
            return
        
        # Type check the expression
        expr_type = self.visit(node.expression)
        if not self.is_type_compatible(entry.var_type, expr_type):
            self.error(
                f"Type mismatch: cannot assign {expr_type} to {entry.var_type}",
                node.line
            )
        
        # Mark as initialized
        self.symbol_table.update_initialized(node.identifier)
    
    def visit_IfStmt(self, node):
        # Check condition
        self.visit(node.condition)
        
        # Visit if block
        self.symbol_table.enter_scope()
        self.visit(node.if_block)
        self.symbol_table.exit_scope()
        
        # Visit elif parts
        for elif_cond, elif_block in node.elif_parts:
            self.visit(elif_cond)
            self.symbol_table.enter_scope()
            self.visit(elif_block)
            self.symbol_table.exit_scope()
        
        # Visit else block
        if node.else_block:
            self.symbol_table.enter_scope()
            self.visit(node.else_block)
            self.symbol_table.exit_scope()
    
    def visit_LoopStmt(self, node):
        """Analyze loop from ... to ... step ... statement"""
        self.symbol_table.enter_scope()
        
        # Check if using existing variable or creating new one
        if node.use_existing_var:
            # Variable must already exist AND be initialized
            entry = self.symbol_table.lookup(node.var_name)
            if not entry:
                self.error(f"Loop variable '{node.var_name}' not declared", node.line)
            else:
                # Check if it's numeric type
                if entry.var_type not in ['int', 'float']:
                    self.error(f"Loop variable must be numeric, got {entry.var_type}", node.line)
                # Check if variable is initialized
                if not entry.initialized:
                    self.error(f"Loop variable '{node.var_name}' used before initialization", node.line)
                # Variable is already initialized, no need to mark again
        else:
            # Check if loop variable exists or create it
            entry = self.symbol_table.lookup(node.var_name)
            if not entry:
                # Auto-declare loop variable as int
                success, result = self.symbol_table.insert(
                    node.var_name,
                    'int',
                    node.line,
                    initialized=True
                )
                if not success:
                    self.error(result, node.line)
            
            # Check start expression type
            if node.start_expr:
                start_type = self.visit(node.start_expr)
                if start_type not in ['int', 'float']:
                    self.error(f"Loop start must be numeric, got {start_type}", node.line)
        
        # Check end expression type
        end_type = self.visit(node.end_expr)
        if end_type not in ['int', 'float']:
            self.error(f"Loop end must be numeric, got {end_type}", node.line)
        
        # Check step expression type (if provided)
        if node.step_expr:
            step_type = self.visit(node.step_expr)
            if step_type not in ['int', 'float']:
                self.error(f"Loop step must be numeric, got {step_type}", node.line)
        
        # Visit loop body
        self.visit(node.block)
        
        self.symbol_table.exit_scope()
    
    def visit_ConditionalLoopStmt(self, node):
        """Analyze conditional loop (while-style)"""
        self.symbol_table.enter_scope()
        
        # Check condition
        self.visit(node.condition)
        
        # Visit loop body
        self.visit(node.block)
        
        self.symbol_table.exit_scope()
    
    def visit_PrintStmt(self, node):
        # Visit all expressions in the print statement
        for expr in node.expressions:
            self.visit(expr)
    
    def visit_InputStmt(self, node):
        entry = self.symbol_table.lookup(node.identifier)
        if not entry:
            self.error(f"Variable '{node.identifier}' not declared", node.line)
        else:
            self.symbol_table.update_initialized(node.identifier)
    
    def visit_Block(self, node):
        # Enter new scope for block
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            self.visit(stmt)
        # Exit block scope
        self.symbol_table.exit_scope()
    
    def visit_BinaryOp(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        
        # Logical operators
        if node.operator in ['&&', '||']:
            node.result_type = 'bool'
            return 'bool'
        
        # Relational operators
        if node.operator in ['==', '!=', '<', '>', '<=', '>=']:
            if not self.are_types_comparable(left_type, right_type):
                self.error(
                    f"Cannot compare {left_type} and {right_type}",
                    node.line
                )
            node.result_type = 'bool'
            return 'bool'
        
        # Arithmetic operators
        if node.operator in ['+', '-', '*', '/', '%']:
            result_type = self.get_arithmetic_result_type(left_type, right_type)
            if result_type is None:
                self.error(
                    f"Invalid operands for {node.operator}: {left_type} and {right_type}",
                    node.line
                )
                return 'int'  # Default fallback
            node.result_type = result_type
            return result_type
        
        return 'int'
    
    def visit_UnaryOp(self, node):
        operand_type = self.visit(node.operand)
        
        if node.operator == '-':
            if operand_type not in ['int', 'float']:
                self.error(f"Cannot negate {operand_type}", node.line)
            node.result_type = operand_type
            return operand_type
        
        if node.operator == '!':
            node.result_type = 'bool'
            return 'bool'
        
        return operand_type
    
    def visit_Identifier(self, node):
        entry = self.symbol_table.lookup(node.name)
        if not entry:
            self.error(f"Variable '{node.name}' not declared", node.line)
            return 'int'  # Default fallback
        
        if not entry.initialized:
            self.error(f"Variable '{node.name}' used before initialization", node.line)
        
        node.var_type = entry.var_type
        return entry.var_type
    
    def visit_Literal(self, node):
        return node.lit_type
    
    def visit_FunctionDecl(self, node):
        """Analyze function declaration"""
        # Enter new scope for function
        self.symbol_table.enter_scope()
        self.symbol_table.current_function = node.name
        
        # Add parameters to function scope
        for param_type, param_name in node.parameters:
            success, result = self.symbol_table.insert(
                param_name,
                param_type,
                node.line,
                initialized=True
            )
            if not success:
                self.error(result, node.line)
        
        # Analyze function body
        self.visit(node.body)
        
        # Check if non-void function has return statement
        if node.return_type != 'void':
            if not self.has_return_statement(node.body):
                self.error(
                    f"Function '{node.name}' with return type '{node.return_type}' must have a return statement",
                    node.line
                )
        
        # Exit function scope
        self.symbol_table.current_function = None
        self.symbol_table.exit_scope()
    
    def visit_FunctionCall(self, node):
        """Analyze function call"""
        # Check if function is declared
        entry = self.symbol_table.lookup(node.name)
        if not entry:
            self.error(f"Function '{node.name}' not declared", node.line)
            return 'int'  # Default fallback
        
        if not entry.is_function:
            self.error(f"'{node.name}' is not a function", node.line)
            return 'int'
        
        # Check argument count
        if len(node.arguments) != len(entry.param_types):
            self.error(
                f"Function '{node.name}' expects {len(entry.param_types)} arguments, got {len(node.arguments)}",
                node.line
            )
        
        # Check argument types
        for i, arg in enumerate(node.arguments):
            arg_type = self.visit(arg)
            if i < len(entry.param_types):
                expected_type = entry.param_types[i]
                if not self.is_type_compatible(expected_type, arg_type):
                    self.error(
                        f"Argument {i+1} type mismatch: expected {expected_type}, got {arg_type}",
                        node.line
                    )
        
        # Set and return the function's return type
        node.return_type = entry.return_type
        return entry.return_type
    
    def visit_ReturnStmt(self, node):
        """Analyze return statement"""
        if self.symbol_table.current_function is None:
            self.error("Return statement outside of function", node.line)
            return
        
        # Get function entry
        func_entry = self.symbol_table.lookup(self.symbol_table.current_function)
        if not func_entry:
            return
        
        # Check return type
        if node.expression:
            return_type = self.visit(node.expression)
            # Void functions should not return a value
            if func_entry.return_type == 'void':
                self.error(
                    f"Void function '{func_entry.name}' should not return a value",
                    node.line
                )
            elif not self.is_type_compatible(func_entry.return_type, return_type):
                self.error(
                    f"Return type mismatch: expected {func_entry.return_type}, got {return_type}",
                    node.line
                )
        else:
            # Empty return - should only be in void functions
            if func_entry.return_type != 'void':
                self.error(
                    f"Function '{func_entry.name}' must return a value of type {func_entry.return_type}",
                    node.line
                )
    
    def is_type_compatible(self, target_type, source_type):
        """Check if source_type can be assigned to target_type"""
        if target_type == source_type:
            return True
        
        # Widening: int -> float is OK
        if target_type == 'float' and source_type == 'int':
            return True
        
        # char -> int is OK
        if target_type == 'int' and source_type == 'char':
            return True
        
        # Narrowing: float -> int is NOT OK
        if target_type == 'int' and source_type == 'float':
            return False
        
        return False
    
    def are_types_comparable(self, type1, type2):
        """Check if two types can be compared"""
        numeric_types = {'int', 'float', 'char'}
        if type1 in numeric_types and type2 in numeric_types:
            return True
        return type1 == type2
    
    def get_arithmetic_result_type(self, type1, type2):
        """Determine result type of arithmetic operation"""
        # char promoted to int
        if type1 == 'char':
            type1 = 'int'
        if type2 == 'char':
            type2 = 'int'
        
        # float + anything numeric = float
        if type1 == 'float' or type2 == 'float':
            if type1 in ['int', 'float'] and type2 in ['int', 'float']:
                return 'float'
        
        # int + int = int
        if type1 == 'int' and type2 == 'int':
            return 'int'
        
        return None
