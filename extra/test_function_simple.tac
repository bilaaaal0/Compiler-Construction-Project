FUNC_add:
PARAM a 0
PARAM b 1
t0 = a + b
RETURN t0
RETURN 0
END_FUNC_add
FUNC_multiply:
PARAM x 0
PARAM y 1
t1 = x * y
RETURN t1
RETURN 0
END_FUNC_multiply
MAIN:
ALLOC result1 int
ALLOC result2 int
ALLOC final int
PUSH 3
PUSH 5
CALL FUNC_add 2
t2 = RETVAL
result1 = t2
PUSH 2
PUSH 4
CALL FUNC_multiply 2
t3 = RETVAL
result2 = t3
PUSH result2
PUSH result1
CALL FUNC_add 2
t4 = RETVAL
final = t4
PRINT final
END_MAIN