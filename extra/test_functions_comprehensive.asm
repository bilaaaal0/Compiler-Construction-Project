; ========== DATA SECTION ==========
prev: .space 4  ; int
prevFact: .space 4  ; int
newExp: .space 4  ; int
sum: .space 4  ; int
product: .space 4  ; int
result1: .space 4  ; int
result2: .space 4  ; int
result3: .space 4  ; int
result4: .space 4  ; int

; ========== TEXT SECTION ==========
FUNC_add:
FUNC_multiply:
FUNC_factorial:
    LOAD t2
    JZ L0  ; Jump if zero (false)
    JMP L0
L0:
    LOAD n
    SUB_IMM 1
    STORE t3
    LOAD t3
    STORE prev
    STORE t4  ; store return value
    LOAD t4
    STORE prevFact
FUNC_power:
    LOAD t6
    JZ L1  ; Jump if zero (false)
    JMP L1
L1:
    LOAD exp
    SUB_IMM 1
    STORE t7
    LOAD t7
    STORE newExp
    STORE t8  ; store return value
FUNC_calculate:
    STORE t10  ; store return value
    LOAD t10
    STORE sum
    STORE t11  ; store return value
    LOAD t11
    STORE product
MAIN:
    STORE t13  ; store return value
    LOAD t13
    STORE result1
    LOAD result1
    PRINT
    STORE t14  ; store return value
    LOAD t14
    STORE result2
    LOAD result2
    PRINT
    STORE t15  ; store return value
    LOAD t15
    STORE result3
    LOAD result3
    PRINT
    STORE t16  ; store return value
    LOAD t16
    STORE result4
    LOAD result4
    PRINT