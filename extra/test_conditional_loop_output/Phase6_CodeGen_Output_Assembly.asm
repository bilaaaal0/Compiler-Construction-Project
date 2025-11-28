; ========== DATA SECTION ==========
x: .space 4  ; int
a: .space 4  ; int
b: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 0
    STORE x
L0:
    LOAD x
    CMP_LT 5
    STORE t0
    LOAD t0
    JZ L1  ; Jump if zero (false)
    LOAD x
    PRINT
    LOAD x
    ADD_IMM 1
    STORE t1
    LOAD t1
    STORE x
    JMP L0
L1:
    LOAD x
    PRINT
    LOAD_IMM 10
    STORE a
    LOAD_IMM 0
    STORE b
L2:
    LOAD a
    CMP_GT 0
    STORE t2
    LOAD b
    CMP_LT 5
    STORE t3
    LOAD t2
    AND t3
    STORE t4
    LOAD t4
    JZ L3  ; Jump if zero (false)
    LOAD a
    PRINT
    LOAD b
    PRINT
    LOAD a
    SUB_IMM 1
    STORE t5
    LOAD t5
    STORE a
    LOAD b
    ADD_IMM 1
    STORE t6
    LOAD t6
    STORE b
    JMP L2
L3: