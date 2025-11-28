; ========== DATA SECTION ==========
x: .space 4  ; int
y: .space 4  ; int
z: .space 4  ; int
a: .space 4  ; int
i: .space 4  ; int
b: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 10
    STORE x
    LOAD_IMM 20
    STORE y
    LOAD x
    PRINT
    LOAD y
    PRINT
    LOAD_IMM 100
    STORE x
    LOAD_IMM 30
    STORE z
    LOAD x
    PRINT
    LOAD z
    PRINT
    LOAD_IMM 200
    STORE x
    LOAD x
    PRINT
    LOAD x
    PRINT
    LOAD x
    PRINT
    LOAD t0
    JZ L0  ; Jump if zero (false)
    LOAD_IMM 50
    STORE a
    LOAD a
    PRINT
    JMP L0
L0:
    LOAD_IMM 0
    STORE i
    LOAD_IMM 0
    STORE i
L1:
    LOAD t1
    JZ L2  ; Jump if zero (false)
    LOAD_IMM 99
    STORE b
    LOAD b
    PRINT
    LOAD i
    ADD_IMM 1
    STORE t2
    LOAD t2
    STORE i
    JMP L1
L2: