; ========== DATA SECTION ==========
x: .space 4  ; int
y: .space 4  ; int
z: .space 4  ; int
i: .space 4  ; int
j: .space 4  ; int
a: .space 4  ; int
b: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 5
    STORE x
    LOAD_IMM 10
    STORE y
    LOAD_IMM 15
    STORE z
    LOAD t0
    AND t1
    STORE t2
    LOAD t2
    OR t3
    STORE t4
    LOAD t4
    JZ L0  ; Jump if zero (false)
    LOAD x
    PRINT
    LOAD y
    PRINT
    JMP L0
L0:
    LOAD x
    CMP_GT 0
    STORE t5
    LOAD t5
    JZ L1  ; Jump if zero (false)
    LOAD x
    PRINT
    LOAD y
    CMP_GT 5
    STORE t6
    LOAD t6
    JZ L2  ; Jump if zero (false)
    LOAD y
    PRINT
    LOAD z
    CMP_GT 10
    STORE t7
    LOAD t7
    JZ L3  ; Jump if zero (false)
    LOAD z
    PRINT
    JMP L3
L3:
    JMP L2
L2:
    JMP L1
L1:
    LOAD_IMM 0
    STORE i
    LOAD_IMM 0
    STORE j
    LOAD_IMM 0
    STORE i
L4:
    LOAD t8
    JZ L5  ; Jump if zero (false)
    LOAD i
    PRINT
    LOAD_IMM 0
    STORE j
L6:
    LOAD t9
    JZ L7  ; Jump if zero (false)
    LOAD j
    PRINT
    LOAD j
    ADD_IMM 1
    STORE t10
    LOAD t10
    STORE j
    JMP L6
L7:
    LOAD i
    ADD_IMM 1
    STORE t11
    LOAD t11
    STORE i
    JMP L4
L5:
    LOAD_IMM 1
    STORE a
    LOAD_IMM 2
    STORE b
    LOAD_IMM 0
    STORE a
L8:
    LOAD t12
    JZ L9  ; Jump if zero (false)
    LOAD t13
    OR t14
    STORE t15
    LOAD t15
    JZ L10  ; Jump if zero (false)
    LOAD a
    PRINT
    LOAD_IMM 0
    STORE b
L11:
    LOAD t16
    JZ L12  ; Jump if zero (false)
    LOAD b
    CMP_GT 0
    STORE t17
    LOAD a
    CMP_GT 0
    STORE t18
    LOAD t17
    AND t18
    STORE t19
    LOAD t19
    OR t20
    STORE t21
    LOAD t21
    JZ L13  ; Jump if zero (false)
    LOAD b
    PRINT
    JMP L13
L13:
    LOAD b
    ADD_IMM 1
    STORE t22
    LOAD t22
    STORE b
    JMP L11
L12:
    JMP L10
L10:
    LOAD a
    ADD_IMM 1
    STORE t23
    LOAD t23
    STORE a
    JMP L8
L9: