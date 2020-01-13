from kokos.src.cpu_stress_test import Start
from kokos.src import fof

class ActionNotExist(Exception):
	pass

class ArgumentRequired(Exception):
	pass

class CannotLoadObject(Exception):
	pass

class DirectoryNotExist(Exception):
	pass

class PermissionDenied(Exception):
	pass

class CannotPickleObject(Exception):
	pass

class CannotUnpickleObject(Exception):
	pass

class CannotZipObject(Exception):
	pass

def cpu_stress_test(TIME=None, THREADS=None):
	return Start(TIME, THREADS)

def FOF(**kwargs):
	return fof.FOF(**kwargs)
