from datetime import datetime
import win32security
from threading import Thread
from pywintypes import error as win32error
import hashlib
import pickle
import zipfile
import shutil
import os
import sys
from folder import Folder
from file import File
from utils import JoinDict

class ActionNotExist(Exception):
	pass

class ArgumentRequired(Exception):
	pass

class CannotLoadObject(Exception):
	pass

class DirectoryNotExist(Exception):
	pass

class FileNotExist(Exception):
	pass

class PermissionDenied(Exception):
	pass

class CannotPickleObject(Exception):
	pass

class CannotUnpickleObject(Exception):
	pass

class CannotZipObject(Exception):
	pass

class FOF:

	def __init__(self):
		self.folders = []
		self.files = []

	def GetFOF(self, **kwargs):
		self.required = ["dir"]
		self.optional = {"multithreading": True, "calculate_hash": True, "hash_formula": ["dir", "name", "ext", "size", "content", "owner"], "adding_action": "s", "max_file_size": 10000, "max_depth": 3}
		for optional in self.optional:
			setattr(self, optional, self.optional[optional])
		for key, value in kwargs.items():
			if key in list(self.optional) + self.required:
				if key == "hash_formula" and self.calculate_hash:
					setattr(self, key, sorted(set(list(value))))
				elif key == "adding_action":
					setattr(self, key, value.lower())
				else:
					setattr(self, key, value)
		# In case I add more required arguments in the future
		for required in self.required:
			if not hasattr(self, required):
				raise ArgumentRequired("\nArgument \"%s\" is required" % required)
		if not os.path.isdir(self.dir):
			raise DirectoryNotExist("\nDirectory \"%s\" does not exist" % self.dir)
		if self.adding_action not in ["w", "a", "s"]:
			raise ActionNotExist("\nAction \"%s\" does not exist" % self.adding_action)
		try:
			for f in os.listdir(self.dir):
				if os.path.isdir(os.path.join(self.dir, f)):
					if self.multithreading:
						Thread(target=self.folders.append(Folder(dir=os.path.join(self.dir, f), **dict(zip(["folders", "files"], FOF().GetFOF(**JoinDict(eval("{%s}" % "".join(str({required: os.path.join(getattr(self, required), f)})[1:-1].replace("\'", "\"") if required == "dir" else str({required: getattr(self, required)})[1:-1].replace("\'", "\"") for required in self.required)), self.optional))))))).start()
					else:
						self.folders.append(Folder(dir=os.path.join(self.dir, f), **dict(zip(["folders", "files"], FOF().GetFOF(**JoinDict(eval("{%s}" % "".join(os.path.join(str({required: os.path.join(getattr(self, required), f)})[1:-1].replace("\'", "\"") if required == "dir" else str({required: getattr(self, required)})[1:-1].replace("\'", "\"") for required in self.required)), self.optional)))))))
				elif os.path.isfile(os.path.join(self.dir, f)):
					self.files.append(File(dir=os.path.join(self.dir, f), **JoinDict(*[{optional: getattr(self, optional)} for optional in self.optional])))
		except PermissionError:
			pass
		return self.folders, self.files

	def Save(self, path="data.pickle", compress=True, ignore_errors=True):
		try:
			with open(path, "wb") as f:
				if compress:
						pickle.dump(self, f)
						with zipfile.ZipFile(os.path.join(os.path.dirname(path), "%s.zip" % os.path.splitext(os.path.basename(path))[0]), "w", compression=zipfile.ZIP_DEFLATED) as f:
							f.write(path, os.path.basename(path))
				else:
					pickle.dump(self, f)
				return True
		except PermissionError:
			if compress:
				File(dir=path).Delete()
			if not ignore_errors:
				raise PermissionDenied("\nCannot write to \"%s\" file" % os.path.basename(path))
		except pickle.PickleError:
			if compress:
				File(dir=path).Delete()
			if not ignore_errors:
				raise CannotPickleObject("\nCannot pickle \"%s\" object" % __name__)
		except (zipfile.BadZipFile, zipfile.LargeZipFile):
			if compress:
				File(dir=path).Delete()
			if not ignore_errors:
				raise CannotZipObject("\nSomething went wrong, cannot Zip \"%s\" object" % __name__)
			return False

	# w = overwrite
	# r = return
	def Load(self, path="data.pickle", loading_action="w", uncompress=True, ignore_errors=True):
		loading_action = loading_action.lower()
		try:
			with open(path, "rb") as f:
				if uncompress:
					if loading_action == "w":
						pass
					elif loading_action == "r":
						pass
					else:
						if not ignore_errors:
							raise ActionDoesNotExist("\nAction \"%s\" does not exist" % self.loading_action)
				else:
					if loading_action == "w":
						obj = pickle.load(f)
						for var in self.__dict__:
							setattr(self, var, getattr(obj, var))
						return
					elif loading_action == "r":
						return pickle.load(f)
					else:
						if not ignore_errors:
							raise ActionDoesNotExist("\nAction \"%s\" does not exist" % self.loading_action)
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot read from \"%s\" file" % os.path.basename(path))
		except FileNotFoundError:
			if not ignore_errors:
				raise FileNotExist("\nFile \"%s\" does not exist" % os.path.basename(path))
		except pickle.UnpicklingError:
			if not ignore_errors:
				raise CannotUnpickleObject("\nCannot unpickle \"%s\" object" % __name__)

	def CalculateHash(self):
		self.hash_data = b""
		for var in self.hash_formula:
			self.hash_data += str(getattr(self, var)).encode()
		for folder in self.folders:
			if not hasattr(folder, "hash"):
				folder.CalculateHash(hash_formula=self.hash_formula, overwrite=False)
			self.hash_data += folder.hash.encode()
		for file in self.files:
			self.hash_data.join(str(data).encode() for data in [getattr(file, var) for var in hash_formula])
		self.hash = hashlib.sha224(self.hash_data).hexdigest()
		return self.hash

	def Delete(self):
		self.__del__()

	def __eq__(self, other):
		if self.hash == None:
			self.CalculateHash()
		if other.hash == None:
			other.CalculateHash()
		return self.hash == other.hash

	def __repr__(self):
		return "\n".join(fof.name for fof in self.folders + self.files)

	def __getitem__(self, key):
		for folder in self.folders:
			if folder.name == key:
				return folder
		for file in self.files:
			if file.name == key:
				return file

	def __missing__(self, key):
		return None

	def __reversed__(self):
		return "\n".join(fof.name for fof in (self.folders + self.files)[::-1])

	def __len__(self):
		return len(self.folders + self.files)

	def __str__(self):
		return self.__repr__()

	def __bool__(self):
		return self.folders != [] and self.files != []

	# w = overwrite
	# a = append
	# s = skip
	def __add__(self, other):
		for folder in other.folders:
			if folder in self.folders:
				if self.adding_action == "w":
					for f in self.folders:
						if f.name == folder.name:
							self.folders[self.folders.index(f)] = folder
				elif self.adding_action == "a":
					self.folders.append(folder)
			else:
				self.folders.append(folder)
		for file in other.files:
			if file in self.files:
				if self.adding_action == "w":
					for f in self.files:
						if f.name == file.name:
							self.files[self.files.index(f)] = file
				elif self.adding_action == "a":
					self.folders.append(file)
			else:
				self.files.append(file)
		return self.__repr__()
