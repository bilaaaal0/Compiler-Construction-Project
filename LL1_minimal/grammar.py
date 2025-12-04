"""
Minimal Grammar for Hand-Written LL(1) Parsing Table
This grammar demonstrates the same conflicts as the full grammar but is small enough
to work with on paper.
"""

grammar = """Program → Stmt

Stmt → Expr ;
     | Cond ;

Expr → Factor ExprBar

ExprBar → + Factor ExprBar
        | ε

Factor → id
       | call
       | ( Expr )

call → id ( )

Cond → Expr == Expr
     | ( Cond )
"""

# Alternative: Even simpler grammar showing just one conflict
simple_grammar = """S → E

E → F

F → id
  | id '(' ')'
"""

grammar2 = """Start → Decl

Decl → Assign :
     | Test :

Assign → Val OpList

OpList → * Val OpList
       | ε

Val → var
    | func
    | [ Assign ]

func → var < >

Test → Assign >= Assign
     | { Test }
"""
