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
PUSH temp
CALL FUNC_factorial 1
t2 = RETVAL
t3 = n * t2
RETURN t3
RETURN 0
END_FUNC_factorial
FUNC_isEven:
PARAM x 0
ALLOC remainder int
t4 = x % 2
remainder = t4
t5 = remainder == 0
IF_FALSE t5 GOTO L1
RETURN 1
GOTO L1
L1:
RETURN 0
RETURN 0
END_FUNC_isEven
MAIN:
ALLOC sum int
ALLOC product int
ALLOC count int
sum = 0
product = 1
count = 0
i = 1
L2:
t6 = i <= 10
IF_FALSE t6 GOTO L3
t7 = sum + i
sum = t7
t8 = i + 1
i = t8
GOTO L2
L3:
PRINT sum
j = 0
L4:
t9 = j <= 20
IF_FALSE t9 GOTO L5
t10 = count + 1
count = t10
t11 = j + 2
j = t11
GOTO L4
L5:
PRINT count
ALLOC result int
PUSH 5
CALL FUNC_factorial 1
t12 = RETVAL
result = t12
PRINT result
x = 1
L6:
t13 = x <= 3
IF_FALSE t13 GOTO L7
y = 1
L8:
t14 = y <= 3
IF_FALSE t14 GOTO L9
ALLOC check int
t15 = x + y
PUSH t15
CALL FUNC_isEven 1
t16 = RETVAL
check = t16
t17 = check == 1
IF_FALSE t17 GOTO L10
PRINT 1
GOTO L11
L10:
PRINT 0
L11:
t18 = y + 1
y = t18
GOTO L8
L9:
t19 = x + 1
x = t19
GOTO L6
L7:
END_MAIN