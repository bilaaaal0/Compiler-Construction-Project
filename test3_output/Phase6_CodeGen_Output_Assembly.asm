; ========== DATA SECTION ==========
sum: .space 4  ; int
temp: .space 4  ; int
result1: .space 4  ; int
result2: .space 4  ; int

; ========== TEXT SECTION ==========
FUNC_add:
    POP a  ; param 0
    POP b  ; param 1
    LOAD a
    ADD b
    STORE t0
    LOAD t0
    STORE sum
    LOAD sum
    RET
    LOAD_IMM 0
    RET
; END_FUNC_add
FUNC_factorial:
    POP n  ; param 0
    LOAD n
    CMP_LT 
    STORE t1
    LOAD t1
    JZ L0  ; Jump if zero (false)
    LOAD_IMM 1
    RET
    JMP L0
L0:
    LOAD n
    SUB_IMM 1
    STORE t2
    LOAD t2
    STORE temp
    LOAD temp
    PUSH
    CALL FUNC_factorial  ; 1 args
    STORE t3  ; store return value
    LOAD n
    MUL t3
    STORE t4
    LOAD t4
    RET
    LOAD_IMM 0
    RET
; END_FUNC_factorial
FUNC_printMessage:
    POP x  ; param 0
    LOAD x
    PRINT
    LOAD x
    ADD_IMM 1
    STORE t5
    LOAD t5
    PRINT
    LOAD_IMM 0
    RET
; END_FUNC_printMessage
MAIN:
    LOAD_IMM 3
    PUSH
    LOAD_IMM 5
    PUSH
    CALL FUNC_add  ; 2 args
    STORE t6  ; store return value
    LOAD t6
    STORE result1
    LOAD result1
    PRINT
    LOAD_IMM 5
    PUSH
    CALL FUNC_factorial  ; 1 args
    STORE t7  ; store return value
    LOAD t7
    STORE result2
    LOAD result2
    PRINT
    LOAD_IMM 10
    PUSH
    CALL FUNC_printMessage  ; 1 args
; END_MAIN