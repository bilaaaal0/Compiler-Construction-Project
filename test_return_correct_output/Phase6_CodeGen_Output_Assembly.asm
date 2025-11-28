; ========== DATA SECTION ==========
sum: .space 4  ; int
x: .space 4  ; int
m: .space 4  ; int

; ========== TEXT SECTION ==========
FUNC_add:
FUNC_printSum:
    LOAD a
    ADD b
    STORE t1
    LOAD t1
    STORE sum
    LOAD sum
    PRINT
FUNC_printValue:
    LOAD x
    PRINT
FUNC_max:
    LOAD a
    CMP_GT b
    STORE t2
    LOAD t2
    JZ L0  ; Jump if zero (false)
    JMP L1
L0:
L1:
MAIN:
    STORE t3  ; store return value
    LOAD t3
    STORE x
    LOAD x
    PRINT
    STORE t6  ; store return value
    LOAD t6
    STORE m
    LOAD m
    PRINT