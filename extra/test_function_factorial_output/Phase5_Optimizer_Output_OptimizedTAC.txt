FUNC_factorial:
IF_FALSE t0 GOTO L0
GOTO L0
L0:
ALLOC temp int
t1 = n - 1
ALLOC result int
t2 = RETVAL
result = t2
MAIN:
ALLOC num int
ALLOC fact int
num = 5
t4 = RETVAL
fact = t4
PRINT fact