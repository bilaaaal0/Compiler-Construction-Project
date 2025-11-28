; ========== DATA SECTION ==========
a: .space 4  ; int
b: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 3
    STORE a
    LOAD t0
    OR t1
    STORE t2
    LOAD t2
    JZ L0  ; Jump if zero (false)
    LOAD a
    PRINT
    LOAD_IMM 6
    STORE b
    LOAD t3
    AND t4
    STORE t5
    LOAD t5
    JZ L1  ; Jump if zero (false)
    LOAD b
    PRINT
    JMP L2
L1:
    LOAD a
    ADD b
    STORE t6
    LOAD t6
    PRINT
L2:
    JMP L0
L0: