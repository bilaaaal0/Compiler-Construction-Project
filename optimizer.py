"""
PHASE 5: CODE OPTIMIZER
Basic optimizations: constant folding, algebraic simplification
"""

import re

class Optimizer:
    def __init__(self):
        self.optimized_code = []
    
    def optimize(self, tac_code):
        """Apply basic optimizations to TAC"""
        self.optimized_code = []
        
        for instruction in tac_code:
            optimized = self.constant_folding(instruction)
            optimized = self.algebraic_simplification(optimized)
            self.optimized_code.append(optimized)
        
        # Remove dead code (unused temporaries)
        self.optimized_code = self.remove_dead_code(self.optimized_code)
        
        return self.optimized_code
    
    def constant_folding(self, instruction):
        """Fold constant expressions at compile time"""
        # Pattern: t0 = 3 + 5 -> t0 = 8
        pattern = r'(\w+) = (-?\d+\.?\d*) ([+\-*/%]) (-?\d+\.?\d*)'
        match = re.match(pattern, instruction)
        
        if match:
            result_var = match.group(1)
            left = match.group(2)
            op = match.group(3)
            right = match.group(4)
            
            try:
                # Determine if float or int
                if '.' in left or '.' in right:
                    left_val = float(left)
                    right_val = float(right)
                else:
                    left_val = int(left)
                    right_val = int(right)
                
                # Compute result
                if op == '+':
                    result = left_val + right_val
                elif op == '-':
                    result = left_val - right_val
                elif op == '*':
                    result = left_val * right_val
                elif op == '/':
                    if right_val != 0:
                        result = left_val / right_val
                    else:
                        return instruction  # Don't optimize division by zero
                elif op == '%':
                    if right_val != 0:
                        result = left_val % right_val
                    else:
                        return instruction
                else:
                    return instruction
                
                return f"{result_var} = {result}"
            except:
                return instruction
        
        return instruction
    
    def algebraic_simplification(self, instruction):
        """Simplify algebraic expressions"""
        # x * 1 -> x
        pattern1 = r'(\w+) = (\w+) \* 1(?:\.\d+)?$'
        match = re.match(pattern1, instruction)
        if match:
            return f"{match.group(1)} = {match.group(2)}"
        
        # x * 0 -> 0
        pattern2 = r'(\w+) = (\w+) \* 0(?:\.\d+)?$'
        match = re.match(pattern2, instruction)
        if match:
            return f"{match.group(1)} = 0"
        
        # x + 0 -> x
        pattern3 = r'(\w+) = (\w+) \+ 0(?:\.\d+)?$'
        match = re.match(pattern3, instruction)
        if match:
            return f"{match.group(1)} = {match.group(2)}"
        
        # x - 0 -> x
        pattern4 = r'(\w+) = (\w+) - 0(?:\.\d+)?$'
        match = re.match(pattern4, instruction)
        if match:
            return f"{match.group(1)} = {match.group(2)}"
        
        return instruction
    
    def remove_dead_code(self, code):
        """Remove unused temporary variables"""
        used_vars = set()
        
        # First pass: collect all used variables
        for instruction in code:
            # Variables in control flow, PUSH, RETURN, PRINT, READ
            if any(keyword in instruction for keyword in ['IF_FALSE', 'GOTO', 'PRINT', 'READ', 'PUSH', 'RETURN']):
                tokens = re.findall(r'\b[a-zA-Z_]\w*\b', instruction)
                # Filter out keywords
                keywords = {'IF_FALSE', 'GOTO', 'PRINT', 'READ', 'ALLOC', 'ENTER_SCOPE', 'EXIT_SCOPE', 'PARAM', 'PUSH', 'CALL', 'RETURN', 'RETVAL'}
                for token in tokens:
                    if token not in keywords:
                        used_vars.add(token)
            
            # Find variables on right side of assignments (but not the left side)
            # Be careful with == operator
            elif '=' in instruction and not instruction.endswith(':'):
                # Check if it's an assignment (single =) not a comparison (==)
                if '==' not in instruction and '!=' not in instruction and '<=' not in instruction and '>=' not in instruction:
                    parts = instruction.split('=', 1)  # Split only on first =
                    if len(parts) == 2:
                        right_side = parts[1]
                        # Extract variable names used on right side (not numbers)
                        tokens = re.findall(r'\b[a-zA-Z_]\w*\b', right_side)
                        used_vars.update(tokens)
        
        # Second pass: keep only instructions that define used variables or are control flow
        optimized = []
        for instruction in code:
            # Keep labels and control flow
            if instruction.endswith(':') or 'GOTO' in instruction or 'IF_FALSE' in instruction:
                optimized.append(instruction)
                continue
            
            # Keep PRINT, READ, ALLOC, function-related instructions
            if any(keyword in instruction for keyword in ['PRINT', 'READ', 'ALLOC', 'PARAM', 'PUSH', 'CALL', 'RETURN', 'END_FUNC', 'END_MAIN']):
                optimized.append(instruction)
                continue
            
            # Skip ENTER_SCOPE and EXIT_SCOPE - not needed in optimized code
            if 'ENTER_SCOPE' in instruction or 'EXIT_SCOPE' in instruction:
                continue
            
            # For assignments, check if left side is used
            if '=' in instruction:
                # Make sure it's an assignment, not just a label
                if '==' not in instruction and '!=' not in instruction and '<=' not in instruction and '>=' not in instruction:
                    parts = instruction.split('=', 1)
                    if len(parts) == 2:
                        left_var = parts[0].strip()
                        # Keep if it's not a temporary OR if it's used somewhere
                        if not left_var.startswith('t') or left_var in used_vars:
                            optimized.append(instruction)
                            continue
                else:
                    # It's a comparison operation (contains ==, !=, <=, >=)
                    # These should always be kept if they define a variable
                    parts = instruction.split('=', 1)
                    if len(parts) == 2:
                        left_var = parts[0].strip()
                        if left_var in used_vars or not left_var.startswith('t'):
                            optimized.append(instruction)
                            continue
        
        return optimized
