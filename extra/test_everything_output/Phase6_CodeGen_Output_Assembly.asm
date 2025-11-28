; ========== DATA SECTION ==========
temp: .space 4  ; int
result: .space 4  ; int
remainder: .space 4  ; int
fact: .space 4  ; int
check: .space 4  ; int
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
    STORE t2  ; store return value
FUNC_isPrime:
    LOAD t4
    JZ L1  ; Jump if zero (false)
    JMP L1
L1:
    LOAD t5
    JZ L2  ; Jump if zero (false)
    JMP L2
L2:
    LOAD_IMM 1
    STORE result
    LOAD_IMM 2
    STORE i
L3:
    LOAD t6
    JZ L4  ; Jump if zero (false)
    LOAD n
    MOD i
    STORE t7
    LOAD t7
    STORE remainder
    LOAD t8
    JZ L5  ; Jump if zero (false)
    LOAD t9
    JZ L6  ; Jump if zero (false)
    LOAD_IMM 0
    STORE result
    JMP L6
L6:
    JMP L5
L5:
    LOAD i
    ADD_IMM 1
    STORE t10
    LOAD t10
    STORE i
    JMP L3
L4:
MAIN:
    LOAD 1
    PRINT
    STORE t11  ; store return value
    LOAD t11
    STORE fact
    LOAD fact
    PRINT
    STORE t12  ; store return value
    LOAD t12
    STORE check
    LOAD check
    PRINT
    LOAD_IMM 0
    STORE sum
    LOAD_IMM 1
    STORE i
L7:
    LOAD t13
    JZ L8  ; Jump if zero (false)
    LOAD i
    CMP_GT 5
    STORE t14
    LOAD t14
    JZ L9  ; Jump if zero (false)
    LOAD sum
    ADD i
    STORE t15
    LOAD t15
    STORE sum
    JMP L9
L9:
    LOAD i
    ADD_IMM 1
    STORE t16
    LOAD t16
    STORE i
    JMP L7
L8:
    LOAD sum
    PRINT