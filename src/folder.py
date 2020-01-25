import win32security
from pywintypes import error as win32error
import hashlib
from threading import Thread
from datetime import datetime
from copy import copy
import pickle
import zipfile
import inspect
import os
try:
	from file import File
except (ModuleNotFoundError, ImportError):
	pass

# Arguments
# ------------------------------------------------------------------------------
class ArgumentRequired(Exception):
	pass

class ArgumentNotExist(Exception):
	pass

class WrongArgumentType(Exception):
	pass
# ------------------------------------------------------------------------------

# Not exist
# ------------------------------------------------------------------------------
class DirectoryNotExist(Exception):
	pass

class AttributeNotExist(Exception):
	pass

class ActionNotExist(Exception):
	pass

class FileNotExist(Exception):
	pass
# ------------------------------------------------------------------------------

# Pickle
# ------------------------------------------------------------------------------
class CannotPickleObject(Exception):
	pass

class CannotUnpickleObject(Exception):
	pass
# ------------------------------------------------------------------------------

# Other
# ------------------------------------------------------------------------------
class PermissionDenied(Exception):
	pass

class InstanceNotSupported(Exception):
	pass

class WrongArgument(Exception):
	pass

class CannotZipObject(Exception):
	pass

class ERROR404(Exception):
	pass

class CannotInitializeDirectory(Exception):
	pass

class CannotTrackChanges(Exception):
	pass
# ------------------------------------------------------------------------------

