from datetime import datetime
import win32security
from pywintypes import error as win32error
import hashlib
import shutil
import os

class File:

	# See why_only_named_arguments.md
	def __init__(self, **kwargs):
		self.required = ["dir"]
		self.optional = {"calculate_hash": False, "hash_formula": ["dir", "name", "ext", "size", "content", "owner"], "max_file_size": 10000}
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
		self.ext = os.path.splitext(self.name)[1]
		self.size = os.stat(self.dir).st_size
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
		if self.calculate_hash:
			self.CalculateHash()
			return
		self.hash = None

	def CalculateHash(self):
		self.hash = hashlib.sha224(b"".join(str(data).encode() for data in [getattr(self, var) for var in self.hash_formula])).hexdigest()
		return self.hash

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

	# Compare 2 files to see if are equal based on their hashes
	def __eq__(self, other):
		if self.hash == None:
			self.CalculateHash()
		if other.hash == None:
			other.CalculateHash()
		return self.hash == other.hash

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.__repr__()

	def __bool__(self):
		return os.path.exists(self.dir)
