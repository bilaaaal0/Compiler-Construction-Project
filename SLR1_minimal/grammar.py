"""
Grammar for SLR(1) Analysis
Same grammar as LR0_minimal - demonstrates how SLR(1) resolves some conflicts.
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
