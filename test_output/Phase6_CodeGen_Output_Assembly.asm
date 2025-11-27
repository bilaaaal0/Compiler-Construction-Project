; ========== DATA SECTION ==========
a: .space 4  ; int
b: .space 4  ; int

; ========== TEXT SECTION ==========
FUNC_Sum:
MAIN:
    LOAD_IMM 3
    STORE a
    LOAD_IMM 4
    STORE b
    LOAD a
    PRINT
    LOAD b
    PRINT
    STORE t1  ; store return value
    LOAD t1
    PRINT