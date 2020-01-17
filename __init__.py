from src import cpu_stress_test
from src import file
from src import folder

def cpu_stress_test(TIME=None, THREADS=None):
	return cpu_stress_test.Start(TIME, THREADS)

def Folder(**kwargs):
	return folder.Folder(**kwargs)
