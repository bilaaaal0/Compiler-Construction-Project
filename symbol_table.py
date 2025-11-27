"""
SYMBOL TABLE MANAGER
Manages variable declarations and scopes
"""

class SymbolEntry:
    def __init__(self, name, var_type, scope_level, line, initialized=False, offset=0, is_function=False, param_types=None, return_type=None):
        self.name = name
        self.var_type = var_type
        self.scope_level = scope_level
        self.line = line
        self.initialized = initialized
        self.offset = offset
        self.is_function = is_function
        self.param_types = param_types or []  # List of parameter types
        self.return_type = return_type  # For functions
    
    def __repr__(self):
        if self.is_function:
            params = ', '.join(self.param_types)
            return f"Function({self.name}, ({params}) -> {self.return_type}, line={self.line})"
        return f"Symbol({self.name}, {self.var_type}, scope={self.scope_level}, line={self.line})"

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes (list of dictionaries)
        self.current_scope = 0
        self.offset_counter = 0
        self.current_function = None  # Track current function for return type checking
    
    def enter_scope(self):
        """Push a new scope onto the stack"""
        self.scopes.append({})
        self.current_scope += 1
    
    def exit_scope(self):
        """Pop the current scope from the stack"""
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1
    
    def insert(self, name, var_type, line, initialized=False, is_function=False, param_types=None, return_type=None):
        """Insert a symbol into the current scope"""
        if name in self.scopes[self.current_scope]:
            return False, f"{'Function' if is_function else 'Variable'} '{name}' already declared in this scope"
        
        offset = self.offset_counter
        if not is_function:
            self.offset_counter += self.get_type_size(var_type)
        
        entry = SymbolEntry(name, var_type, self.current_scope, line, initialized, offset, is_function, param_types, return_type)
        self.scopes[self.current_scope][name] = entry
        return True, entry
    
    def lookup(self, name):
        """Look up a symbol in all scopes (from current to global)"""
        for i in range(self.current_scope, -1, -1):
            if name in self.scopes[i]:
                return self.scopes[i][name]
        return None
    
    def lookup_current_scope(self, name):
        """Look up a symbol only in the current scope"""
        if name in self.scopes[self.current_scope]:
            return self.scopes[self.current_scope][name]
        return None
    
    def update_initialized(self, name):
        """Mark a variable as initialized"""
        entry = self.lookup(name)
        if entry:
            entry.initialized = True
    
    def get_type_size(self, var_type):
        """Return memory size for a type"""
        sizes = {'int': 4, 'float': 4, 'char': 1}
        return sizes.get(var_type, 4)
    
    def print_table(self):
        """Print the symbol table for debugging"""
        print("\n=== SYMBOL TABLE ===")
        for level, scope in enumerate(self.scopes):
            print(f"\nScope Level {level}:")
            print(f"{'Name':<15} {'Type':<15} {'Line':<8} {'Init':<8} {'Offset':<8}")
            print("-" * 70)
            for name, entry in scope.items():
                if entry.is_function:
                    params = ', '.join(entry.param_types)
                    type_str = f"({params})->{entry.return_type}"
                    print(f"{entry.name:<15} {type_str:<15} {entry.line:<8} {'N/A':<8} {'N/A':<8}")
                else:
                    print(f"{entry.name:<15} {entry.var_type:<15} {entry.line:<8} {entry.initialized!s:<8} {entry.offset:<8}")
