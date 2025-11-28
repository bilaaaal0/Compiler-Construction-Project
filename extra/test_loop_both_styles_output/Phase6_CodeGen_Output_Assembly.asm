; ========== DATA SECTION ==========
sum1: .space 4  ; int
sum2: .space 4  ; int
j: .space 4  ; int
k: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 0
    STORE sum1
    LOAD_IMM 0
    STORE sum2
    LOAD_IMM 1
    STORE i
L0:
    LOAD t0
    JZ L1  ; Jump if zero (false)
    LOAD sum1
    ADD i
    STORE t1
    LOAD t1
    STORE sum1
    LOAD i
    ADD_IMM 1
    STORE t2
    LOAD t2
    STORE i
    JMP L0
L1:
    LOAD sum1
    PRINT
    LOAD_IMM 5
    STORE j
L2:
    LOAD t3
    JZ L3  ; Jump if zero (false)
    LOAD sum2
    ADD j
    STORE t4
    LOAD t4
    STORE sum2
    LOAD j
    ADD_IMM 1
    STORE t5
    LOAD t5
    STORE j
    JMP L2
L3:
    LOAD sum2
    PRINT
    LOAD_IMM 0
    STORE k
L4:
    LOAD t6
    JZ L5  ; Jump if zero (false)
    LOAD k
    PRINT
    LOAD k
    ADD_IMM 2
    STORE t7
    LOAD t7
    STORE k
    JMP L4
L5: