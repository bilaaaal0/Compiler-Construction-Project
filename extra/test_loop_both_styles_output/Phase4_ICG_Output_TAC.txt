MAIN:
ALLOC sum1 int
ALLOC sum2 int
sum1 = 0
sum2 = 0
i = 1
L0:
t0 = i <= 10
IF_FALSE t0 GOTO L1
t1 = sum1 + i
sum1 = t1
t2 = i + 1
i = t2
GOTO L0
L1:
PRINT sum1
ALLOC j int
j = 5
L2:
t3 = j <= 15
IF_FALSE t3 GOTO L3
t4 = sum2 + j
sum2 = t4
t5 = j + 1
j = t5
GOTO L2
L3:
PRINT sum2
ALLOC k int
k = 0
L4:
t6 = k <= 20
IF_FALSE t6 GOTO L5
PRINT k
t7 = k + 2
k = t7
GOTO L4
L5:
END_MAIN