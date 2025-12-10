; ========== DATA SECTION ==========
i: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 0
    STORE i
    LOAD_IMM 0
    STORE i
L0:
    LOAD i
    CMP_LT 
    STORE t0
    LOAD t0
    JZ L1  ; Jump if zero (false)
    LOAD t2
    JZ L2  ; Jump if zero (false)
    LOAD i
    PRINT
    JMP L2
L2:
    LOAD i
    ADD_IMM 1
    STORE t3
    LOAD t3
    STORE i
    JMP L0
L1:
; END_MAIN