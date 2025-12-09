; ========== DATA SECTION ==========
score: .space 4  ; int
x: .space 4  ; int
y: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 85
    STORE score
    LOAD score
    CMP_GT 
    STORE t0
    LOAD t0
    JZ L0  ; Jump if zero (false)
    LOAD 1
    PRINT
    JMP L3
L0:
    LOAD score
    CMP_GT 
    STORE t1
    LOAD t1
    JZ L1  ; Jump if zero (false)
    LOAD 2
    PRINT
    JMP L3
L1:
    LOAD score
    CMP_GT 
    STORE t2
    LOAD t2
    JZ L2  ; Jump if zero (false)
    LOAD 3
    PRINT
    JMP L3
L2:
    LOAD 0
    PRINT
L3:
    LOAD_IMM 10
    STORE x
    LOAD_IMM 20
    STORE y
    LOAD x
    CMP_LT y
    STORE t3
    LOAD t3
    JZ L4  ; Jump if zero (false)
    LOAD x
    CMP_GT 5
    STORE t4
    LOAD t4
    JZ L6  ; Jump if zero (false)
    LOAD x
    PRINT
    JMP L7
L6:
    LOAD 0
    PRINT
L7:
    JMP L5
L4:
    LOAD y
    PRINT
L5:
; END_MAIN