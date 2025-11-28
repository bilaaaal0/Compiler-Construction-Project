; ========== DATA SECTION ==========
x: .space 4  ; int
y: .space 4  ; int
a: .space 4  ; int
b: .space 4  ; int
i: .space 4  ; int
j: .space 4  ; int
m: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 10
    STORE x
    LOAD x
    PRINT
    LOAD_IMM 20
    STORE y
    LOAD y
    PRINT
    LOAD_IMM 5
    STORE a
    LOAD a
    ADD_IMM 3
    STORE t0
    LOAD t0
    STORE b
    LOAD b
    PRINT
    LOAD_IMM 0
    STORE i
L0:
    LOAD t1
    JZ L1  ; Jump if zero (false)
    LOAD i
    PRINT
    LOAD i
    ADD_IMM 1
    STORE t2
    LOAD t2
    STORE i
    JMP L0
L1:
    LOAD_IMM 5
    STORE j
L2:
    LOAD t3
    JZ L3  ; Jump if zero (false)
    LOAD j
    PRINT
    LOAD j
    ADD_IMM 1
    STORE t4
    LOAD t4
    STORE j
    JMP L2
L3:
    LOAD_IMM 10
    STORE k
L4:
    LOAD t5
    JZ L5  ; Jump if zero (false)
    LOAD k
    PRINT
    LOAD k
    ADD_IMM 1
    STORE t6
    LOAD t6
    STORE k
    JMP L4
L5:
    LOAD_IMM 0
    STORE m
L6:
    LOAD m
    CMP_LT 3
    STORE t7
    LOAD t7
    JZ L7  ; Jump if zero (false)
    LOAD m
    PRINT
    LOAD m
    ADD_IMM 1
    STORE t8
    LOAD t8
    STORE m
    JMP L6
L7: