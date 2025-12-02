# LR(0) Parser Analysis

This folder contains a complete LR(0) parser analysis of the custom programming language grammar.

## Files

- **grammar.py** - Grammar definition
- **lr0_analyzer.py** - Complete LR(0) parser analyzer
- **lr0_analysis.xlsx** - Excel file with detailed analysis (6 sheets)
- **ANALYSIS_RESULT.txt** - Summary of analysis results

## Quick Result

**The grammar is NOT LR(0)** ❌

Found 3 shift-reduce conflicts:
1. **State 41** on terminal `(` - Conflict between r23 and s68
2. **State 100** on terminal `&&` - Conflict between r8 and s105
3. **State 132** on terminal `&&` - Conflict between r7 and s105

## LR(0) Automaton

- **171 states** generated
- **501 transitions** created
- Start symbol: `Program`
- Augmented start: `Program'`

## Excel File Contents

The `lr0_analysis.xlsx` file contains 6 sheets:

1. **Result** - Summary with detailed conflict table showing:
   - State number
   - Symbol
   - Conflict type (shift-reduce or reduce-reduce)
   - Action 1
   - Action 2

2. **Grammar** - All productions with numbers:
   - Production number (used in reduce actions)
   - Non-terminal
   - Full production rule

3. **States** - All 171 LR(0) states:
   - State number
   - All items in the state (with dot positions)

4. **ACTION Table** - Parsing action table:
   - Rows: States (0-170)
   - Columns: Terminals
   - Actions: shift (sN), reduce (rN), accept
   - Conflicts highlighted in RED
   - Empty cells marked with "-"

5. **GOTO Table** - State transition table for non-terminals:
   - Rows: States (0-170)
   - Columns: Non-terminals
   - Values: State numbers
   - Empty cells marked with "-"

6. **Transitions** - Complete transition information:
   - From State
   - Symbol
   - To State

## How to Run

```bash
python LR0/lr0_analyzer.py
```

This will:
1. Parse the grammar
2. Augment the grammar with S' → S
3. Build the LR(0) automaton using canonical item set construction
4. Create ACTION and GOTO tables
5. Detect conflicts
6. Generate the Excel file
7. Report whether the grammar is LR(0)

## Understanding the Output

### ACTION Table Entries

- **sN** - Shift to state N
- **rN** - Reduce by production N
- **accept** - Accept the input
- **-** - Error (no action defined)
- **Conflicts** - Multiple actions separated by "/" (highlighted in RED)

### GOTO Table Entries

- **N** - Go to state N after reducing to non-terminal
- **-** - No transition defined

### Conflict Types

- **shift-reduce** - Parser cannot decide whether to shift or reduce
- **reduce-reduce** - Parser cannot decide which production to reduce by

## Why LR(0) Fails

LR(0) parsers make decisions based solely on the current state without lookahead. This grammar requires lookahead to resolve:

1. Factor vs. parenthesized expression (conflict on `(`)
2. Condition reduction vs. continuing with logical operators (conflicts on `&&`)

## Alternative Parsers

Since the grammar is not LR(0), consider:

- **SLR(1)** - Uses FOLLOW sets, may resolve conflicts
- **LALR(1)** - More powerful, commonly used (Yacc, Bison)
- **LR(1)** - Most powerful LR parser
- **GLR** - Handles ambiguous grammars
- **Recursive Descent** - Hand-written with custom conflict resolution

## Dependencies

```bash
pip install openpyxl
```

## LR(0) Item Format

Items are shown as: `A → α·β`

- `A` - Non-terminal being parsed
- `α` - Symbols already seen
- `·` - Current position (dot)
- `β` - Symbols yet to be seen

When the dot is at the end (`A → α·`), it's a complete item indicating a reduce action.