class Folder:

	def __init__(self, **kwargs):

		# Set arguments
		kwargs["overwrite"] = True
		self.SetArguments(**kwargs)

		# Other
		self.GetFOF()

	def GetFOF(self):
		self.folders = []
		self.files = []

		# Main loop
		for fof in os.listdir(self.dir):
			try:
				if os.path.isdir(os.path.join(self.dir, fof)):
					Thread(target=self.folders.append(Folder(dir=os.path.join(self.dir, fof), **self.PassArguments("hash_formula", "adding_action", "max_file_size", "max_depth"))))
				elif os.path.isfile(os.path.join(self.dir, fof)):
					self.files.append(File(dir=os.path.join(self.dir, fof), **self.PassArguments("hash_formula", "adding_action", "max_file_size", "max_depth")))
			# OSError (SError: [Errno 22] Invalid argument) is being raised when
			# a 0-byte executable is trying to be accessed (if you using Windows
			# check %HOMEPATH%\AppData\Local\Microsoft\WindowsApps).
			except (PermissionError, OSError):
				pass

		# Other
		self.name = os.path.basename(self.dir)
		self.created = datetime.fromtimestamp(os.path.getctime(self.dir))
		self.modified = datetime.fromtimestamp(os.path.getmtime(self.dir))
		self.accessed = datetime.fromtimestamp(os.path.getatime(self.dir))
		try:
			self.owner, self.pc_name, self.pc_number = win32security.LookupAccountSid(None, win32security.GetFileSecurity(self.dir, win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner())
		except win32error:
			self.owner, self.pc_name, self.pc_number = None, None, None
		self.permissions = int(oct(os.stat(self.dir).st_mode)[-3:])
		self.CalculateHash()
		self.CalculateSize()
		self.GetFOFNum()
		return self.folders, self.files

	def SetArguments(self, **kwargs):

		# Set default arguments (where None is required)
		self.arguments = {
			"dir": [None, [str]],
			"hash_formula": [["dir", "name", "ext", "size", "content", "owner"], [list, str]],
			"adding_action": ["s", [str]],
			"loading_action": ["w", [str]],
			"max_file_size": [1000000, [int]],
			"max_depth": [3, [int]],
			"overwrite": [False, [bool]],
			"required": [True, [bool]],
		}

		# Overwrite all arguments to default
		if "overwrite" in kwargs and kwargs["overwrite"]:
			for key, value in self.arguments.items():
				setattr(self, key, value[0])

		# Check if all required arguments are passed
		try:
			if kwargs["required"]:
				raise KeyError
		except KeyError:
			for key, value in self.arguments.items():
				if value[0] == None and key not in kwargs:
					raise ArgumentRequired("\nArgument \"%s\" is required" % key)

		# Set any passed arguments
		for key, value in kwargs.items():
			if key not in self.arguments:
				raise ArgumentNotExist("\nArgument \"%s\" does not exist" % (key))
			if isinstance(value, tuple(self.arguments[key][1])):

				# If an argument can be string or list and its not list, make it list
				if list in self.arguments[key][1] and not isinstance(key, list):
					value = list(value)

				# Check if directory is valid
				if key == "dir":
					try:
						if not os.path.isdir(value):
							raise DirectoryNotExist("\nDirectory \"%s\" does not exist" % value)
					except TypeError:
						raise DirectoryNotExist("\nDirectory can't be blank")

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
						]:
							raise WrongArgument("\nArgument element \"%s\" for \"%s\" is incorrect" % (data, value))

				# Make adding_action lowercase
				if key == "adding_action":
					value = value.lower()
					if value not in ["w", "a", "s"]:
						raise ActionNotExist("\nAdding action \"%s\" does not exist" % value)

				# Check if "loading_action" is valid
				if key == "loading_action":
					value = value.lower()
					if value not in ["w", "r"]:
						raise ActionNotExist("\nLoading action \"%s\" does not exist" % loading_action)

				if key == "action_type":
					value = value.lower()
					if value not in ["virtual", "actual"]:
						raise ActionNotExist("\\nAction type \"%s\" for \"%s\" is incorrect" % (value, "action_type"))

				# Set attribute
				setattr(self, key, value)
				continue
			raise WrongArgumentType("\nArgument type \"%s\" for \"%s\" is incorrect" % (type(value), value))

	def PassArguments(self, *args):
		arguments = {}
		for argument in args:
			if hasattr(self, argument):
				arguments[argument] = getattr(self, argument)
				continue
			raise AttributeNotExist("\nAttribute \"%s\" does not exist" % argument)
		return arguments

	def CalculateHash(self):
		self.hash_data = ""
		for var in self.hash_formula:
			try:
				self.hash_data += str(getattr(self, var))
			except AttributeError:
				pass
		for folder in self.folders:
			self.hash_data += folder.hash
		for file in self.files:
			self.hash_data += file.hash
		self.hash = hashlib.sha224(self.hash_data.encode()).hexdigest()
		return self.hash

	# return in bytes
	def CalculateSize(self):
		self.size = 0
		for folder in self.folders:
			self.size += folder.size
		for file in self.files:
			self.size += file.size
		return self.size

	def GetFOFNum(self):
		self.FOLDERS_NUM = 0
		self.FILES_NUM = 0
		for folder in self.folders:
			self.FOLDERS_NUM += 1
			fof = folder.GetFOFNum()
			self.FOLDERS_NUM += fof[0]
			self.FILES_NUM += fof[1]
		for file in self.files:
			self.FILES_NUM += 1
		return self.FOLDERS_NUM, self.FILES_NUM

	def Save(self, path="data.pickle", compress=True, ignore_errors=False):
		try:
			with open(path, "wb") as f:
				pickle.dump(self, f)
			if compress:
				with zipfile.ZipFile(os.path.join(os.path.dirname(path), "%s.zip" % os.path.splitext(os.path.basename(path))[0]), "w", compression=zipfile.ZIP_DEFLATED) as f:
					f.write(path, os.path.basename(path))
				File(dir=path).Delete(ignore_errors=ignore_errors)
			return True
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot write to \"%s\" file" % os.path.basename(path))
		except pickle.PickleError:
			if not ignore_errors:
				raise CannotPickleObject("\nCannot pickle \"%s\" object" % __name__)
		except (zipfile.BadZipFile, zipfile.LargeZipFile):
			if not ignore_errors:
				raise CannotZipObject("\nSomething went wrong, cannot Zip \"%s\" object" % __name__)
		if compress:
			File(dir=path).Delete(ignore_errors=ignore_errors)
		return False

	# w = Overwrite
	# r = Return
	def Load(self, path="data.pickle", loading_action="w", uncompress=True, ignore_errors=False):
		self.SetArguments(required=False, loading_action=loading_action)
		try:
			if uncompress:
				with zipfile.ZipFile(os.path.join(os.path.dirname(path), "%s.zip" % os.path.splitext(os.path.basename(path))[0]), "r") as f:
					f.extract(os.path.basename(path), os.path.dirname(path))
			with open(path, "rb") as f:
				if self.loading_action == "w":
					obj = pickle.load(f)
					for var in self.__dict__:
						setattr(self, var, getattr(obj, var))
					return
				if uncompress:
					File(dir=path).Delete(ignore_errors=ignore_errors)
				return pickle.load(f)
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot read from \"%s\" file" % os.path.basename(path))
		except FileNotFoundError:
			if not ignore_errors:
				raise FileNotExist("\nFile \"%s\" does not exist" % os.path.basename(path))
		except pickle.UnpicklingError:
			if not ignore_errors:
				raise CannotUnpickleObject("\nCannot unpickle \"%s\" object" % __name__)
		if uncompress:
			File(dir=os.path.join(os.path.dirname(path), "%s.zip" % os.path.splitext(os.path.basename(path))[0])).Delete(ignore_errors=ignore_errors)
		return False

	def CreateStructure(self, depth=0):
		self.structure = "%s/" % self.name
		self.depth = depth + 1
		if self.folders != [] or self.files != []:
			self.structure += "\n"
		for folder in self.folders:
			for line in folder.CreateStructure(self.depth).split("\n"):
				self.structure += "%s%s\n" % ("│   ", line)
		for file in self.files:
			self.structure += "%s── %s " % ("├" if self.files.index(file) != self.files.index(self.files[-1]) else "└", file.name)
			if self.files.index(file) != self.files.index(self.files[-1]):
				self.structure += "\n"
		return self.structure

	def Delete(self, ignore_errors=False, action_type="virtual"):
		self.SetArguments(required=False, action_type=action_type)
		if self.action_type == "virtual":
			self.__del__()
		else:
			try:
				shutil.rmtree(self.dir)
				return True
			except PermissionError:
				if not ignore_errors:
					raise PermissionDenied("\nCannot delete \"%s\" folder" % self.name)
			except FileNotFoundError:
				if not ignore_errors:
					raise DirectoryNotExist("\nDirectory \"%s\" does not exist" % self.name)
			return False

	def Rename(self, new_name, ignore_errors=False, action_type="virtual"):
		self.SetArguments(required=False, action_type=action_type)
		if self.action_type == "virtual":
			self.name = new_name
			self.dir = os.path.join(os.path.dirname(self.dir), self.name)
			self.modified = datetime.fromtimestamp(os.path.getmtime(self.dir))
			self.CalculateHash()
		else:
			try:
				shutil.move(self.dir, os.path.join(os.path.dirname(self.dir), new_name))
				self.dir = os.path.join(os.path.dirname(self.dir), new_name)
				self.CalculateHash()
				return True
			except PermissionError:
				if not ignore_errors:
					raise PermissionDenied("\nCannot rename \"%s\" folder" % self.name)
			except FileNotFoundError:
				if not ignore_errors:
					raise DirectoryNotExist("\nDirectory \"%s\" does not exist" % self.name)
			return False

	def Move(self, new_path, ignore_errors=True, action_type="virtual"):
		self.SetArguments(required=False, action_type=action_type)
		if self.action_type == "virtual":
			self.dir = os.path.join(new_path, self.name)
			self.modified = datetime.fromtimestamp(os.path.getmtime(self.dir))
			self.CalculateHash()
		else:
			try:
				shutil.move(self.dir, new_name)
				self.dir = new_name
				self.CalculateHash()
				return True
			except PermissionError:
				if not ignore_errors:
					raise PermissionDenied("\nCannot move \"%s\" folder" % self.name)
			except FileNotFoundError:
				if not ignore_errors:
					raise DirectoryNotExist("\nDirectory \"%s\" does not exist" % self.name)
			return False

	def PrayToGod(self):
		raise ERROR404("\n\nInstance \"God\" does not exist...\nDid you mean \"Dog\"?")

	def IsInitialized(self):
		if ".kokos" in os.listdir(os.getcwd()):
			return False
		return True

	def init(self, overwrite=False):
		if overwrite or not self.IsInitialized():
			self.kokognore = [".kokos"]
			if ".kokognore" in os.listdir(os.getcwd()):
				try:
					with open(os.path.join(os.getcwd(), ".kokognore"), "r") as f:
						for fof in f.read():
							if fof != "":
								self.kokognore.append(fof)
				except PermissionError:
					raise PermissionDenied("\nCannot read from \"%s\" file" % ".kokognore")
			self.Save(os.path.join(os.getcwd(), ".kokos"), compress=False)
			return
		raise CannotInitializeDirectory("\nDirectory cannot be initialized because a \"%s\" file already exists in it" % default_name)

	def CheckInstanceValidation(self, other):
		if not isinstance(other, (Folder, File)):
			raise InstanceNotSupported("\nInstance \"%s\" is not supported for \"%s\" operation" % (type(other).__name__, inspect.stack()[1][3]))

	# ==
	def __eq__(self, other):
		self.CheckInstanceValidation(other)
		return self.hash == other.hash

	# !=
	def __ne__(self, other):
		self.CheckInstanceValidation(other)
		return self.hash != other.hash

	# in
	def __contains__(self, other):
		self.CheckInstanceValidation(other)
		if isinstance(other, Folder):
			return other in self.folders
		elif isinstance(other, File):
			return other in self.files

	# +
	def __add__(self, other):
		self.CheckInstanceValidation(other)
		obj = copy(self)
		obj.folders += other.folders
		obj.files += other.files
		return obj

	# -
	def __sub__(self, other):
		self.CheckInstanceValidation(other)
		obj = copy(self)
		for folder in other.folders:
			for f in obj.folders:
				if folder.name == f.name:
					obj.folders.remove(f)
		for file in other.files:
			for f in obj.files:
				if file.name == f.name:
					obj.files.remove(f)
		return obj

	# +=
	def __iadd__(self, other):
		self.CheckInstanceValidation(other)
		self.folders += other.folders
		self.files += other.files
		return self

	# -=
	def __isub__(self, other):
		self.CheckInstanceValidation(other)
		for folder in other.folders:
			for f in self.folders:
				if folder.name == f.name:
					self.folders.remove(f)
		for file in other.files:
			for f in self.files:
				if file.name == f.name:
					self.files.remove(f)
		return self

	# []
	def __getitem__(self, key):
		for folder in self.folders:
			if folder.name == key:
				return folder
		for file in self.files:
			if file.name == key:
				return file

	def __missing__(self, key):
		return

	# len()
	def __len__(self):
		return len(self.folders + self.files)

	# bool()
	def __bool__(self):
		return self.folders != [] and self.files != []

	# for fof in folder_object:
	#	...
	def __iter__(self):
		return iter(self.folders + self.files)

	def __repr__(self):
		return self.name

	# str()
	def __str__(self):
		return self.__repr__()
