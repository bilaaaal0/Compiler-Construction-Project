"""
MAIN COMPILER
Orchestrates all six phases of compilation
"""

import os
import json
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from icg import ICG
from optimizer import Optimizer
from code_generator import CodeGenerator
from error_handler import ErrorHandler

class Compiler:
    def __init__(self):
        self.error_handler = ErrorHandler()
        self.output_folder = None
    
    def compile(self, source_code, verbose=True, output_folder=None):
        """
        Complete compilation pipeline
        Returns: (success, assembly_code)
        """
        
        self.output_folder = output_folder
        
        if verbose:
            print("\n" + "="*60)
            print("MINI COMPILER - COMPILATION STARTED")
            print("="*60)
        
        # Create output folder if specified
        if self.output_folder:
            os.makedirs(self.output_folder, exist_ok=True)
            if verbose:
                print(f"\nOutput folder: {self.output_folder}")
            
            # Save Phase 1 Input (source code)
            self._save_file("Phase1_Lexer_Input.txt", source_code)
        
        # PHASE 1: Lexical Analysis
        if verbose:
            print("\n[PHASE 1] Lexical Analysis...")
        lexer = Lexer(source_code)
        tokens, lex_errors = lexer.tokenize()
        
        for error in lex_errors:
            self.error_handler.add_lexical_error(error)
        
        if verbose:
            print(f"  Tokens generated: {len(tokens)}")
            if lex_errors:
                print(f"  ⚠ Lexical errors: {len(lex_errors)}")
        
        # Save Phase 1 Output (tokens)
        if self.output_folder:
            self._save_tokens("Phase1_Lexer_Output_Tokens.txt", tokens)
        
        if lex_errors:
            self.error_handler.print_errors()
            return False, None
        
        # PHASE 2: Syntax Analysis (Parsing)
        if verbose:
            print("\n[PHASE 2] Syntax Analysis (Parsing)...")
        
        # Save Phase 2 Input (tokens - same as Phase 1 output)
        if self.output_folder:
            self._save_file("Phase2_Parser_Input_Tokens.txt", 
                          "# Same as Phase1_Lexer_Output_Tokens.txt\n# See that file for token list")
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        for error in parser.errors:
            self.error_handler.add_syntax_error(error)
        
        if verbose:
            if parser.errors:
                print(f"  ⚠ Syntax errors: {len(parser.errors)}")
            else:
                print("  ✓ AST built successfully")
        
        # Save Phase 2 Output (AST)
        if self.output_folder:
            self._save_ast("Phase2_Parser_Output_AST.txt", ast)
        
        if parser.errors:
            self.error_handler.print_errors()
            return False, None
        
        # PHASE 3: Semantic Analysis
        if verbose:
            print("\n[PHASE 3] Semantic Analysis...")
        
        # Save Phase 3 Input (AST - same as Phase 2 output)
        if self.output_folder:
            self._save_file("Phase3_Semantic_Input_AST.txt",
                          "# Same as Phase2_Parser_Output_AST.txt\n# See that file for AST structure")
        
        semantic_analyzer = SemanticAnalyzer()
        symbol_table, sem_errors = semantic_analyzer.analyze(ast)
        
        for error in sem_errors:
            self.error_handler.add_semantic_error(error)
        
        if verbose:
            if sem_errors:
                print(f"  ⚠ Semantic errors: {len(sem_errors)}")
            else:
                print("  ✓ Type checking passed")
        
        # Save Phase 3 Output (Symbol Table)
        if self.output_folder:
            self._save_symbol_table("Phase3_Semantic_Output_SymbolTable.txt", symbol_table)
        
        if sem_errors:
            self.error_handler.print_errors()
            if verbose:
                symbol_table.print_table()
            return False, None
        
        # PHASE 4: Intermediate Code Generation
        if verbose:
            print("\n[PHASE 4] Intermediate Code Generation...")
        
        # Save Phase 4 Input (Annotated AST + Symbol Table)
        if self.output_folder:
            self._save_file("Phase4_ICG_Input_AnnotatedAST.txt",
                          "# Annotated AST with type information\n# See Phase2_Parser_Output_AST.txt for structure\n# See Phase3_Semantic_Output_SymbolTable.txt for types")
        
        icg = ICG()
        tac_code = icg.generate(ast)
        
        if verbose:
            print(f"  ✓ Generated {len(tac_code)} TAC instructions")
        
        # Save Phase 4 Output (TAC)
        if self.output_folder:
            self._save_file("Phase4_ICG_Output_TAC.txt", '\n'.join(tac_code))
        
        # PHASE 5: Optimization
        if verbose:
            print("\n[PHASE 5] Code Optimization...")
        
        # Save Phase 5 Input (TAC - same as Phase 4 output)
        if self.output_folder:
            self._save_file("Phase5_Optimizer_Input_TAC.txt",
                          "# Same as Phase4_ICG_Output_TAC.txt\n# See that file for TAC instructions")
        
        optimizer = Optimizer()
        optimized_tac = optimizer.optimize(tac_code)
        
        if verbose:
            print(f"  ✓ Optimized to {len(optimized_tac)} instructions")
            if len(tac_code) > len(optimized_tac):
                print(f"  Removed {len(tac_code) - len(optimized_tac)} dead instructions")
        
        # Save Phase 5 Output (Optimized TAC)
        if self.output_folder:
            self._save_file("Phase5_Optimizer_Output_OptimizedTAC.txt", '\n'.join(optimized_tac))
        
        # PHASE 6: Final Code Generation
        if verbose:
            print("\n[PHASE 6] Final Code Generation...")
        
        # Save Phase 6 Input (Optimized TAC - same as Phase 5 output)
        if self.output_folder:
            self._save_file("Phase6_CodeGen_Input_OptimizedTAC.txt",
                          "# Same as Phase5_Optimizer_Output_OptimizedTAC.txt\n# See that file for optimized TAC")
        
        code_gen = CodeGenerator()
        assembly = code_gen.generate(optimized_tac)
        
        if verbose:
            print(f"  ✓ Generated {len(assembly)} assembly instructions")
        
        # Save Phase 6 Output (Assembly)
        if self.output_folder:
            self._save_file("Phase6_CodeGen_Output_Assembly.asm", '\n'.join(assembly))
        
        # Success
        if verbose:
            print("\n" + "="*60)
            print("✓ COMPILATION SUCCESSFUL")
            print("="*60)
            self.error_handler.print_errors()
        
        # Save summary
        if self.output_folder:
            self._save_summary(verbose, tokens, tac_code, optimized_tac, assembly, symbol_table)
        
        return True, {
            'tokens': tokens,
            'ast': ast,
            'symbol_table': symbol_table,
            'tac': tac_code,
            'optimized_tac': optimized_tac,
            'assembly': assembly
        }
    
    def _save_file(self, filename, content):
        """Save content to file in output folder"""
        filepath = os.path.join(self.output_folder, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _save_tokens(self, filename, tokens):
        """Save tokens to file"""
        content = "=" * 70 + "\n"
        content += "PHASE 1 OUTPUT: TOKENS\n"
        content += "=" * 70 + "\n\n"
        content += f"Total Tokens: {len(tokens)}\n\n"
        
        for i, token in enumerate(tokens, 1):
            content += f"{i:3d}. {token}\n"
        
        self._save_file(filename, content)
    
    def _save_ast(self, filename, ast):
        """Save AST to file"""
        content = "=" * 70 + "\n"
        content += "PHASE 2 OUTPUT: ABSTRACT SYNTAX TREE (AST)\n"
        content += "=" * 70 + "\n\n"
        content += self._ast_to_string(ast, 0)
        self._save_file(filename, content)
    
    def _ast_to_string(self, node, indent=0):
        """Convert AST to readable string"""
        prefix = "  " * indent
        result = ""
        
        node_type = node.__class__.__name__
        result += f"{prefix}{node_type}\n"
        
        if hasattr(node, '__dict__'):
            for key, value in node.__dict__.items():
                if key.startswith('_'):
                    continue
                if isinstance(value, list):
                    if value:
                        result += f"{prefix}  {key}:\n"
                        for item in value:
                            if hasattr(item, '__class__') and hasattr(item.__class__, '__name__'):
                                result += self._ast_to_string(item, indent + 2)
                            else:
                                result += f"{prefix}    {item}\n"
                elif hasattr(value, '__class__') and hasattr(value.__class__, '__name__') and value.__class__.__module__ == 'ast_nodes':
                    result += f"{prefix}  {key}:\n"
                    result += self._ast_to_string(value, indent + 2)
                else:
                    result += f"{prefix}  {key}: {value}\n"
        
        return result
    
    def _save_symbol_table(self, filename, symbol_table):
        """Save symbol table to file"""
        content = "=" * 70 + "\n"
        content += "PHASE 3 OUTPUT: SYMBOL TABLE\n"
        content += "=" * 70 + "\n\n"
        
        for level, scope in enumerate(symbol_table.scopes):
            content += f"\nScope Level {level}:\n"
            content += f"{'Name':<15} {'Type':<15} {'Line':<8} {'Init':<8} {'Offset':<8}\n"
            content += "-" * 70 + "\n"
            for name, entry in scope.items():
                if entry.is_function:
                    params = ', '.join(entry.param_types)
                    type_str = f"({params})->{entry.return_type}"
                    content += f"{entry.name:<15} {type_str:<15} {entry.line:<8} {'N/A':<8} {'N/A':<8}\n"
                else:
                    content += f"{entry.name:<15} {entry.var_type:<15} {entry.line:<8} {entry.initialized!s:<8} {entry.offset:<8}\n"
        
        self._save_file(filename, content)
    
    def _save_summary(self, verbose, tokens, tac_code, optimized_tac, assembly, symbol_table):
        """Save compilation summary"""
        content = "=" * 70 + "\n"
        content += "COMPILATION SUMMARY\n"
        content += "=" * 70 + "\n\n"
        
        content += "PHASE 1: Lexical Analysis\n"
        content += f"  - Tokens Generated: {len(tokens)}\n\n"
        
        content += "PHASE 2: Syntax Analysis\n"
        content += f"  - AST Built: ✓\n\n"
        
        content += "PHASE 3: Semantic Analysis\n"
        content += f"  - Variables in Symbol Table: {sum(len(scope) for scope in symbol_table.scopes)}\n\n"
        
        content += "PHASE 4: Intermediate Code Generation\n"
        content += f"  - TAC Instructions: {len(tac_code)}\n\n"
        
        content += "PHASE 5: Optimization\n"
        content += f"  - Optimized Instructions: {len(optimized_tac)}\n"
        content += f"  - Instructions Removed: {len(tac_code) - len(optimized_tac)}\n\n"
        
        content += "PHASE 6: Code Generation\n"
        content += f"  - Assembly Instructions: {len(assembly)}\n\n"
        
        content += "=" * 70 + "\n"
        content += "STATUS: ✓ COMPILATION SUCCESSFUL\n"
        content += "=" * 70 + "\n"
        
        self._save_file("00_COMPILATION_SUMMARY.txt", content)
    
    def compile_file(self, filename, verbose=True, create_output_folder=True):
        """Compile from a source file"""
        try:
            with open(filename, 'r') as f:
                source_code = f.read()
            
            # Create output folder based on filename
            output_folder = None
            if create_output_folder:
                base_name = os.path.splitext(os.path.basename(filename))[0]
                output_folder = f"{base_name}_output"
            
            return self.compile(source_code, verbose, output_folder)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return False, None
        except Exception as e:
            print(f"Error reading file: {e}")
            return False, None


def main():
    """Main entry point for the compiler"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <source_file>")
        print("   or: python compiler.py --interactive")
        sys.exit(1)
    
    compiler = Compiler()
    
    if sys.argv[1] == '--interactive':
        print("Mini Compiler - Interactive Mode")
        print("Enter your code (type 'END' on a new line to compile):\n")
        
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        
        source_code = '\n'.join(lines)
        success, result = compiler.compile(source_code, verbose=True)
        
        if success:
            print("\n--- SYMBOL TABLE ---")
            result['symbol_table'].print_table()
            
            print("\n--- THREE-ADDRESS CODE ---")
            for instruction in result['tac']:
                print(instruction)
            
            print("\n--- OPTIMIZED TAC ---")
            for instruction in result['optimized_tac']:
                print(instruction)
            
            print("\n--- ASSEMBLY CODE ---")
            for instruction in result['assembly']:
                print(instruction)
    else:
        filename = sys.argv[1]
        success, result = compiler.compile_file(filename, verbose=True)
        
        if success:
            # All output files are already in the output folder
            # No need to create additional files here
            
            # Print symbol table
            print("\n--- SYMBOL TABLE ---")
            result['symbol_table'].print_table()


if __name__ == '__main__':
    main()
