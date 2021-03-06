from copy import copy
import os
try:
	from .fof_management import AttributeNotExist
except ImportError:
	pass

# Used for passing dicts with attributes
def PassArguments(self, *args):
	arguments = {}
	for argument in args:
		if hasattr(self, argument):
			arguments[argument] = getattr(self, argument)
			continue
		raise AttributeNotExist("\nAttribute \"%s\" does not exist" % argument)
	return arguments

# Adds elements and returns a new list without modifying the old one
def Add(old_list, *args):
	new_list = copy(old_list)
	for arg in args:
		if arg not in new_list:
			new_list.append(arg)
	return new_list

# Removes elements and returns a new list without modifying the old one
def Remove(old_list, *args):
	new_list = copy(old_list)
	for arg in args:
		if arg in new_list:
			new_list.remove(arg)
	return new_list

# Returns a new directory X times back from the given
def DirBack(old_dir, times):
	new_dir = copy(old_dir)
	for _ in range(times):
		new_dir = os.path.split(new_dir)[0]
	return os.path.realpath(new_dir)
