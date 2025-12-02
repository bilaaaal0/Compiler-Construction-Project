"""
Minimal Grammar for Hand-Written LR(0) Parsing Tables
Extracted from the full grammar - demonstrates the EXACT conflicts that occur.

This grammar shows:
1. Factor conflict: IDENTIFIER vs FunctionCall (when seeing '(')
2. Condition conflict: Logical operators with left recursion (when seeing '&&')
"""

grammar = """Program → Stmt

Stmt → Expr ;
     | Cond ;

Expr → Factor

Factor → IDENTIFIER
       | FunctionCall
       | ( Expr )

FunctionCall → IDENTIFIER ( )

Cond → Expr == Expr
     | Cond && Cond
"""
