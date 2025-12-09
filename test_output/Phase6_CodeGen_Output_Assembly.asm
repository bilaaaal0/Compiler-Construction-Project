; ========== DATA SECTION ==========
i1: .space 4  ; int
end: .space 4  ; int

; ========== TEXT SECTION ==========
MAIN:
    LOAD_IMM 0
    STORE i1
    READ
    STORE end
    LOAD end
    PRINT