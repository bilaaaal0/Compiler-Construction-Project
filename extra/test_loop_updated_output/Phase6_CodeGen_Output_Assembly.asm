; ========== DATA SECTION ==========
sum: .space 4  ; int
product: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 0
    STORE sum
    LOAD_IMM 1
    STORE product
    LOAD_IMM 1
    STORE i
L0:
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
    LOAD_IMM 1
    STORE j
L2:
    LOAD t3
    JZ L3  ; Jump if zero (false)
    LOAD product
    MUL j
    STORE t4
    LOAD t4
    STORE product
    LOAD j
    ADD_IMM 1
    STORE t5
    LOAD t5
    STORE j
    JMP L2
L3:
    LOAD product
    PRINT