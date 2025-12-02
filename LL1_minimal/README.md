# LL(1) Minimal Grammar - For Hand-Written Parsing Tables

This folder contains a **simplified grammar** designed for hand-written LL(1) parsing table construction. It demonstrates the same conflicts as the full grammar but is small enough to work with on paper.

## Why This Grammar?

The full grammar has:
- **42 non-terminals** × **42 terminals** = **1,764 cells** 😱

This minimal grammar has:
- **7 non-terminals** × **8 terminals** = **56 cells** ✓ (manageable!)

## Grammar

```
Program → Stmt

Stmt → Expr ';'
     | Cond ';'

Expr → Factor Expr'

Expr' → '+' Factor Expr'
      | ε

Factor → id
       | call
       | '(' Expr ')'

call → id '(' ')'

Cond → Expr '==' Expr
     | '(' Cond ')'
```

## Grammar Components

**Non-Terminals (7):**
- Program (start symbol)
- Stmt
- Expr
- Expr'
- Factor
- call
- Cond

**Terminals (8):**
- id
- '('
- ')'
- '+'
- '=='
- ';'
- $

## Analysis Results

**Is LL(1)?** ❌ NO

**Conflicts Found:** 4

### Conflict Details

1. **Stmt** on `(` → Cannot distinguish `Expr ';'` from `Cond ';'`
2. **Stmt** on `id` → Cannot distinguish `Expr ';'` from `Cond ';'`
3. **Cond** on `(` → Cannot distinguish `Expr '==' Expr` from `'(' Cond ')'`
4. **Factor** on `id` → Cannot distinguish `id` from `call`

## Computed Sets

### NULLABLE
```
Expr'
```

### FIRST Sets
```
FIRST(Program) = {(, id}
FIRST(Stmt)    = {(, id}
FIRST(Expr)    = {(, id}
FIRST(Expr')   = {+, ε}
FIRST(Factor)  = {(, id}
FIRST(call)    = {id}
FIRST(Cond)    = {(, id}
```

### FOLLOW Sets
```
FOLLOW(Program) = {$}
FOLLOW(Stmt)    = {$}
FOLLOW(Expr)    = {', ), ;, ==}
FOLLOW(Expr')   = {', ), ;, ==}
FOLLOW(Factor)  = {+, ', ), ;, ==}
FOLLOW(call)    = {+, ', ), ;, ==}
FOLLOW(Cond)    = {), ;}
```

## Parsing Table (Simplified View)

```
           | id  | (   | )   | +   | ==  | ;   | $
-----------|-----|-----|-----|-----|-----|-----|-----
Program    | P→S | P→S |     |     |     |     |
Stmt       | CONFLICT | CONFLICT |     |     |     |     |
Expr       | E→FE'| E→FE'|    |     |     |     |
Expr'      |     |     | E'→ε| E'→+FE'| E'→ε| E'→ε|
Factor     | CONFLICT | F→(E)|    |     |     |     |
call       | c→id()|  |     |     |     |     |
Cond       | C→E==E| CONFLICT|    |     |     |     |
```

## How to Use for Hand-Written Tables

### Step 1: Draw the Table
```
Draw a table with:
- 7 rows (one for each non-terminal)
- 8 columns (one for each terminal including $)
```

### Step 2: Fill Using FIRST and FOLLOW

For each production `A → α`:

1. **For each terminal `a` in FIRST(α):**
   - Add `A → α` to table[A, a]

2. **If ε is in FIRST(α):**
   - For each terminal `b` in FOLLOW(A):
     - Add `A → α` to table[A, b]

### Step 3: Mark Conflicts

If a cell has multiple entries, it's a conflict!

## Excel File Contents

The `grammar_analysis.xlsx` file contains:

1. **Result** - Summary with conflict details
2. **Grammar** - All productions
3. **NULLABLE** - Nullable non-terminals
4. **FIRST Sets** - FIRST for each non-terminal
5. **FOLLOW Sets** - FOLLOW for each non-terminal
6. **Parsing Table** - Complete table with conflicts in RED
7. **Hand-Written Guide** - Step-by-step instructions

## Example: Building Table Entry

**For production: Expr → Factor Expr'**

1. FIRST(Factor Expr') = FIRST(Factor) = {(, id}
2. Add "Expr → Factor Expr'" to:
   - table[Expr, '(']
   - table[Expr, id]

**For production: Expr' → ε**

1. ε is in FIRST(Expr' → ε)
2. FOLLOW(Expr') = {', ), ;, ==}
3. Add "Expr' → ε" to:
   - table[Expr', ''']
   - table[Expr', ')']
   - table[Expr', ';']
   - table[Expr', '==']

## Practice Exercise

Try building the parsing table by hand following these steps:

1. Copy the grammar
2. Compute NULLABLE (check answer in Excel)
3. Compute FIRST sets (check answer in Excel)
4. Compute FOLLOW sets (check answer in Excel)
5. Build parsing table (check answer in Excel)
6. Identify conflicts (should find 4)

## Comparison with Full Grammar

| Aspect | Full Grammar | Minimal Grammar |
|--------|--------------|-----------------|
| Non-Terminals | 42 | 7 |
| Terminals | 42 | 8 |
| Table Size | 1,764 cells | 56 cells |
| Conflicts | 2 | 4 |
| Hand-Writable? | ❌ No | ✅ Yes |

## Key Conflicts Demonstrated

This minimal grammar demonstrates:

1. **Factor Conflict** (like full grammar)
   - `Factor → id` vs `Factor → call`
   - Same pattern as `Factor → IDENTIFIER` vs `Factor → FunctionCall`

2. **Condition Conflict** (like full grammar)
   - `Cond → Expr '==' Expr` vs `Cond → '(' Cond ')'`
   - Same pattern as full grammar's Condition conflict

3. **Additional Stmt Conflict**
   - Shows how conflicts propagate upward in the grammar

## Run the Analyzer

```bash
python LL1_minimal/ll1_analyzer.py
```

This will generate the Excel file with all analysis details.
