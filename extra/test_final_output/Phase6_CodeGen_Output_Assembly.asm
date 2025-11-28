; ========== DATA SECTION ==========
x: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 100
    STORE x
    LOAD x
    PRINT