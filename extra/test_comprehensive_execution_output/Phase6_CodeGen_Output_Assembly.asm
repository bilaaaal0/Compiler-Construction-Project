; ========== DATA SECTION ==========
prev: .space 4  ; int
result: .space 4  ; int
a: .space 4  ; int
b: .space 4  ; int
remainder: .space 4  ; int
num: .space 4  ; int
result: .space 4  ; int
sum: .space 4  ; int

; ========== TEXT SECTION ==========
FUNC_factorial:
    LOAD t0
    JZ L0  ; Jump if zero (false)
    JMP L0
L0:
    LOAD n
    SUB_IMM 1
    STORE t1
    LOAD t1
    STORE prev
    STORE t2  ; store return value
    LOAD t2
    STORE result
FUNC_fibonacci:
    LOAD t4
    JZ L1  ; Jump if zero (false)
    JMP L1
L1:
    LOAD t5
    JZ L2  ; Jump if zero (false)
    JMP L2
L2:
    LOAD n
    SUB_IMM 1
    STORE t6
    LOAD t6
    STORE a
    LOAD n
    SUB_IMM 2
    STORE t7
    LOAD t7
    STORE b
    STORE t8  ; store return value
    STORE t9  ; store return value
FUNC_isEven:
    LOAD x
    MOD_IMM 2
    STORE t11
    LOAD t11
    STORE remainder
    LOAD t12
    JZ L3  ; Jump if zero (false)
    JMP L4
L3:
L4:
FUNC_getGrade:
    LOAD t13
    JZ L5  ; Jump if zero (false)
    JMP L8
L5:
    LOAD t14
    JZ L6  ; Jump if zero (false)
    JMP L8
L6:
    LOAD t15
    JZ L7  ; Jump if zero (false)
    JMP L8
L7:
L8:
MAIN:
    LOAD_IMM 5
    STORE num
    LOAD num
    PRINT
    STORE t16  ; store return value
    LOAD t16
    STORE result
    LOAD result
    PRINT
    STORE t17  ; store return value
    LOAD t17
    STORE result
    LOAD result
    PRINT
    STORE t18  ; store return value
    LOAD t18
    STORE result
    LOAD result
    PRINT
    STORE t19  ; store return value
    LOAD t19
    STORE result
    LOAD result
    PRINT
    LOAD_IMM 0
    STORE sum
    LOAD_IMM 1
    STORE i
L9:
    LOAD t20
    JZ L10  ; Jump if zero (false)
    LOAD sum
    ADD i
    STORE t21
    LOAD t21
    STORE sum
    LOAD i
    ADD_IMM 1
    STORE t22
    LOAD t22
    STORE i
    JMP L9
L10:
    LOAD sum
    PRINT