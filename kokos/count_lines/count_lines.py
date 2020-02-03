from ..fof_management import (
	Folder,
	File,
	ArgumentRequired,
	ArgumentNotExist,
	WrongArgumentType,
	AttributeNotExist,
	DirectoryNotExist,
)
from ..utils import PassArguments, Add
from copy import copy
import os

class GetLines:

	def __init__(self, **kwargs):

		# Set arguments
		kwargs["overwrite"] = True
		self.SetArguments(**kwargs)

		# Other
		self.GetLines()

	def GetLines(self):
		self.lines = 0
		if self.is_dir:
			f = Folder(**PassArguments(self, "dir", "max_file_size"))
			for folder in f.folders:
				if folder.name not in self.exclude_folders:
					self += GetLines(dir=folder.dir, **PassArguments(self, "exclude_ext", "exclude_files", "exclude_folders", "exclude_blank_lines", "exclude_comments", "comment_prefixes", "max_file_size"))
			for file in f.files:

				# exclude files:
				# 	with extention in exclude
				# 	larger than "max_file_size"
				if file.ext in self.exclude_ext or file.name in self.exclude_files or not file.content:
					continue

				# Set variables for each file type
				if not hasattr(self, file.ext[1:]) and file.ext[1:].strip():
					setattr(self, file.ext[1:], 0)

				for line in file.content.split("\n"):

					# If line is blank
					if self.exclude_blank_lines and not line.strip():
						continue

					# If line is comment
					if self.exclude_comments and file.ext in self.comment_prefixes:
						if line.strip().startswith(self.comment_prefixes[file.ext]):
							continue
					self.lines += 1

					# Increase variable file type dynamically (its bad but it works)
					if file.ext[1:].strip():
						setattr(self, file.ext[1:], getattr(self, file.ext[1:]) + 1)
		else:
			file = File(**PassArguments(self, "dir", "max_file_size"))

			# exclude file if:
			# 	has with extention in exclude
			# 	is larger than "max_file_size"
			if file.ext in self.exclude_ext or file.name in self.exclude_files or not file.content:
				return self.lines

			# Set file type variable
			if file.ext[1:].strip():
				setattr(self, file.ext[1:], 0)
			for line in file.content.split("\n"):

				# If line is blank
				if self.exclude_blank_lines and not line.strip():
					continue

				# If line is comment
				if self.exclude_comments and file.ext in self.comment_prefixes:
					if line.strip().startswith(self.comment_prefixes[file.ext]):
						continue
				self.lines += 1

				# Increase variable file type dynamically (its bad but it works)
				if file.ext[1:].strip():
					setattr(self, file.ext[1:], getattr(self, file.ext[1:]) + 1)
		return self.lines

	def SetArguments(self, **kwargs):

		# Set default arguments (where None is required)
		self.arguments = {
			"dir": [None, [str]],
			"exclude_ext": [[], [list, str]],
			"exclude_files": [[], [list, str]],
			"exclude_folders": [[], [list, str]],
			"exclude_blank_lines": [True, [bool]],
			"exclude_comments": [True, [bool]],
			"comment_prefixes": [{".py": "#"}, [dict]],
			"max_file_size": [50000, [int]],
			"overwrite": [False, [bool]],
			"NO_VARIABLES": [[
							"NO_VARIABLES",
							"arguments",
							"dir",
							"is_dir",
							"exclude_ext",
							"exclude_files",
							"exclude_folders",
							"exclude_blank_lines",
							"exclude_comments",
							"comment_prefixes",
							"max_file_size",
							"overwrite",
						], [list, str]],
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
				if not value[0] and value[0] != [] and key not in kwargs:
					raise ArgumentRequired("\nArgument \"%s\" is required" % key)

		# Set any passed arguments
		for key, value in kwargs.items():
			if key not in self.arguments:
				raise ArgumentNotExist("\nArgument \"%s\" does not exist" % (key))
			if isinstance(value, tuple(self.arguments[key][1])):

				# Check if its directory or file
				if key == "dir":
					if os.path.isdir(value):
						self.is_dir = True
					else:
						self.is_dir = False

				# Make every element lowercase and add "." in the start of it
				elif key == "exclude_ext":
					value = ["%s%s" % ("." if not data.startswith(".") else "", data.lower())  for data in value]

				elif key == "exclude_files":
					if not isinstance(value, list):
						value = [value]

				elif key == "exclude_folders":
					if not isinstance(value, list):
						value = [value]

				# Set attribute
				setattr(self, key, value)
				continue
			raise WrongArgumentType("\nArgument type \"%s\" for \"%s\" is incorrect" % (type(value), value))

	def GetExtensions(self):
		extensions = []
		for ext in self.__dict__:
			if ext not in Add(self.NO_VARIABLES, "lines"):
				extensions.append(".%s" % ext)
		return extensions

	# +
	def __add__(self, other):
		gl = copy(self)
		for var in other.__dict__:

			# Get all file type variables
			if var not in self.NO_VARIABLES:
				if hasattr(gl, var):
					setattr(gl, var, getattr(gl, var) + getattr(other, var))
					continue
				setattr(gl, var, getattr(other, var))
		return gl

	# +=
	def __iadd__(self, other):
		for var in other.__dict__:

			# Get all file type variables
			if var not in self.NO_VARIABLES:
				if hasattr(self, var):
					setattr(self, var, getattr(self, var) + getattr(other, var))
					continue
				setattr(self, var, getattr(other, var))
		return self

	# >
	def __gt__(self, other):
		return self.lines > other.lines

	# <
	def __lt__(self, other):
		return self.lines < other.lines

	# >=
	def __ge__(self, other):
		return self.lines >= other.lines

	# <=
	def __le__(self, other):
		return self.lines <= other.lines

	# ==
	def __eq__(self, other):
		return self.lines == other.lines

	# !=
	def __ne__(self, other):
		return self.lines != other.lines

	def __repr__(self):
		return self.lines

	def __str__(self):
		return str(self.__repr__())

	def __int__(self):
		return self.__repr__()
