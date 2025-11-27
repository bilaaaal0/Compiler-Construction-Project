; ========== DATA SECTION ==========
temp: .space 4  ; int
result: .space 4  ; int
num: .space 4  ; int
fact: .space 4  ; int

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
    LOAD t2
    STORE result
MAIN:
    LOAD_IMM 5
    STORE num
    STORE t4  ; store return value
    LOAD t4
    STORE fact
    LOAD fact
    PRINT