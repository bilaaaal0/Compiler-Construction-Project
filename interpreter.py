"""
TAC INTERPRETER
Executes Three-Address Code and shows output
"""

class TACInterpreter:
    def __init__(self):
        self.variables = {}
        self.var_types = {}  # Track variable types for conversions
        self.labels = {}
        self.functions = {}
        self.arg_stack = []  # For function arguments
        self.call_stack = []  # For function call frames
        self.scope_stack = []  # For block scope management
        self.pc = 0  # Program counter
        self.instructions = []
        self.output = []
        self.max_iterations = 100000  # Prevent infinite loops (increased for recursion)
        self.iteration_count = 0
    
    def execute(self, tac_code):
        """Execute TAC instructions"""
        self.instructions = tac_code
        
        # First pass: find labels and functions
        for i, instruction in enumerate(self.instructions):
            if instruction.endswith(':'):
                label = instruction[:-1]
                self.labels[label] = i
                if label.startswith('FUNC_'):
                    func_name = label[5:]  # Remove 'FUNC_' prefix
                    self.functions[func_name] = i
        
        # Second pass: execute from MAIN
        if 'MAIN' in self.labels:
            self.pc = self.labels['MAIN'] + 1
            self.run()
        else:
            print("Error: No MAIN label found")
        
        return self.output
    
    def run(self):
        """Run instructions from current PC"""
        while self.pc < len(self.instructions):
            self.iteration_count += 1
            
            # Safety check for infinite loops
            if self.iteration_count > self.max_iterations:
                print(f"\nWarning: Stopped after {self.max_iterations} iterations (possible infinite loop)")
                break
            
            instruction = self.instructions[self.pc].strip()
            
            # Skip empty lines and labels
            if not instruction or instruction.endswith(':'):
                self.pc += 1
                continue
            
            # End of main
            if instruction == 'END_MAIN':
                break
            
            # Execute instruction
            try:
                self.execute_instruction(instruction)
            except Exception as e:
                print(f"Error executing: {instruction}")
                print(f"Error: {e}")
                raise
            self.pc += 1
    
    def execute_instruction(self, instruction):
        """Execute a single TAC instruction"""
        
        # ENTER_SCOPE - save current variable state
        if instruction.startswith('ENTER_SCOPE'):
            # Save both the variable names AND their values
            # Also track which variables are allocated in this scope
            self.scope_stack.append({
                'var_names': set(self.variables.keys()),
                'var_values': dict(self.variables),
                'allocated_in_scope': set()  # Track variables ALLOCated in this scope
            })
        
        # EXIT_SCOPE - restore variables from before scope
        elif instruction.startswith('EXIT_SCOPE'):
            if self.scope_stack:
                scope_info = self.scope_stack.pop()
                old_var_names = scope_info['var_names']
                old_var_values = scope_info['var_values']
                allocated_in_scope = scope_info['allocated_in_scope']
                
                # Remove or restore variables based on whether they were allocated in this scope
                current_var_names = list(self.variables.keys())
                for var_name in current_var_names:
                    if var_name not in old_var_names:
                        # Variable was declared ONLY in this scope, remove it
                        del self.variables[var_name]
                    elif var_name in allocated_in_scope:
                        # Variable was re-declared (shadowed) in this scope, restore old value
                        self.variables[var_name] = old_var_values[var_name]
                    # else: variable existed before and was just modified, keep new value
        
        # ALLOC variable type
        elif instruction.startswith('ALLOC'):
            parts = instruction.split()
            var_name = parts[1]
            var_type = parts[2] if len(parts) > 2 else 'int'
            
            # Track variable type
            self.var_types[var_name] = var_type
            
            # Track if this is an allocation in a scope
            if self.scope_stack:
                self.scope_stack[-1]['allocated_in_scope'].add(var_name)
            
            self.variables[var_name] = 0  # Initialize to 0
        
        # PRINT variable
        elif instruction.startswith('PRINT'):
            parts = instruction.split()
            var_name = parts[1]
            value = self.get_value(var_name)
            print(f"  Output: {value}")
            self.output.append(value)
        
        # READ variable
        elif instruction.startswith('READ'):
            parts = instruction.split()
            var_name = parts[1]
            value = input(f"Input {var_name}: ")
            try:
                self.variables[var_name] = int(value)
            except:
                try:
                    self.variables[var_name] = float(value)
                except:
                    self.variables[var_name] = value
        
        # GOTO label
        elif instruction.startswith('GOTO'):
            parts = instruction.split()
            label = parts[1]
            if label in self.labels:
                self.pc = self.labels[label] - 1  # -1 because pc will be incremented
        
        # IF_FALSE condition GOTO label
        elif instruction.startswith('IF_FALSE'):
            parts = instruction.split()
            condition = parts[1]
            label = parts[3]
            cond_value = self.get_value(condition)
            if not cond_value or cond_value == 0:
                if label in self.labels:
                    self.pc = self.labels[label] - 1
        
        # PARAM (function parameter) - pop from arg stack
        elif instruction.startswith('PARAM'):
            parts = instruction.split()
            param_name = parts[1]
            if self.arg_stack:
                # Pop arguments (they were pushed in reverse order)
                value = self.arg_stack.pop(0)
                self.variables[param_name] = value
        
        # PUSH value
        elif instruction.startswith('PUSH'):
            parts = instruction.split()
            value = self.get_value(parts[1])
            self.arg_stack.append(value)
        
        # CALL function arg_count
        elif instruction.startswith('CALL'):
            parts = instruction.split()
            func_label = parts[1]
            arg_count = int(parts[2])
            
            # Save current state (return address and local variables)
            return_addr = self.pc + 1
            saved_vars = dict(self.variables)  # Save current variables
            
            # Push call frame
            self.call_stack.append({
                'return_addr': return_addr,
                'saved_vars': saved_vars
            })
            
            # Jump to function
            if func_label in self.labels:
                self.pc = self.labels[func_label]
        
        # RETURN value
        elif instruction.startswith('RETURN'):
            parts = instruction.split()
            return_value = 0
            
            if len(parts) > 1:
                return_value = self.get_value(parts[1])
            
            # Restore caller's state
            if self.call_stack:
                frame = self.call_stack.pop()
                return_addr = frame['return_addr']
                self.variables = frame['saved_vars']
                
                # Store return value
                self.variables['RETVAL'] = return_value
                
                # Return to caller
                self.pc = return_addr - 1  # -1 because pc will be incremented
                return
        
        # END_FUNC marker
        elif instruction.startswith('END_FUNC'):
            # Skip to next instruction
            pass
        
        # Assignment: var = value or var = expr
        elif '=' in instruction:
            # Check if it's an assignment (has = but not ==, !=, <=, >=)
            # Split on first = and check if left side is a single identifier
            parts = instruction.split('=', 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                expr = parts[1].strip()
                
                # Make sure left side is a valid variable name (not a comparison)
                if var_name and not any(c in var_name for c in ['<', '>', '!', ' ']):
                    # Special case for RETVAL
                    if expr == 'RETVAL':
                        if 'RETVAL' in self.variables:
                            self.variables[var_name] = self.variables['RETVAL']
                        else:
                            self.variables[var_name] = 0
                    else:
                        # Evaluate expression
                        value = self.evaluate_expression(expr)
                        
                        # Type conversion: char to int
                        if var_name in self.var_types:
                            target_type = self.var_types[var_name]
                            
                            # Convert single character to ASCII value for int variables
                            if target_type == 'int' and isinstance(value, str) and len(value) == 1:
                                value = ord(value)
                            
                            # Convert int to float for float variables
                            elif target_type == 'float' and isinstance(value, int):
                                value = float(value)
                        
                        self.variables[var_name] = value
    
    def evaluate_expression(self, expr):
        """Evaluate an expression"""
        expr = expr.strip()
        
        # Binary operations - check in order of precedence
        # Logical operators (lowest precedence)
        if '||' in expr:
            parts = expr.split('||', 1)
            if len(parts) == 2:
                left = self.get_value(parts[0].strip())
                right = self.get_value(parts[1].strip())
                return 1 if (left or right) else 0
        
        if '&&' in expr:
            parts = expr.split('&&', 1)
            if len(parts) == 2:
                left = self.get_value(parts[0].strip())
                right = self.get_value(parts[1].strip())
                return 1 if (left and right) else 0
        
        # Comparison operators (check these first as they contain other operators)
        for op in ['<=', '>=', '==', '!=']:
            if op in expr:
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    left = self.get_value(parts[0].strip())
                    right = self.get_value(parts[1].strip())
                    
                    if op == '<=':
                        return 1 if left <= right else 0
                    elif op == '>=':
                        return 1 if left >= right else 0
                    elif op == '==':
                        return 1 if left == right else 0
                    elif op == '!=':
                        return 1 if left != right else 0
        
        # Single character comparison operators
        for op in ['<', '>']:
            if op in expr:
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    left = self.get_value(parts[0].strip())
                    right = self.get_value(parts[1].strip())
                    
                    if op == '<':
                        return 1 if left < right else 0
                    elif op == '>':
                        return 1 if left > right else 0
        
        # Arithmetic operators
        for op in ['+', '-', '*', '/', '%']:
            if op in expr:
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    left = self.get_value(parts[0].strip())
                    right = self.get_value(parts[1].strip())
                    
                    if op == '+':
                        return left + right
                    elif op == '-':
                        return left - right
                    elif op == '*':
                        return left * right
                    elif op == '/':
                        return left / right if right != 0 else 0
                    elif op == '%':
                        return left % right if right != 0 else 0
        
        # Unary operations
        if expr.startswith('-'):
            return -self.get_value(expr[1:].strip())
        if expr.startswith('!'):
            return 0 if self.get_value(expr[1:].strip()) else 1
        
        # Single value
        return self.get_value(expr)
    
    def get_value(self, token):
        """Get value of a token (variable or literal)"""
        token = token.strip()
        
        # Try as number
        try:
            if '.' in token:
                return float(token)
            return int(token)
        except:
            pass
        
        # Try as variable
        if token in self.variables:
            return self.variables[token]
        
        # Try as char literal
        if token.startswith("'") and token.endswith("'"):
            return token[1:-1]
        
        # Unknown - return 0
        return 0


def main():
    """Test the interpreter"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <tac_file>")
        sys.exit(1)
    
    tac_file = sys.argv[1]
    
    try:
        with open(tac_file, 'r') as f:
            tac_code = [line.strip() for line in f.readlines()]
        
        print("\n" + "="*60)
        print("TAC INTERPRETER - EXECUTION STARTED")
        print("="*60 + "\n")
        
        interpreter = TACInterpreter()
        output = interpreter.execute(tac_code)
        
        print("\n" + "="*60)
        print("EXECUTION COMPLETED")
        print("="*60)
        print(f"\nTotal outputs: {len(output)}")
        
    except FileNotFoundError:
        print(f"Error: File '{tac_file}' not found")
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
