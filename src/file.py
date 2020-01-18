from datetime import datetime
import win32security
from pywintypes import error as win32error
import hashlib
import shutil
from copy import copy
import os
import folder

# Arguments
# ------------------------------------------------------------------------------
class ArgumentNotExist(Exception):
	pass

class ArgumentRequired(Exception):
	pass

class WrongArgumentType(Exception):
	pass
# ------------------------------------------------------------------------------

# Other
# ------------------------------------------------------------------------------
class FileNotExist(Exception):
	pass

class PermissionDenied(Exception):
	pass
# ------------------------------------------------------------------------------

class File:

	def __init__(self, **kwargs):

		# Set arguments
		kwargs["overwrite"] = True
		self.SetArguments(**kwargs)

		# Other
		self.name = os.path.basename(self.dir)
		self.ext = os.path.splitext(self.name)[1]
		self.size = os.path.getsize(self.dir)
		if self.size < self.max_file_size:
			try:
				with open(self.dir, "r", errors="ignore") as f:
					self.content = f.read()
			except (PermissionError, UnicodeDecodeError):
				self.content = None
		else:
			self.content = None
		self.created = datetime.fromtimestamp(os.path.getctime(self.dir))
		self.modified = datetime.fromtimestamp(os.path.getmtime(self.dir))
		self.accessed = datetime.fromtimestamp(os.path.getatime(self.dir))
		try:
			self.owner, self.pc_name, self.pc_number = win32security.LookupAccountSid(None, win32security.GetFileSecurity(self.dir, win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner())
		except win32error:
			self.owner = None
		self.permissions = int(oct(os.stat(self.dir).st_mode)[-3:])
		self.CalculateHash()

	def SetArguments(self, **kwargs):

		# Set default arguments (where None is required)
		self.arguments = {
			"dir": [None, [str]],
			"hash_formula": [["dir", "name", "ext", "size", "content", "owner"], [list, str]],
			"adding_action": ["s", [str]],
			"max_file_size": [10000, [int]],
			"max_depth": [3, [int]],
			"overwrite": [False, [bool]],
		}

		# Check if all required arguments are passed
		for key, value in self.arguments.items():
			if value[0] == None and key not in kwargs:
				raise ArgumentRequired("\nArgument \"%s\" is required" % key)

		# overwrite all arguments to default
		if "overwrite" in kwargs and kwargs["overwrite"]:
			for argument in self.arguments:
				if self.arguments[argument][0] != None:
					setattr(self, argument, self.arguments[argument][0])

		# set any passed arguments
		for key, value in kwargs.items():
			if key not in self.arguments:
				raise ArgumentNotExist("\nArgument \"%s\" does not exist" % (key))
			if isinstance(value, tuple(self.arguments[key][1])):
				# checks

				# If an argument can be string or list and its not list, make it list
				if list in self.arguments[key][1] and not isinstance(key, list):
					value = list(value)

				# If directory is not valid
				if key == "dir":
					try:
						if not os.path.isfile(value):
							raise FileNotExist("\nFile \"%s\" does not exist" % value)
					except TypeError:
						raise FileNotExist("\nFile can't be blank")

				# Check if "hash_formula" elements are valid
				if key == "hash_formula":
					value = [data.lower() for data in value]
					value.sort()
					for data in copy(value):
						if data in ["ext", "content"]:
							value.remove(data)
							continue
						if not isinstance(data, str):
							raise WrongArgumentType("\nArgument element's type \"%s\" for \"%s\" in \"%s\" is incorrect" % (type(data), data, value))
						if data not in [
							"dir",
							"name",
							"created",
							"modified",
							"accessed",
							"owner",
							"pc_name",
							"pc_number",
							"permissions",
							"hash",
							"size",
							"ext",
							"content"
						]:
							raise WrongArgument("\nArgument element \"%s\" for \"%s\" is incorrect" % (data, value))

				# Make adding_action lowercase
				if key == "adding_action":
					value = value.lower()

				# Set attribute
				setattr(self, key, value)
				continue
			raise WrongArgumentType("\nArgument type \"%s\" for \"%s\" is incorrect" % (type(value), value))

	def CalculateHash(self):
		self.hash = hashlib.sha224(b"".join(str(data).encode() for data in [getattr(self, var) for var in self.hash_formula])).hexdigest()
		return self.hash

	# Virtual delete
	# def Delete(self):
	# 	self.__del__()

	# Actual delete
	def Delete(self, ignore_errors=True):
		try:
			os.remove(self.dir)
			return True
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot delete \"%s\" file" % self.name)
		except FileNotFoundError:
			if not ignore_errors:
				raise FileNotExist("\nFile \"%s\" does not exist" % self.name)
		return False

	def Rename(self, new_name, ignore_errors=True):
		try:
			shutil.move(self.dir, os.path.join(os.path.dirname(self.dir), new_name))
			self.dir = os.path.join(os.path.dirname(self.dir), new_name)
			return True
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot rename \"%s\" File" % self.name)
		except FileNotFoundError:
			if not ignore_errors:
				raise FileNotExist("\nFile \"%s\" does not exist" % self.name)
		return False

	def Move(self, new_path, ignore_errors=True):
		try:
			shutil.move(self.dir, new_path)
			self.dir = new_path
			return True
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot move \"%s\" File" % self.name)
		except FileNotFoundError:
			if not ignore_errors:
				raise FileNotExist("\nFile \"%s\" does not exist" % self.name)
		return False

	def CheckInstanceValidation(self, other):
		if not isinstance(other, (folder.Folder, File)):
			raise InstanceNotSupported("\nInstance \"%s\" is not supported for \"%s\" operation" % (type(other).__name__, inspect.stack()[1][3]))

	# ==
	def __eq__(self, other):
		self.CheckInstanceValidation(other)
		return self.hash == other.hash

	# !=
	def __ne__(self, other):
		self.CheckInstanceValidation(other)
		return self.hash != other.hash

	# bool()
	def __bool__(self):
		return os.path.isfile(self.dir)

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.__repr__()
