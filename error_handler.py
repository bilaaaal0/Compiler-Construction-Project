"""
ERROR HANDLER
Centralized error reporting and management
"""

class ErrorHandler:
    def __init__(self):
        self.lexical_errors = []
        self.syntax_errors = []
        self.semantic_errors = []
    
    def add_lexical_error(self, error):
        self.lexical_errors.append(error)
    
    def add_syntax_error(self, error):
        self.syntax_errors.append(error)
    
    def add_semantic_error(self, error):
        self.semantic_errors.append(error)
    
    def has_errors(self):
        return len(self.lexical_errors) > 0 or len(self.syntax_errors) > 0 or len(self.semantic_errors) > 0
    
    def print_errors(self):
        if not self.has_errors():
            print("✓ No errors found!")
            return
        
        print("\n" + "="*60)
        print("COMPILATION ERRORS")
        print("="*60)
        
        if self.lexical_errors:
            print("\n--- LEXICAL ERRORS ---")
            for error in self.lexical_errors:
                print(f"  • {error}")
        
        if self.syntax_errors:
            print("\n--- SYNTAX ERRORS ---")
            for error in self.syntax_errors:
                print(f"  • {error}")
        
        if self.semantic_errors:
            print("\n--- SEMANTIC ERRORS ---")
            for error in self.semantic_errors:
                print(f"  • {error}")
        
        print("\n" + "="*60)
        total = len(self.lexical_errors) + len(self.syntax_errors) + len(self.semantic_errors)
        print(f"Total Errors: {total}")
        print("="*60 + "\n")
    
    def get_error_summary(self):
        return {
            'lexical': len(self.lexical_errors),
            'syntax': len(self.syntax_errors),
            'semantic': len(self.semantic_errors),
            'total': len(self.lexical_errors) + len(self.syntax_errors) + len(self.semantic_errors)
        }
