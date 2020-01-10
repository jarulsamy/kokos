import os
import sys
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="main script manager")
	parser.add_argument("command", help="Run cpu_stress_test.py", type=str, nargs="+")
	parser.add_argument("-t", type=int, default=None, required=False)
	parser.add_argument("-mt", type=int, default=None, required=False)
	args = parser.parse_args()
	command = args.command[0]
	t = args.t
	mt = args.mt
	if command == "cst":
		sys.path.insert(1, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kokos"))
		import cpu_stress_test
		print(cpu_stress_test.Start(t, mt))
	else:
		print("Command \"%s\" does not exist" % command)
