from interpreter import TACInterpreter

class VerboseInterpreter(TACInterpreter):
    def execute_instruction(self, instruction):
        print(f"PC={self.pc}: {instruction}")
        result = super().execute_instruction(instruction)
        print(f"  All Vars: {self.variables}")
        return result

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

interp = VerboseInterpreter()
interp.max_iterations = 20

print("Starting execution...\n")
interp.execute(tac_code)

print(f"\nFinal: sum={interp.variables.get('sum')}, i={interp.variables.get('i')}")
