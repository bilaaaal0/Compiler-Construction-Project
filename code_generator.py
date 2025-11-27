"""
PHASE 6: FINAL CODE GENERATOR
Converts optimized TAC to pseudo-assembly code
"""

class CodeGenerator:
    def __init__(self):
        self.assembly = []
        self.data_section = []
        self.text_section = []
    
    def generate(self, tac_code):
        """Convert TAC to pseudo-assembly"""
        self.assembly = []
        self.data_section = []
        self.text_section = []
        
        # Process each TAC instruction
        for instruction in tac_code:
            self.translate_instruction(instruction)
        
        # Build final assembly
        self.assembly.append("; ========== DATA SECTION ==========")
        self.assembly.extend(self.data_section)
        self.assembly.append("")
        self.assembly.append("; ========== TEXT SECTION ==========")
        self.assembly.extend(self.text_section)
        
        return self.assembly
    
    def translate_instruction(self, instruction):
        """Translate a single TAC instruction to assembly"""
        
        # Labels (including function labels)
        if instruction.endswith(':'):
            self.text_section.append(instruction)
            return
        
        # Function end markers
        if instruction.startswith('END_FUNC') or instruction == 'END_MAIN':
            self.text_section.append(f"; {instruction}")
            return
        
        # ALLOC - Variable allocation
        if instruction.startswith('ALLOC'):
            parts = instruction.split()
            var_name = parts[1]
            var_type = parts[2]
            size = {'int': 4, 'float': 4, 'char': 1}.get(var_type, 4)
            self.data_section.append(f"{var_name}: .space {size}  ; {var_type}")
            return
        
        # PRINT
        if instruction.startswith('PRINT'):
            var = instruction.split()[1]
            self.text_section.append(f"    LOAD {var}")
            self.text_section.append(f"    PRINT")
            return
        
        # READ
        if instruction.startswith('READ'):
            var = instruction.split()[1]
            self.text_section.append(f"    READ")
            self.text_section.append(f"    STORE {var}")
            return
        
        # PARAM - Function parameter
        if instruction.startswith('PARAM'):
            parts = instruction.split()
            param_name = parts[1]
            param_index = parts[2]
            self.text_section.append(f"    POP {param_name}  ; param {param_index}")
            return
        
        # PUSH - Push argument
        if instruction.startswith('PUSH'):
            var = instruction.split()[1]
            if var.replace('.', '').replace('-', '').isdigit():
                self.text_section.append(f"    LOAD_IMM {var}")
            else:
                self.text_section.append(f"    LOAD {var}")
            self.text_section.append(f"    PUSH")
            return
        
        # CALL - Function call
        if instruction.startswith('CALL'):
            parts = instruction.split()
            func_label = parts[1]
            arg_count = parts[2]
            self.text_section.append(f"    CALL {func_label}  ; {arg_count} args")
            return
        
        # RETURN - Return from function
        if instruction.startswith('RETURN'):
            parts = instruction.split()
            if len(parts) > 1:
                ret_val = parts[1]
                if ret_val.replace('.', '').replace('-', '').isdigit():
                    self.text_section.append(f"    LOAD_IMM {ret_val}")
                else:
                    self.text_section.append(f"    LOAD {ret_val}")
            self.text_section.append(f"    RET")
            return
        
        # RETVAL - Get return value
        if '= RETVAL' in instruction:
            dest = instruction.split('=')[0].strip()
            self.text_section.append(f"    STORE {dest}  ; store return value")
            return
        
        # GOTO
        if instruction.startswith('GOTO'):
            label = instruction.split()[1]
            self.text_section.append(f"    JMP {label}")
            return
        
        # IF_FALSE
        if instruction.startswith('IF_FALSE'):
            parts = instruction.split()
            condition = parts[1]
            label = parts[3]
            self.text_section.append(f"    LOAD {condition}")
            self.text_section.append(f"    JZ {label}  ; Jump if zero (false)")
            return
        
        # Assignment: x = y
        if '=' in instruction and not any(op in instruction for op in ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!']):
            parts = instruction.split('=')
            dest = parts[0].strip()
            source = parts[1].strip()
            
            # Check if source is a literal
            if source.replace('.', '').replace('-', '').isdigit():
                self.text_section.append(f"    LOAD_IMM {source}")
            else:
                self.text_section.append(f"    LOAD {source}")
            self.text_section.append(f"    STORE {dest}")
            return
        
        # Binary operations: t0 = x + y
        if '=' in instruction:
            parts = instruction.split('=')
            dest = parts[0].strip()
            expr = parts[1].strip()
            
            # Arithmetic operations
            for op, asm_op in [('+', 'ADD'), ('-', 'SUB'), ('*', 'MUL'), ('/', 'DIV'), ('%', 'MOD')]:
                if op in expr:
                    operands = expr.split(op)
                    if len(operands) == 2:
                        left = operands[0].strip()
                        right = operands[1].strip()
                        
                        # Load left operand
                        if left.replace('.', '').replace('-', '').isdigit():
                            self.text_section.append(f"    LOAD_IMM {left}")
                        else:
                            self.text_section.append(f"    LOAD {left}")
                        
                        # Load right operand
                        if right.replace('.', '').replace('-', '').isdigit():
                            self.text_section.append(f"    {asm_op}_IMM {right}")
                        else:
                            self.text_section.append(f"    {asm_op} {right}")
                        
                        self.text_section.append(f"    STORE {dest}")
                        return
            
            # Relational operations
            for op, asm_op in [('==', 'CMP_EQ'), ('!=', 'CMP_NE'), ('<=', 'CMP_LE'), 
                               ('>=', 'CMP_GE'), ('<', 'CMP_LT'), ('>', 'CMP_GT')]:
                if op in expr:
                    operands = expr.split(op)
                    if len(operands) == 2:
                        left = operands[0].strip()
                        right = operands[1].strip()
                        
                        self.text_section.append(f"    LOAD {left}")
                        self.text_section.append(f"    {asm_op} {right}")
                        self.text_section.append(f"    STORE {dest}")
                        return
            
            # Logical operations
            if '&&' in expr:
                operands = expr.split('&&')
                left = operands[0].strip()
                right = operands[1].strip()
                self.text_section.append(f"    LOAD {left}")
                self.text_section.append(f"    AND {right}")
                self.text_section.append(f"    STORE {dest}")
                return
            
            if '||' in expr:
                operands = expr.split('||')
                left = operands[0].strip()
                right = operands[1].strip()
                self.text_section.append(f"    LOAD {left}")
                self.text_section.append(f"    OR {right}")
                self.text_section.append(f"    STORE {dest}")
                return
            
            # Unary operations
            if expr.startswith('-'):
                operand = expr[1:].strip()
                self.text_section.append(f"    LOAD {operand}")
                self.text_section.append(f"    NEG")
                self.text_section.append(f"    STORE {dest}")
                return
            
            if expr.startswith('!'):
                operand = expr[1:].strip()
                self.text_section.append(f"    LOAD {operand}")
                self.text_section.append(f"    NOT")
                self.text_section.append(f"    STORE {dest}")
                return
