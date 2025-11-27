# Mini Compiler - Complete Implementation

A full-featured compiler implementation with all six classical phases, built from scratch without parser generators.

## 📋 Features

### Supported Language Constructs
- **Data Types**: `int`, `float`, `char`
- **Control Flow**: `if`, `elif`, `else`
- **Loops**: `while`, `for`
- **Functions**: Function declarations, recursion, parameter passing, return values
- **I/O**: `print`, `input`
- **Operators**: Arithmetic (`+`, `-`, `*`, `/`, `%`), Relational (`==`, `!=`, `<`, `>`, `<=`, `>=`), Logical (`&&`, `||`, `!`)
- **Nested Structures**: Full support for nested blocks and scopes

### Compiler Phases

#### Phase 1: Lexical Analysis
- Character-by-character tokenization
- Keyword recognition
- Number parsing (int and float)
- Char literal handling
- Comment support (`//`)
- Comprehensive error detection

#### Phase 2: Syntax Analysis (Parsing)
- **Recursive Descent Parser** (Top-Down)
- Builds Abstract Syntax Tree (AST)
- Error recovery mechanism
- Grammar-driven implementation

#### Phase 3: Semantic Analysis
- Type checking with coercion rules
- Scope management (stack-based)
- Declaration-before-use validation
- Symbol table construction
- Initialization tracking

#### Phase 4: Intermediate Code Generation
- Three-Address Code (TAC) generation
- Label management for control flow
- Temporary variable allocation

#### Phase 5: Optimization
- Constant folding (`3 + 5` → `8`)
- Algebraic simplification (`x * 1` → `x`, `x + 0` → `x`)
- Dead code elimination

#### Phase 6: Code Generation
- Pseudo-assembly output
- Stack-based architecture
- Data and text sections

## 🚀 Usage

### Command Line

```bash
# Compile a source file
python compiler.py test_program1.txt

# Interactive mode
python compiler.py --interactive
```

### Programmatic Usage

```python
from compiler import Compiler

compiler = Compiler()
success, result = compiler.compile(source_code, verbose=True)

if success:
    print("Compilation successful!")
    result['symbol_table'].print_table()
```

## 📁 Project Structure

```
mini-compiler/
├── grammar.txt              # Formal grammar specification
├── lexer.py                 # Phase 1: Lexical Analyzer
├── ast_nodes.py             # AST node definitions
├── parser.py                # Phase 2: Syntax Analyzer
├── symbol_table.py          # Symbol table manager
├── semantic_analyzer.py     # Phase 3: Semantic Analyzer
├── icg.py                   # Phase 4: Intermediate Code Generator
├── optimizer.py             # Phase 5: Code Optimizer
├── code_generator.py        # Phase 6: Final Code Generator
├── error_handler.py         # Centralized error handling
├── compiler.py              # Main compiler orchestrator
├── test_program1.txt        # Test: Basic arithmetic
├── test_program2.txt        # Test: If-elif-else
├── test_program3.txt        # Test: Loops
├── test_program4.txt        # Test: Nested structures
├── test_errors.txt          # Test: Error detection
└── README.md                # This file
```

## 📖 Grammar

See `grammar.txt` for the complete formal grammar specification in BNF notation.

### Type Coercion Rules

1. `int + int` → `int`
2. `float + float` → `float`
3. `int + float` → `float` (int promoted to float)
4. `char` in arithmetic → promoted to `int`
5. Assignment: `int = float` → **ERROR** (narrowing not allowed)
6. Assignment: `float = int` → **OK** (widening allowed)

## 🧪 Test Programs

### Test 1: Basic Arithmetic
```
int x;
x = 10 + 5 * 2;
print x;
```

### Test 2: Control Flow
```
int score;
score = 85;

if (score >= 90) {
    print 1;
} elif (score >= 80) {
    print 2;
} else {
    print 0;
}
```

### Test 3: Loops (Modern Syntax)
```rust
int sum;
sum = 0;

loop from i = 1 to 10 {
    sum = sum + i;
}
print sum;
```

### Test 4: Functions (NEW!)
```
func int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    int temp;
    temp = n - 1;
    return n * factorial(temp);
}

int result;
result = factorial(5);
print result;  // Output: 120
```

## 🔍 Error Handling

The compiler detects three types of errors:

### 1. Lexical Errors
- Unknown characters
- Malformed literals
- Invalid tokens

### 2. Syntax Errors
- Missing semicolons
- Unmatched braces
- Invalid token sequences

### 3. Semantic Errors
- Undeclared variables
- Type mismatches
- Use before initialization
- Redeclaration in same scope

## 📊 Output Files

When compiling a file `program.txt`, the compiler generates:

- `program.tac` - Three-Address Code
- `program_opt.tac` - Optimized TAC
- `program.asm` - Final assembly code

## 🎓 Educational Value

This compiler is designed for:
- Compiler design courses
- Understanding compilation phases
- Learning parser implementation
- Studying optimization techniques
- Semester projects and viva preparation

## 🛠️ Implementation Details

### Parser Choice: Recursive Descent (Top-Down)

**Why not Bottom-Up (LR/LALR)?**
- Easier to implement manually
- No need for complex table generation
- Better error messages
- More intuitive for small languages
- Suitable for academic projects

### Symbol Table: Stack-Based Scopes

Each scope is a dictionary on a stack:
```python
scopes = [
    {'x': SymbolEntry(...)},  # Global scope
    {'y': SymbolEntry(...)},  # Block scope
]
```

### Three-Address Code Format

```
t0 = a + b
t1 = t0 * c
x = t1
IF_FALSE t2 GOTO L1
L1:
```

## 📝 Example Compilation

**Input:**
```
int x;
x = 5 + 3;
print x;
```

**Tokens:**
```
INT, IDENTIFIER(x), SEMICOLON, IDENTIFIER(x), ASSIGN, 
INTEGER_LITERAL(5), PLUS, INTEGER_LITERAL(3), SEMICOLON, ...
```

**TAC:**
```
ALLOC x int
t0 = 5 + 3
x = t0
PRINT x
```

**Optimized TAC:**
```
ALLOC x int
x = 8
PRINT x
```

**Assembly:**
```
x: .space 4  ; int
    LOAD_IMM 8
    STORE x
    LOAD x
    PRINT
```

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more optimizations
- Extend the language features
- Improve error messages
- Add more test cases

## 📄 License

Free to use for educational purposes.

## 👨‍💻 Author

Built as a complete semester project demonstrating all phases of compilation.

---

**Happy Compiling! 🎉**
