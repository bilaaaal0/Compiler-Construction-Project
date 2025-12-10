; ========== DATA SECTION ==========
x: .space 4  ; int
y: .space 4  ; int
pi: .space 4  ; float
grade: .space 1  ; char
result: .space 4  ; float
code: .space 4  ; int
counter: .space 4  ; int
x: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 10
    STORE x
    LOAD_IMM 3.14
    STORE pi
    LOAD 'A'
    STORE grade
    LOAD_IMM 5
    STORE y
    LOAD x
    PRINT
    LOAD y
    PRINT
    LOAD pi
    PRINT
    LOAD x
    ADD pi
    STORE t0
    LOAD t0
    STORE result
    LOAD result
    PRINT
    LOAD grade
    STORE code
    LOAD code
    PRINT
    LOAD x
    CMP_GT y
    STORE t1
    LOAD t1
    JZ L0  ; Jump if zero (false)
    LOAD 1
    PRINT
    JMP L2
L0:
    LOAD t2
    JZ L1  ; Jump if zero (false)
    LOAD 0
    PRINT
    JMP L2
L1:
    LOAD 
    SUB_IMM 1
    STORE t3
    LOAD t3
    PRINT
L2:
    LOAD_IMM 0
    STORE counter
L3:
    LOAD counter
    CMP_LT 3
    STORE t4
    LOAD t4
    JZ L4  ; Jump if zero (false)
    LOAD counter
    PRINT
    LOAD counter
    ADD_IMM 1
    STORE t5
    LOAD t5
    STORE counter
    JMP L3
L4:
    LOAD_IMM 0
    STORE counter
L5:
    LOAD counter
    CMP_LT 
    STORE t6
    LOAD t6
    JZ L6  ; Jump if zero (false)
    LOAD counter
    PRINT
    LOAD counter
    ADD_IMM 2
    STORE t7
    LOAD t7
    STORE counter
    JMP L5
L6:
    LOAD_IMM 100
    STORE x
    LOAD x
    PRINT
    LOAD x
    PRINT
; END_MAIN