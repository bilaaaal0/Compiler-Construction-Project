; ========== DATA SECTION ==========
temp: .space 4  ; int
remainder: .space 4  ; int
sum: .space 4  ; int
product: .space 4  ; int
count: .space 4  ; int
result: .space 4  ; int
check: .space 4  ; int

; ========== TEXT SECTION ==========
FUNC_factorial:
    LOAD t0
    JZ L0  ; Jump if zero (false)
    JMP L0
L0:
    LOAD n
    SUB_IMM 1
    STORE t1
    STORE t2  ; store return value
FUNC_isEven:
    LOAD x
    MOD_IMM 2
    STORE t4
    LOAD t4
    STORE remainder
    LOAD t5
    JZ L1  ; Jump if zero (false)
    JMP L1
L1:
MAIN:
    LOAD_IMM 0
    STORE sum
    LOAD_IMM 1
    STORE product
    LOAD_IMM 0
    STORE count
    LOAD_IMM 1
    STORE i
L2:
    LOAD t6
    JZ L3  ; Jump if zero (false)
    LOAD sum
    ADD i
    STORE t7
    LOAD t7
    STORE sum
    LOAD i
    ADD_IMM 1
    STORE t8
    LOAD t8
    STORE i
    JMP L2
L3:
    LOAD sum
    PRINT
    LOAD_IMM 0
    STORE j
L4:
    LOAD t9
    JZ L5  ; Jump if zero (false)
    LOAD count
    ADD_IMM 1
    STORE t10
    LOAD t10
    STORE count
    LOAD j
    ADD_IMM 2
    STORE t11
    LOAD t11
    STORE j
    JMP L4
L5:
    LOAD count
    PRINT
    STORE t12  ; store return value
    LOAD t12
    STORE result
    LOAD result
    PRINT
    LOAD_IMM 1
    STORE x
L6:
    LOAD t13
    JZ L7  ; Jump if zero (false)
    LOAD_IMM 1
    STORE y
L8:
    LOAD t14
    JZ L9  ; Jump if zero (false)
    STORE t16  ; store return value
    LOAD t16
    STORE check
    LOAD t17
    JZ L10  ; Jump if zero (false)
    LOAD 1
    PRINT
    JMP L11
L10:
    LOAD 0
    PRINT
L11:
    LOAD y
    ADD_IMM 1
    STORE t18
    LOAD t18
    STORE y
    JMP L8
L9:
    LOAD x
    ADD_IMM 1
    STORE t19
    LOAD t19
    STORE x
    JMP L6
L7: