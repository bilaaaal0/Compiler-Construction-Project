MAIN:
ALLOC sum int
ALLOC product int
sum = 0
product = 1
i = 1
L0:
t0 = i <= 10
IF_FALSE t0 GOTO L1
t1 = sum + i
sum = t1
t2 = i + 1
i = t2
GOTO L0
L1:
PRINT sum
j = 1
L2:
t3 = j <= 5
IF_FALSE t3 GOTO L3
t4 = product * j
product = t4
t5 = j + 1
j = t5
GOTO L2
L3:
PRINT product
END_MAIN