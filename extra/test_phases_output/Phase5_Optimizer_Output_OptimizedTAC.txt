MAIN:
ALLOC x int
ALLOC y int
x = 10
t0 = x + 5
y = t0
t1 = y > 10
IF_FALSE t1 GOTO L0
PRINT y
GOTO L0
L0: