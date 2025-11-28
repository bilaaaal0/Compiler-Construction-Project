; ========== DATA SECTION ==========
x: .space 4  ; int
y: .space 4  ; int
z: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 10
    STORE x
    LOAD_IMM 20
    STORE y
    LOAD_IMM 30
    STORE z
    LOAD x
    PRINT
    LOAD x
    PRINT
    LOAD y
    PRINT
    LOAD z
    PRINT
    LOAD x
    ADD y
    STORE t0
    LOAD t0
    PRINT
    LOAD x
    MUL_IMM 2
    STORE t1
    LOAD t1
    PRINT
    LOAD z
    SUB_IMM 5
    STORE t2
    LOAD t2
    PRINT
    LOAD x
    PRINT
    LOAD x
    ADD y
    STORE t3
    LOAD t3
    PRINT
    LOAD y
    PRINT
    LOAD y
    MUL z
    STORE t4
    LOAD t4
    PRINT
    LOAD_IMM 0
    STORE i
L0:
    LOAD t5
    JZ L1  ; Jump if zero (false)
    LOAD i
    PRINT
    LOAD i
    MUL_IMM 2
    STORE t6
    LOAD t6
    PRINT
    LOAD i
    ADD_IMM 10
    STORE t7
    LOAD t7
    PRINT
    LOAD i
    ADD_IMM 1
    STORE t8
    LOAD t8
    STORE i
    JMP L0
L1: