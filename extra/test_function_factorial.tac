FUNC_factorial:
PARAM n 0
t0 = n <= 1
IF_FALSE t0 GOTO L0
RETURN 1
GOTO L0
L0:
ALLOC temp int
t1 = n - 1
temp = t1
ALLOC result int
PUSH temp
CALL FUNC_factorial 1
t2 = RETVAL
result = t2
t3 = n * result
RETURN t3
RETURN 0
END_FUNC_factorial
MAIN:
ALLOC num int
ALLOC fact int
num = 5
PUSH num
CALL FUNC_factorial 1
t4 = RETVAL
fact = t4
PRINT fact
END_MAIN