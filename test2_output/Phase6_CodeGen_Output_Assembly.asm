; ========== DATA SECTION ==========
sum: .space 4  ; int
result: .space 4  ; int
counter: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 0
    STORE sum
    LOAD_IMM 1
    STORE i
L0:
    LOAD i
    CMP_LT 
    STORE t0
    LOAD t0
    JZ L1  ; Jump if zero (false)
    LOAD sum
    ADD i
    STORE t1
    LOAD t1
    STORE sum
    LOAD i
    ADD_IMM 1
    STORE t2
    LOAD t2
    STORE i
    JMP L0
L1:
    LOAD sum
    PRINT
    LOAD_IMM 0
    STORE result
    LOAD_IMM 0
    STORE j
L2:
    LOAD j
    CMP_LT 
    STORE t3
    LOAD t3
    JZ L3  ; Jump if zero (false)
    LOAD result
    ADD j
    STORE t4
    LOAD t4
    STORE result
    LOAD j
    ADD_IMM 2
    STORE t5
    LOAD t5
    STORE j
    JMP L2
L3:
    LOAD result
    PRINT
    LOAD_IMM 0
    STORE counter
L4:
    LOAD counter
    CMP_LT 5
    STORE t6
    LOAD t6
    JZ L5  ; Jump if zero (false)
    LOAD counter
    PRINT
    LOAD counter
    ADD_IMM 1
    STORE t7
    LOAD t7
    STORE counter
    JMP L4
L5:
; END_MAIN