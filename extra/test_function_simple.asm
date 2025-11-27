; ========== DATA SECTION ==========
result1: .space 4  ; int
result2: .space 4  ; int
final: .space 4  ; int

; ========== TEXT SECTION ==========
FUNC_add:
FUNC_multiply:
MAIN:
    STORE t2  ; store return value
    LOAD t2
    STORE result1
    STORE t3  ; store return value
    LOAD t3
    STORE result2
    STORE t4  ; store return value
    LOAD t4
    STORE final
    LOAD final
    PRINT