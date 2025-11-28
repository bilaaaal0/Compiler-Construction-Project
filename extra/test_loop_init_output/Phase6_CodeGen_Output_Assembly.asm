; ========== DATA SECTION ==========
i: .space 4  ; int
j: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 2
    STORE i
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
    LOAD_IMM 0
    STORE j
L2:
    LOAD t2
    JZ L3  ; Jump if zero (false)
    LOAD j
    PRINT
    LOAD j
    ADD_IMM 1
    STORE t3
    LOAD t3
    STORE j
    JMP L2
L3: