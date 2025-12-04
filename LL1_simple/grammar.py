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

grammar2 = """Start → DeclList AssignList

DeclList → Declaration DeclList
         | ε

Declaration → 'def' Kind var '< ' InputList ' >' Section

InputList → Input InputRest
          | ε

InputRest → ', ' Input InputRest
          | ε

Input → Kind var

AssignList → Assign AssignList
           | ε

Assign → VarDecl
       | Update
       | Branch
       | Iterate
       | Display
       | Read
       | Exit
       | Section

Section → '{ ' AssignList ' }'

VarDecl → Kind var ': '
        | Kind var ': ' Val ': '

Kind → 'num'
     | 'text'
     | 'flag'
     | 'none'

Update → var ': ' Val ': '

Branch → 'check '< ' Test ' >' Section OptionList DefaultPart

OptionList → 'option '< ' Test ' >' Section OptionList
           | ε

DefaultPart → 'default ' Section
            | ε

Iterate → 'repeat ' 'start ' var ': ' Val ' end ' Val ' step ' Val Section
        | 'repeat ' 'start ' var ': ' Val ' end ' Val Section
        | 'repeat ' 'start ' var ' end ' Val ' step ' Val Section
        | 'repeat ' 'start ' var ' end ' Val Section
        | 'repeat '< ' Test ' >' Section

Display → 'print ' ValList ': '

ValList → Val ValRest

ValRest → ', ' Val ValRest
        | ε

Read → 'input ' var ': '

Exit → 'stop ' Val ': '
     | 'stop ': '

Test → Val Compare Val
     | Test Logic Test
     | '! ' Test
     | '< ' Test ' >'

Val → Unit Prime

Prime → '* ' Unit Prime
      | '/ ' Unit Prime
      | ε

Unit → Element Rest

Rest → '+ ' Element Rest
     | '- ' Element Rest
     | ε

Element → var
        | func
        | NUM_VAL
        | TEXT_VAL
        | FLAG_VAL
        | '< ' Val ' >'
        | '- ' Element

func → var '< ' Args ' >'

Args → Val ArgRest
     | ε

ArgRest → ', ' Val ArgRest
        | ε

Compare → '>= ' | '!= ' | '< ' | '> ' | '<= ' | '== '

Logic → '& ' | '| '
"""