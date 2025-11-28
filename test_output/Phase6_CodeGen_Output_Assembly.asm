; ========== DATA SECTION ==========
i: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 0
    STORE i
L0:
    LOAD i
    CMP_LT 10
    STORE t0
    LOAD t0
    JZ L1  ; Jump if zero (false)
    LOAD i
    PRINT
    LOAD i
    ADD_IMM 1
    STORE t1
    LOAD t1
    STORE i
    JMP L0
L1: