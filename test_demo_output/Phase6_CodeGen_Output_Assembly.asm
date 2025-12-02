; ========== DATA SECTION ==========
score: .space 4  ; int
average: .space 4  ; float
count: .space 4  ; int
num: .space 4  ; int
x: .space 4  ; int
y: .space 4  ; int
fact: .space 4  ; int

; ========== TEXT SECTION ==========
FUNC_Factorial:
    LOAD t0
    JZ L0  ; Jump if zero (false)
    JMP L0
L0:
    STORE t2  ; store return value
MAIN:
    LOAD_IMM 0
    STORE score
    LOAD_IMM 0.0
    STORE average
    LOAD_IMM 5
    STORE count
    LOAD_IMM 1
    STORE i
L1:
    LOAD t4
    JZ L2  ; Jump if zero (false)
    LOAD score
    ADD i
    STORE t5
    LOAD t5
    STORE score
    LOAD i
    ADD_IMM 1
    STORE t6
    LOAD t6
    STORE i
    JMP L1
L2:
    LOAD score
    STORE average
    LOAD score
    PRINT
    LOAD average
    PRINT
    LOAD score
    CMP_GT 20
    STORE t7
    LOAD t7
    JZ L3  ; Jump if zero (false)
    LOAD 100
    PRINT
    JMP L6
L3:
    LOAD score
    CMP_GT 15
    STORE t8
    LOAD t8
    JZ L4  ; Jump if zero (false)
    LOAD 200
    PRINT
    JMP L6
L4:
    LOAD score
    CMP_GT 10
    STORE t9
    LOAD t9
    JZ L5  ; Jump if zero (false)
    LOAD 300
    PRINT
    JMP L6
L5:
    LOAD 400
    PRINT
L6:
    LOAD_IMM 0
    STORE num
L7:
    LOAD num
    CMP_LT 5
    STORE t10
    LOAD t10
    JZ L8  ; Jump if zero (false)
    LOAD t11
    JZ L9  ; Jump if zero (false)
    LOAD 1000
    PRINT
    JMP L11
L9:
    LOAD t12
    JZ L10  ; Jump if zero (false)
    LOAD 2000
    PRINT
    JMP L11
L10:
    LOAD num
    PRINT
L11:
    LOAD num
    ADD_IMM 1
    STORE t13
    LOAD t13
    STORE num
    JMP L7
L8:
    LOAD_IMM 0
    STORE x
    LOAD_IMM 0
    STORE x
L12:
    LOAD t14
    JZ L13  ; Jump if zero (false)
    LOAD_IMM 0
    STORE y
    LOAD_IMM 0
    STORE y
L14:
    LOAD t15
    JZ L15  ; Jump if zero (false)
    LOAD t16
    JZ L16  ; Jump if zero (false)
    LOAD 9999
    PRINT
    JMP L18
L16:
    LOAD x
    CMP_GT y
    STORE t17
    LOAD t17
    JZ L17  ; Jump if zero (false)
    LOAD x
    PRINT
    JMP L18
L17:
    LOAD y
    PRINT
L18:
    LOAD y
    ADD_IMM 1
    STORE t18
    LOAD t18
    STORE y
    JMP L14
L15:
    LOAD x
    ADD_IMM 1
    STORE t19
    LOAD t19
    STORE x
    JMP L12
L13:
    STORE t20  ; store return value
    LOAD t20
    STORE fact
    LOAD fact
    PRINT