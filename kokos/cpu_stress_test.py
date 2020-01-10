from threading import Thread
import argparse
from time import time, strftime, gmtime
import bcrypt
import sys

def Load():
	global times_looping
	while not start:
		if stop:
			return
	while True:
		if stop:
			return
		bcrypt.hashpw(b"1234567890qwertyuiopasdfghjklzxcvbnm", bcrypt.gensalt())
		times_looping += 1

def Start(TIME=None, THREADS=None, RETURN=False):
	TIME_DEFAULT = 300
	THREADS_DEFAULT = 20
	if __name__ == "__main__":
		parser = argparse.ArgumentParser(description="CPU Stress Test")
		parser.add_argument("-t", help="How much time the stress test will last (in seconds)", type=int, default=TIME_DEFAULT, required=False)
		parser.add_argument("-mt", help="The number of process the program will use", type=int, default=THREADS_DEFAULT, required=False)
		args = parser.parse_args()
		RETURN = True
		if TIME == None:
			RETURN = False
			TIME = args.t
		if THREADS == None:
			RETURN = False
			THREADS = args.mt
	else:
		if TIME == None:
			TIME = TIME_DEFAULT
		if THREADS == None:
			THREADS = THREADS_DEFAULT
	global start
	global stop
	global times_looping
	global score
	start = False
	stop = False
	times_looping = 0
	started_processes = 0
	try:
		for _ in range(THREADS):
			Thread(target=Load).start()
			started_processes += 1
			if not RETURN:
				sys.stdout.write("\r%s threads have started..." % started_processes)
		global st
		global old_time
		old_time = None
		if not RETURN:
			print("\nStarting stress test...")
		st = time()
		start = True
		# Print and update the remaining stress time
		while True:
			if not RETURN:
				remaining_time = (st + TIME) - time()
				# Change the time format based on how much time remains
				if remaining_time < 60:
					format = "%S"
				elif remaining_time < 3600:
					format = "%M:%S"
				else:
					format = "%H:%M:%S"
				new_time = strftime(format, gmtime(st + TIME - time()))
				if old_time == None:
					old_time = new_time
				sys.stdout.write("\rTime remaining: %s%s" % (new_time, " " * (len(old_time) - len(new_time))))
				old_time = new_time
			if st + TIME < time():
				break
		stop = True
		score = int(times_looping / TIME)
	# If CTRL-C is pressed before the stress test finishes, calculate the score
	# based on the performance up to this point.
	except KeyboardInterrupt:
		stop = True
		if start:
			score = int(times_looping / (time() - st))
		else:
			score = 0
	if RETURN:
		return score
	return "\nScore: %s" % score

if __name__ == "__main__":
	print(Start())
