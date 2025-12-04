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
