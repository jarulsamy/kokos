from datetime import datetime
import win32security
from threading import Thread
from pywintypes import error as win32error
import hashlib
import shutil
import os

class Folder:

	def __init__(self, **kwargs):
		self.required = ["dir", "folders", "files"]
		self.optional = {"multithreading": True, "calculate_hash": True, "hash_formula": ["dir", "name", "size", "owner"], "adding_action": "r", "max_depth": 3}
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
		for required in self.required:
			if not hasattr(self, required):
				raise ArgumentRequired("\nArgument \"%s\" is required" % required)
		self.name = os.path.basename(self.dir)
		if self.multithreading:
			Thread(target=self.CalculateSize).start()
		else:
			self.CalculateSize()
		self.created = datetime.fromtimestamp(os.path.getctime(self.dir))
		self.modified = datetime.fromtimestamp(os.path.getmtime(self.dir))
		self.accessed = datetime.fromtimestamp(os.path.getatime(self.dir))
		try:
			self.owner, self.pc_name, self.pc_number = win32security.LookupAccountSid(None, win32security.GetFileSecurity(self.dir, win32security.OWNER_SECURITY_INFORMATION).GetSecurityDescriptorOwner())
		except win32error:
			self.owner = None
		self.permissions = int(oct(os.stat(self.dir).st_mode)[-3:])
		if self.calculate_hash:
			self.CalculateHash()
			return
		self.hash = None

	def CreateFileStructure(self, depth=0):
		self.structure = "├%s%s" % ("".join("──" for i in range(depth)), self.name)
		self.depth = depth + 1
		if self.folders != [] or self.files != []:
			self.structure += "\n"
		for folder in self.folders:
			self.structure += folder.CreateFileStructure(self.depth)
			if self.folders.index(folder) != self.folders.index(self.folders[-1]) or self.files != []:
				self.structure += "\n"
		for file in self.files:
			self.structure += "├%s%s" % ("".join("──" for i in range(self.depth)), file.name)
			if self.files.index(file) != self.files.index(self.files[-1]):
				self.structure += "\n"
		return self.structure

	# request from the other objects to re-create hashes based on the "hash_formula"
	# from this obecjt and return them to it without overwriting their own hash.
	# the reason I want to make them return their hash without updating it, is becase
	# this object can have differend "hash_formula" from the others. So if I want
	# to make a hash based on hash_formula without changing the hash from the other
	# obejcts, I have to do it this way. also find out how I will pass the "hash_formula"
	# and "overwrite" without storing them as object-variables or breaking something.
	def CalculateHash(self, hash_formula=None, overwrite=True):
		if hash_formula == None:
			hash_formula = self.hash_formula
		self.hash_data = b""
		for var in self.hash_formula:
			self.hash_data += str(getattr(self, var)).encode()




		for folder in self.folders:
			if not hasattr(folder, "hash"):
				folder.CalculateHash(hash_formula=hash_formula, overwrite=overwrite)
			self.hash_data += folder.hash.encode()







		# based on the hash of this fof
		for file in self.files:
			self.hash_data.join(str(data).encode() for data in [getattr(file, var) for var in hash_formula])



		if overwrite:
			self.hash = hashlib.sha224(self.hash_data).hexdigest()
			return self.hash
		return hashlib.sha224(self.hash_data).hexdigest()

	def CalculateSize(self):
		# self.size = 0
		# for path, folders, files in os.walk(self.dir):
		# 	for file in files:
		# 		self.size += os.path.getsize(os.path.join(path, file))


		self.size = 0
		for folder in self.folders:
			self.size += folder.size

		for file in self.files:
			self.size += file.size

		return self.size

	def Delete(self, ignore_errors=True):
		try:
			shutil.rmtree(self.dir)
			return True
		except PermissionError:
			if not ignore_errors:
				raise PermissionDenied("\nCannot delete \"%s\" folder" % self.name)
		except FileNotFoundError:
			if not ignore_errors:
				raise nDirectoryNotExist("\nDirectory \"%s\" does not exist" % self.name)
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

	def __eq__(self, other):
		if self.hash == None:
			self.CalculateHash()
		if other.hash == None:
			other.CalculateHash()
		return self.hash == other.hash

	def __repr__(self):
		return self.name

	def __getitem__(self, key):
		for folder in self.folders:
			if folder.name == key:
				return folder
		for file in self.files:
			if file.name == key:
				return file

	def __missing__(self, key):
		return None

	def __len__(self):
		return len(self.folders + self.files)

	def __str__(self):
		return self.__repr__()

	def __bool__(self):
		return self.folders != [] and self.files != []
