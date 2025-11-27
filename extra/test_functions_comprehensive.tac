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
FUNC_factorial:
PARAM n 0
t2 = n <= 1
IF_FALSE t2 GOTO L0
RETURN 1
GOTO L0
L0:
ALLOC prev int
t3 = n - 1
prev = t3
ALLOC prevFact int
PUSH prev
CALL FUNC_factorial 1
t4 = RETVAL
prevFact = t4
t5 = n * prevFact
RETURN t5
RETURN 0
END_FUNC_factorial
FUNC_power:
PARAM base 0
PARAM exp 1
t6 = exp == 0
IF_FALSE t6 GOTO L1
RETURN 1
GOTO L1
L1:
ALLOC newExp int
t7 = exp - 1
newExp = t7
PUSH newExp
PUSH base
CALL FUNC_power 2
t8 = RETVAL
t9 = base * t8
RETURN t9
RETURN 0
END_FUNC_power
FUNC_calculate:
PARAM a 0
PARAM b 1
ALLOC sum int
ALLOC product int
PUSH b
PUSH a
CALL FUNC_add 2
t10 = RETVAL
sum = t10
PUSH b
PUSH a
CALL FUNC_multiply 2
t11 = RETVAL
product = t11
PUSH product
PUSH sum
CALL FUNC_add 2
t12 = RETVAL
RETURN t12
RETURN 0
END_FUNC_calculate
MAIN:
ALLOC result1 int
ALLOC result2 int
ALLOC result3 int
ALLOC result4 int
PUSH 5
PUSH 10
CALL FUNC_add 2
t13 = RETVAL
result1 = t13
PRINT result1
PUSH 5
CALL FUNC_factorial 1
t14 = RETVAL
result2 = t14
PRINT result2
PUSH 4
PUSH 2
CALL FUNC_power 2
t15 = RETVAL
result3 = t15
PRINT result3
PUSH 4
PUSH 3
CALL FUNC_calculate 2
t16 = RETVAL
result4 = t16
PRINT result4
END_MAIN