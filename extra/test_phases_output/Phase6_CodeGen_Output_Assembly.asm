; ========== DATA SECTION ==========
x: .space 4  ; int
y: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 10
    STORE x
    LOAD x
    ADD_IMM 5
    STORE t0
    LOAD t0
    STORE y
    LOAD y
    CMP_GT 10
    STORE t1
    LOAD t1
    JZ L0  ; Jump if zero (false)
    LOAD y
    PRINT
    JMP L0
L0: