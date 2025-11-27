; ========== DATA SECTION ==========
a: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 10
    STORE a
    LOAD a
    ADD_IMM 3
    STORE t0
    LOAD t0
    PRINT