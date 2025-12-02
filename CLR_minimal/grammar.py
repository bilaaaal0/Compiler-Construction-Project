"""
Grammar for CLR (LR(1)) Analysis
Same grammar as LR0_minimal and SLR1_minimal - demonstrates how CLR resolves all conflicts.
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
