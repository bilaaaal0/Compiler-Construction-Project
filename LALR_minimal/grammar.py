"""
Grammar for LALR(1) Analysis
Same grammar as LR0_minimal, SLR1_minimal, and CLR_minimal
LALR(1) is the industry standard - used in Yacc, Bison, etc.
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
