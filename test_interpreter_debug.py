from interpreter import TACInterpreter

tac_code = """
MAIN:
ALLOC sum int
sum = 0
i = 1
L0:
t0 = i <= 5
IF_FALSE t0 GOTO L1
t1 = sum + i
sum = t1
t2 = i + 1
i = t2
GOTO L0
L1:
PRINT sum
END_MAIN
""".strip().split('\n')

interp = TACInterpreter()
interp.max_iterations = 20  # Limit for debugging

print("Starting execution...")
interp.execute(tac_code)

print("\nFinal variables:")
for var, val in interp.variables.items():
    print(f"  {var} = {val}")

print(f"\nIterations: {interp.iteration_count}")
print(f"Outputs: {interp.output}")
