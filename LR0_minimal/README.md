# LR(0) Minimal Grammar - For Hand-Written Parsing Tables

This folder contains a **simplified grammar** extracted from your full grammar that demonstrates the EXACT conflicts that occur in LR(0) parsing. It's small enough to work with on paper.

## Why This Grammar?

The full grammar has:
- **171 states** in LR(0) automaton 😱
- **33 non-terminals** × **42 terminals**
- Impossible to build by hand

This minimal grammar has:
- **20 states** in LR(0) automaton ✓
- **7 non-terminals** × **7 terminals**
- **Manageable** for hand-written work!

## Grammar

```
Program → Stmt

Stmt → Expr ';'
     | Cond ';'

Expr → Factor

Factor → IDENTIFIER
       | FunctionCall
       | '(' Expr ')'

FunctionCall → IDENTIFIER '(' ')'

Cond → Expr '==' Expr
     | Cond '&&' Cond
```

## Grammar Components

**Non-Terminals (7):**
- Program' (augmented start)
- Program
- Stmt
- Expr
- Factor
- FunctionCall
- Cond

**Terminals (7):**
- IDENTIFIER
- '('
- ')'
- ';'
- '=='
- '&&'
- $

## Analysis Results

**Is LR(0)?** ❌ NO (2 conflicts)
**Is SLR(1)?** ❌ NO (1 conflict)

**States Generated:** 20

**LR(0) Conflicts:** 2
**SLR(1) Conflicts:** 1
**Improvement:** ✓ SLR(1) resolved 1 out of 2 conflicts (50%)

### Conflict Details

1. **State 2** on `(` → **shift-reduce conflict**
   - **Reduce:** r3 (Factor → IDENTIFIER)
   - **Shift:** s9 (to parse '(' for FunctionCall or parenthesized Expr)
   - **Problem:** After seeing IDENTIFIER, parser doesn't know if:
     - It's a simple identifier (reduce)
     - It's start of function call IDENTIFIER'('')' (shift)

2. **State 16** on `&&` → **shift-reduce conflict**
   - **Reduce:** r1 (Cond → Expr '==' Expr)
   - **Shift:** s11 (to parse '&&' for Cond '&&' Cond)
   - **Problem:** After parsing "Expr == Expr", parser doesn't know if:
     - Complete condition (reduce)
     - Part of larger condition with && (shift)

## Why These Are The EXACT Conflicts From Full Grammar

### Conflict 1: Factor/FunctionCall (Same as Full Grammar)

**Full Grammar:**
```
Factor → IDENTIFIER
Factor → FunctionCall
FunctionCall → IDENTIFIER '(' ArgList ')'
```

**Minimal Grammar:**
```
Factor → IDENTIFIER
Factor → FunctionCall
FunctionCall → IDENTIFIER '(' ')'
```

**Same Pattern:** Both start with IDENTIFIER, causing shift-reduce conflict on '('

### Conflict 2: Condition with && (Same as Full Grammar)

**Full Grammar:**
```
Condition → Expr RelOp Expr
Condition → Condition LogicOp Condition
LogicOp → '&&' | '||'
```

**Minimal Grammar:**
```
Cond → Expr '==' Expr
Cond → Cond '&&' Cond
```

**Same Pattern:** Left recursion with logical operators causes shift-reduce conflict on '&&'

## LR(0) Automaton Size

- **20 states** (vs 171 in full grammar)
- **33 transitions** (vs 501 in full grammar)
- **88% reduction** in complexity!

## Parsing Tables Size

**ACTION Table:**
- 20 states × 7 terminals = **140 cells**
- Manageable for hand-written work

**GOTO Table:**
- 20 states × 7 non-terminals = **140 cells**
- Can be completed in 1-2 hours

## Excel File Contents

The `lr0_analysis.xlsx` file contains 11 sheets:

1. **Result** - Summary with LR(0) and SLR(1) results
2. **Grammar** - All productions with numbers
3. **States** - All 20 LR(0) states with items
4. **ACTION Table** - LR(0) parsing actions (conflicts in RED)
5. **GOTO Table** - LR(0) state transitions
6. **SLR(1) ACTION Table** - SLR(1) parsing actions (fewer conflicts!)
7. **SLR(1) GOTO Table** - SLR(1) state transitions
8. **FOLLOW Sets** - FOLLOW sets used by SLR(1)
9. **LR(0) vs SLR(1)** - Comparison showing improvements
10. **Transitions** - Complete transition information
11. **Hand-Written Guide** - Step-by-step instructions for both

## How to Use for Hand-Written Tables

### Step 1: Augment Grammar
```
Program' → Program
```

