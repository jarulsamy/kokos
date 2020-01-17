import win32security
from pywintypes import error as win32error
import hashlib
from threading import Thread
from datetime import datetime
from copy import copy
import pickle
import zipfile
import os
try:
	from file import File
except ModuleNotFoundError:
	from src.file import File

# Arguments
# ------------------------------------------------------------------------------
class ArgumentRequired(Exception):
	pass

class ArgumentNotExist(Exception):
	pass

class WrongArgumentType(Exception):
	pass
# ------------------------------------------------------------------------------

# Does not exist
# ------------------------------------------------------------------------------
class DirectoryNotExist(Exception):
	pass

class AttributeNotExist(Exception):
	pass

class ActionDoesNotExist(Exception):
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
		return self.folders, self.files

	def SetArguments(self, **kwargs):

		# Set default arguments (where None is required)
		self.arguments = {
			"dir": [None, [str]],
			"hash_formula": [["dir", "name", "ext", "size", "content", "owner"], [list, str]],
			"adding_action": ["s", [str]],
			"loading_action": ["w", [str]],
			"max_file_size": [10000, [int]],
			"max_depth": [3, [int]],
			"overwrite": [False, [bool]],
		}

		# Overwrite all arguments to default
		if "overwrite" in kwargs and kwargs["overwrite"]:
			for key, value in self.arguments.items():
				setattr(self, key, value[0])

		# Check if all required arguments are passed
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

				# Check if "loading_action" is valid
				if key == "loading_action":
					value = value.lower()
					if value not in ["w", "r"]:
						raise ArgumentNotExist("\nArgument \"%s\" for \"%s\" is not valid" % (value, key))

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
		self.hash_data = b""
		for var in self.hash_formula:
			try:
				self.hash_data += str(getattr(self, var)).encode()
			except AttributeError:
				pass
		for folder in self.folders:
			if not hasattr(folder, "hash"):
				folder.CalculateHash(hash_formula=self.hash_formula, overwrite=False)
			self.hash_data += folder.hash.encode()
		for file in self.files:
			self.hash_data.join(str(data).encode() for data in [getattr(file, var) for var in self.hash_formula])
		self.hash = hashlib.sha224(self.hash_data).hexdigest()
		return self.hash

	def CalculateSize(self):
		self.size = 0
		for folder in self.folders:
			self.size += folder.size
			for file in self.files:
				self.size += file.size
				return self.size

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
		if not loading_action in ["w", "r"]:
			raise ActionNotExist("\nLoading action \"%s\" does not exist" % loading_action)
		try:
			if uncompress:
				with zipfile.ZipFile(os.path.join(os.path.dirname(path), "%s.zip" % os.path.splitext(os.path.basename(path))[0]), "r") as f:
					f.extract(os.path.basename(path))
			with open(path, "rb") as f:
				if loading_action == "w":
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
		self.structure = "├%s%s" % ("".join("──" for i in range(depth)), self.name)
		self.depth = depth + 1
		if self.folders != [] or self.files != []:
			self.structure += "\n"
		for folder in self.folders:
			self.structure += folder.CreateStructure(self.depth)
			if self.folders.index(folder) != self.folders.index(self.folders[-1]) or self.files != []:
				self.structure += "\n"
		for file in self.files:
			self.structure += "├%s%s" % ("".join("──" for i in range(self.depth)), file.name)
			if self.files.index(file) != self.files.index(self.files[-1]):
				self.structure += "\n"
		return self.structure

	# Virtual delete
	# def Delete(self):
	# 	self.__del__()

	# Actual delete
	def Delete(self, ignore_errors=True):
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

	def Rename(self, new_name, ignore_errors=True):
		try:
			shutil.move(self.dir, os.path.join(os.path.dirname(self.dir), new_name))
			self.dir = os.path.join(os.path.dirname(self.dir), new_name)
			return True
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot rename \"%s\" folder" % self.name)
		except FileNotFoundError:
			if not ignore_errors:
				raise DirectoryNotExist("\nDirectory \"%s\" does not exist" % self.name)
		return False

	def Move(self, new_path, ignore_errors=True):
		try:
			shutil.move(self.dir, new_name)
			self.dir = new_name
			return True
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot move \"%s\" folder" % self.name)
		except FileNotFoundError:
			if not ignore_errors:
				raise DirectoryNotExist("\nDirectory \"%s\" does not exist" % self.name)
		return False

	# Apply virtual changes
	def Apply(self):
		pass

	def PrayToGod(self):
		raise ERROR404("\nLogic Not Found...")

	def __eq__(self, other):
		if self.hash == None:
			self.CalculateHash()
		if other.hash == None:
			other.CalculateHash()
		return self.hash == other.hash

	def __ne__(self, other):
		return self.hash != other.hash

	def __contains__(self, other):
		if isinstance(other, list):
			for element in other:
				if isinstance(element, Folder):
					return element in other.folders
				elif isinstance(element, File):
					return element in self.files
				elif isinstance(element, FOF):
					return other in self.folders + self.files
		elif isinstance(other, Folder):
			return other in self.folders
		elif isinstance(other, File):
			return other in self.files
		elif isinstance(other, fof.FOF):
			return other in self.folders + self.files
		raise InstanceNotSupported("\nInstance \"%s\" is not supported for \"%s\" operation" % (type(other).__name__, "in"))

	def __add__(self, other):
		pass

	def __sub__(self, other):
		pass

	def __iadd__(self, other):
		pass

	def __isub__(self, other):
		pass

	def __getitem__(self, key):
		for folder in self.folders:
			if folder.name == key:
				return folder
		for file in self.files:
			if file.name == key:
				return file

	def __missing__(self, key):
		return

	def __len__(self):
		return len(self.folders + self.files)

	def __bool__(self):
		return self.folders != [] and self.files != []

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.__repr__()
