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

grammar2 = """Start → Decl

Decl → Assign :
     | Test :

Assign → Val

Val → var
    | func
    | [ Assign ]

func → var < >

Test → Assign >= Assign
     | Test & Test
"""
