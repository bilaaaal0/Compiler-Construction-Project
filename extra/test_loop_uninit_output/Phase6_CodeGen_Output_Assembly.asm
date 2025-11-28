; ========== DATA SECTION ==========
i: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
L0:
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