### Step 2: Create Initial State (I0)
```
Program' → · Program
```

### Step 3: Compute Closure
Add items for all productions of non-terminals after the dot

### Step 4: Build States
Use GOTO function to create new states

### Step 5: Build ACTION Table
- If item is `A → α · a β`, add shift to ACTION[state, a]
- If item is `A → α ·`, add reduce to ACTION[state, all terminals]
- If item is `S' → S ·`, add accept to ACTION[state, $]

### Step 6: Build GOTO Table
- Add state transitions for non-terminals

### Step 7: Identify Conflicts
- Cells with multiple actions are conflicts

## Example States

**State 0 (Initial):**
```
Program' → · Program
Program → · Stmt
Stmt → · Expr ';'
Stmt → · Cond ';'
Expr → · Factor
Factor → · IDENTIFIER
Factor → · FunctionCall
Factor → · '(' Expr ')'
FunctionCall → · IDENTIFIER '(' ')'
Cond → · Expr '==' Expr
Cond → · Cond '&&' Cond
```

**State 2 (After IDENTIFIER):**
```
Factor → IDENTIFIER ·           ← Complete item (reduce)
FunctionCall → IDENTIFIER · '(' ')'  ← Incomplete item (shift on '(')
```
**CONFLICT!** On '(': reduce r3 or shift s9?

## Comparison with Full Grammar

| Aspect | Full Grammar | Minimal Grammar |
|--------|--------------|-----------------|
| States | 171 | 20 |
| Transitions | 501 | 33 |
| Non-Terminals | 33 | 7 |
| Terminals | 42 | 7 |
| Conflicts | 3 | 2 |
| Hand-Writable? | ❌ No | ✅ Yes |
| Time to Complete | 8-12 hours | 1-2 hours |

## What's Preserved

✓ **Factor/IDENTIFIER conflict** - Exact same pattern
✓ **Condition/&& conflict** - Exact same pattern
✓ **Shift-reduce conflicts** - Same type
✓ **Left recursion issue** - Same problem
✓ **LR(0) limitations** - Same demonstration

## What's Simplified

✗ Removed: Functions with parameters
✗ Removed: Multiple statement types
✗ Removed: Complex expressions (only Factor level)
✗ Removed: Multiple operators (only ==, &&)
✗ Removed: ArgList complexity

But kept: **The exact conflict-causing patterns!**

## Run the Analyzer

```bash
python LR0_minimal/lr0_analyzer.py
```

This will generate the Excel file with all analysis details.

## Practice Exercise

Try building the LR(0) automaton and parsing tables by hand:

1. Augment the grammar
2. Create state 0 with closure
3. Build all 20 states using GOTO
4. Fill ACTION table (20 × 7 = 140 cells)
5. Fill GOTO table (20 × 7 = 140 cells)
6. Identify the 2 conflicts
7. Check your work against the Excel file

Expected time: 1-2 hours

## Key Learning Points

1. **LR(0) Items** - Understanding dot positions
2. **Closure Operation** - Adding items for non-terminals
3. **GOTO Function** - Creating new states
4. **ACTION Table** - Shift and reduce actions
5. **GOTO Table** - Non-terminal transitions
6. **Shift-Reduce Conflicts** - Why LR(0) fails
7. **Need for Lookahead** - Why SLR/LALR needed

## Why LR(0) Fails

**Conflict 1 (Factor):**
- After IDENTIFIER, seeing '(' could mean:
  - End of identifier (reduce)
  - Start of function call (shift)
- LR(0) has no lookahead to decide

**Conflict 2 (Condition):**
- After "Expr == Expr", seeing '&&' could mean:
  - Complete condition (reduce)
  - Part of larger condition (shift)
- LR(0) cannot determine operator precedence

## SLR(1) Analysis Included!

This analyzer also performs SLR(1) analysis:

**SLR(1) Results:**
- ✓ Resolved Factor/FunctionCall conflict (State 7, '(')
- ✗ Condition/&& conflict persists (State 16, '&&')

**Why SLR(1) is Better:**
- Uses FOLLOW sets instead of all terminals
- More precise reduce decisions
- Resolves 50% of conflicts in this grammar

**Why SLR(1) Still Fails:**
- '&&' is in FOLLOW(Cond)
- Cannot distinguish operator precedence
- Needs LALR(1) or LR(1) for full resolution

See `SLR_ANALYSIS.txt` for detailed explanation!

## Next Steps

After mastering this grammar:

1. ✓ Understand LR(0) limitations
2. ✓ Understand SLR(1) improvements (included!)
3. Try LALR(1) analysis (uses lookahead)
4. Compare how each resolves conflicts
5. Understand why LALR(1) is industry standard
