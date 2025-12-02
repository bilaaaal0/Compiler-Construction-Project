# LL(1) Grammar Analysis

This folder contains a complete LL(1) analysis of the custom programming language grammar.

## Files

- **grammar.py** - Original grammar definition
- **ll1_analyzer.py** - Complete LL(1) analysis tool
- **grammar_analysis.xlsx** - Excel file with detailed analysis (7 sheets)
- **ANALYSIS_RESULT.txt** - Summary of analysis results

## Quick Result

**The grammar is NOT LL(1)** ❌

Found 2 conflicts:
1. **Condition** on terminal `(` - Cannot distinguish between Expr starting with `(` and parenthesized Condition
2. **Factor** on terminal `IDENTIFIER` - Cannot distinguish between variable and function call

## Excel File Contents

The `grammar_analysis.xlsx` file contains 7 sheets:

1. **Result** - Summary and LL(1) determination with detailed conflict table showing:
   - Non-Terminal
   - Terminal
   - Production 1
   - Production 2
2. **Original Grammar** - Grammar before transformations
3. **Transformed Grammar** - Grammar after left recursion elimination and left factoring
4. **NULLABLE** - Set of nullable non-terminals
5. **FIRST Sets** - FIRST sets for all non-terminals
6. **FOLLOW Sets** - FOLLOW sets for all non-terminals
7. **Parsing Table** - Complete predictive parsing table with:
   - Conflicts highlighted in RED
   - Empty cells marked with "-"
   - Full production rules in each cell

## Transformations Applied

### Left Recursion Elimination
- Eliminated left recursion in `Condition` production

### Left Factoring
- Factored `DeclStmt` (common prefix: `Type IDENTIFIER`)
- Factored `LoopStmt` (multiple levels of factoring)
- Factored `ReturnStmt` (common prefix: `return`)
- Factored `ArgList` (common prefix: `IDENTIFIER`)

## How to Run

```bash
python LL1_simple/ll1_analyzer.py
```

This will:
1. Parse the grammar
2. Eliminate left recursion
3. Perform left factoring
4. Compute NULLABLE, FIRST, and FOLLOW sets
5. Build the predictive parsing table
6. Generate the Excel file
7. Report whether the grammar is LL(1)

## Conflict Resolution Format

In the parsing table, conflicts are shown using the format:
```
A→α / A→β
```

This indicates that for non-terminal A on a specific terminal, there are two possible productions (α and β).

## Dependencies

```bash
pip install openpyxl
```
