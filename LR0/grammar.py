grammar = """Program → FunctionList StmtList

FunctionList → FunctionDecl FunctionList
             | ε

FunctionDecl → 'func' Type IDENTIFIER '(' ParamList ')' Block

ParamList → Param ParamListTail
          | ε

ParamListTail → ',' Param ParamListTail
              | ε

Param → Type IDENTIFIER

StmtList → Stmt StmtList
         | ε

Stmt → DeclStmt
     | AssignStmt
     | IfStmt
     | LoopStmt
     | ShowStmt
     | TellStmt
     | ReturnStmt
     | Block

Block → '{' StmtList '}'

DeclStmt → Type IDENTIFIER ';'                    
         | Type IDENTIFIER '=' Expr ';'            
Type → 'int'
     | 'float'
     | 'char'
     | 'void'

AssignStmt → IDENTIFIER '=' Expr ';'

IfStmt → 'if' '(' Condition ')' Block ElifList ElsePart

ElifList → 'elif' '(' Condition ')' Block ElifList
         | ε

ElsePart → 'else' Block
         | ε

LoopStmt → 'loop' 'from' IDENTIFIER '=' Expr 'to' Expr 'step' Expr Block
         | 'loop' 'from' IDENTIFIER '=' Expr 'to' Expr Block
         | 'loop' 'from' IDENTIFIER 'to' Expr 'step' Expr Block
         | 'loop' 'from' IDENTIFIER 'to' Expr Block
         | 'loop' '(' Condition ')' Block

ShowStmt → 'show' ExprList ';'

ExprList → Expr ExprListTail

ExprListTail → ',' Expr ExprListTail
             | ε

TellStmt → 'tell' IDENTIFIER ';'

ReturnStmt → 'return' Expr ';'
           | 'return' ';'

Condition → Expr RelOp Expr
          | Condition LogicOp Condition
          | '!' Condition
          | '(' Condition ')'

Expr → Term ExprPrime

ExprPrime → '+' Term ExprPrime
          | '-' Term ExprPrime
          | ε

Term → Factor TermPrime

TermPrime → '*' Factor TermPrime
          | '/' Factor TermPrime
          | '%' Factor TermPrime
          | ε

Factor → IDENTIFIER
       | FunctionCall
       | INTEGER_LITERAL
       | FLOAT_LITERAL
       | CHAR_LITERAL
       | '(' Expr ')'
       | '-' Factor

FunctionCall → IDENTIFIER '(' ArgList ')'

ArgList → Expr ArgListTail
        | ε

ArgListTail → ',' Expr ArgListTail
            | ε

RelOp → '==' | '!=' | '<' | '>' | '<=' | '>='

LogicOp → '&&' | '||' 
"""