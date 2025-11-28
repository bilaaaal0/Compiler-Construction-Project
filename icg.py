"""
PHASE 4: INTERMEDIATE CODE GENERATOR (ICG)
Generates Three-Address Code (TAC) from AST
"""

from ast_nodes import *

class ICG:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, instruction):
        self.code.append(instruction)
    
    def generate(self, ast):
        self.visit(ast)
        return self.code
    
    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(f'No visit_{node.__class__.__name__} method in ICG')
    
    def visit_Program(self, node):
        # Generate code for functions first
        for func in node.functions:
            self.visit(func)
        
        # Generate code for main program
        self.emit("MAIN:")
        for stmt in node.statements:
            self.visit(stmt)
        self.emit("END_MAIN")
    
    def visit_DeclStmt(self, node):
        # Allocate space for variable
        self.emit(f"ALLOC {node.identifier} {node.var_type}")
        
        # Initialize if value provided
        if node.init_value:
            result = self.visit(node.init_value)
            self.emit(f"{node.identifier} = {result}")
    
    def visit_AssignStmt(self, node):
        result = self.visit(node.expression)
        self.emit(f"{node.identifier} = {result}")
    
    def visit_IfStmt(self, node):
        # Generate labels
        elif_labels = [self.new_label() for _ in node.elif_parts]
        else_label = self.new_label() if node.else_block else None
        end_label = self.new_label()
        
        # If condition
        cond_result = self.visit(node.condition)
        next_label = elif_labels[0] if elif_labels else (else_label if else_label else end_label)
        self.emit(f"IF_FALSE {cond_result} GOTO {next_label}")
        
        # If block
        self.visit(node.if_block)
        self.emit(f"GOTO {end_label}")
        
        # Elif parts
        for i, (elif_cond, elif_block) in enumerate(node.elif_parts):
            self.emit(f"{elif_labels[i]}:")
            cond_result = self.visit(elif_cond)
            next_label = elif_labels[i+1] if i+1 < len(elif_labels) else (else_label if else_label else end_label)
            self.emit(f"IF_FALSE {cond_result} GOTO {next_label}")
            self.visit(elif_block)
            self.emit(f"GOTO {end_label}")
        
        # Else block
        if else_label:
            self.emit(f"{else_label}:")
            self.visit(node.else_block)
        
        # End label
        self.emit(f"{end_label}:")
    
    def visit_LoopStmt(self, node):
        """Generate code for loop from ... to ... step ... statement"""
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Initialize loop variable (only if not using existing variable)
        if not node.use_existing_var and node.start_expr:
            start_result = self.visit(node.start_expr)
            self.emit(f"{node.var_name} = {start_result}")
        # If using existing variable, it's already initialized
        
        # Loop start
        self.emit(f"{start_label}:")
        
        # Condition: var <= end
        end_result = self.visit(node.end_expr)
        temp_cond = self.new_temp()
        self.emit(f"{temp_cond} = {node.var_name} <= {end_result}")
        self.emit(f"IF_FALSE {temp_cond} GOTO {end_label}")
        
        # Loop body
        self.visit(node.block)
        
        # Update: var = var + step
        if node.step_expr:
            step_result = self.visit(node.step_expr)
        else:
            step_result = "1"  # Default step
        
        temp_update = self.new_temp()
        self.emit(f"{temp_update} = {node.var_name} + {step_result}")
        self.emit(f"{node.var_name} = {temp_update}")
        
        self.emit(f"GOTO {start_label}")
        
        # End
        self.emit(f"{end_label}:")
    
    def visit_ConditionalLoopStmt(self, node):
        """Generate code for conditional loop (while-style)"""
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Loop start
        self.emit(f"{start_label}:")
        
        # Evaluate condition
        cond_result = self.visit(node.condition)
        self.emit(f"IF_FALSE {cond_result} GOTO {end_label}")
        
        # Loop body
        self.visit(node.block)
        
        # Jump back to start
        self.emit(f"GOTO {start_label}")
        
        # End
        self.emit(f"{end_label}:")
    
    def visit_PrintStmt(self, node):
        # Generate PRINT instruction for each expression
        for expr in node.expressions:
            result = self.visit(expr)
            self.emit(f"PRINT {result}")
    
    def visit_InputStmt(self, node):
        self.emit(f"READ {node.identifier}")
    
    def visit_Block(self, node):
        # Emit scope markers for proper variable scoping
        self.emit("ENTER_SCOPE")
        for stmt in node.statements:
            self.visit(stmt)
        self.emit("EXIT_SCOPE")
    
    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        temp = self.new_temp()
        self.emit(f"{temp} = {left} {node.operator} {right}")
        return temp
    
    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        
        temp = self.new_temp()
        self.emit(f"{temp} = {node.operator}{operand}")
        return temp
    
    def visit_Identifier(self, node):
        return node.name
    
    def visit_Literal(self, node):
        if node.lit_type == 'char':
            return f"'{node.value}'"
        return str(node.value)
    
    def visit_FunctionDecl(self, node):
        """Generate code for function declaration"""
        # Function label
        self.emit(f"FUNC_{node.name}:")
        
        # Parameters are already on stack (passed by caller)
        # Store parameters in local variables
        for i, (param_type, param_name) in enumerate(node.parameters):
            self.emit(f"PARAM {param_name} {i}")
        
        # Function body
        self.visit(node.body)
        
        # Default return if no explicit return
        self.emit(f"RETURN 0")
        self.emit(f"END_FUNC_{node.name}")
    
    def visit_FunctionCall(self, node):
        """Generate code for function call"""
        # Evaluate arguments and push onto stack
        arg_results = []
        for arg in node.arguments:
            result = self.visit(arg)
            arg_results.append(result)
        
        # Push arguments in reverse order (right to left)
        for arg_result in reversed(arg_results):
            self.emit(f"PUSH {arg_result}")
        
        # Call function
        self.emit(f"CALL FUNC_{node.name} {len(node.arguments)}")
        
        # Result is in return register
        temp = self.new_temp()
        self.emit(f"{temp} = RETVAL")
        return temp
    
    def visit_ReturnStmt(self, node):
        """Generate code for return statement"""
        if node.expression:
            result = self.visit(node.expression)
            self.emit(f"RETURN {result}")
        else:
            self.emit(f"RETURN 0")
