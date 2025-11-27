FUNC_add:
FUNC_multiply:
FUNC_factorial:
IF_FALSE t2 GOTO L0
GOTO L0
L0:
ALLOC prev int
t3 = n - 1
prev = t3
ALLOC prevFact int
t4 = RETVAL
prevFact = t4
FUNC_power:
IF_FALSE t6 GOTO L1
GOTO L1
L1:
ALLOC newExp int
t7 = exp - 1
newExp = t7
t8 = RETVAL
FUNC_calculate:
ALLOC sum int
ALLOC product int
t10 = RETVAL
sum = t10
t11 = RETVAL
product = t11
MAIN:
ALLOC result1 int
ALLOC result2 int
ALLOC result3 int
ALLOC result4 int
t13 = RETVAL
result1 = t13
PRINT result1
t14 = RETVAL
result2 = t14
PRINT result2
t15 = RETVAL
result3 = t15
PRINT result3
t16 = RETVAL
result4 = t16
PRINT result4