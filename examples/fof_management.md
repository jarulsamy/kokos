Assuming that current directory's structure is the following:
```
MyDirectory/
	Code/
		amazon_web_scraper.py
		some_python_script.py
		test.py
	Notes/
		notes.txt
	Photos/
		cat.jpg
		dog.png
	other.txt
```
## Create a Folder object
```python
from folder import Folder
import os

dir = os.getcwd()
f = Folder(dir=dir)
print(f)
# MyDirectory
```
All arguments need to be passed by name (see [why_only_named_arguments.md](../qna/why_only_named_arguments.md)).
## Visualize the structure
Get a list with all folders inside **f** as **Folder** objects
```python
print(f.folders)
# [Code, Notes, Photos]
```
Get a list with all files inside **f** as **File** objects
```python
print(f.files)
# [other.txt]
```
Returns a string that represents the structure of **f**
```python
print(f.CreateStructure())
# MyDirectory/
# │   Code/
# │   ├── amazon_web_scraper.py
# │   ├── some_python_script.py
# │   └── test.py
# │   Notes/
# │   └── notes.txt
# │   Photos/
# │   ├── cat.png
# │   └── dog.png
# └── other.txt
```
## Navigate through [FOF](../qna/what_is_fof.md)
Loop thought folders
```python
for folder in f.folders:
	print(folder)
# Code
# Notes
# Photos
```
Loop thought files
```python
for file in f.files:
	print(file)
# other.txt
```
Loop thought [FOF](../qna/what_is_fof.md)
```python
for fof in f:
	print(fof)
# Code
# Notes
# Photos
# other.txt
```
Select a [FOF](../qna/what_is_fof.md) and get its data
```python
for file in f["Code"]:
	print("Name: %s\nSize: %s\nPermissions: %s\n\n" % (file.name, file.size, file.permissions))
# Name: amazon_web_scraper.py
# Size: 0
# Permissions: 777
#
#
# Name: some_python_script.py
# Size: 0
# Permissions: 777
#
#
# Name: test.py
# Size: 180
# Permissions: 777

print(f["Code"]["test.py"].size)
# 180

print(f["other.txt"].content)
# this is a test
```
## Get Folder info
Get the full directory of a **Folder**
```python
print(f.dir)
# ../MyDirectory
```
Get the name of a **Folder**
```python
print(f.name)
# MyDirectory
```
Get the creation time of a **Folder** as a [DateTime](https://pypi.org/project/DateTime/) object
```python
print(f.created)
# 2020-01-25 12:30:00.000000
```
Get the last modified time of a **Folder** as [DateTime](https://pypi.org/project/DateTime/) object
```python
print(f.modified)
# 2020-01-25 12:35:00.000000
```
Get the last accessed time of a **Folder** as [DateTime](https://pypi.org/project/DateTime/) object
```python
print(f.accessed)
# 2020-01-25 12:35:00.000000
```
Get the owner of a **Folder**
```python
print(f.owner)
# kokos
```
Get the PC name to which a **Folder** belongs to
```python
print(f.pc_name)
# PC
```
Get the PC number to which a **Folder** belongs to (start counting from **1**)
```python
print(f.pc_number)
# 1
```
Get the permissions of a **Folder** that the current user has (in [octal](https://www.google.com/search?q=octal+permissions))
```python
print(f.permissions)
# 777
```
Get a [sha224](https://www.google.com/search?q=sha224+hash+algorithm) hash based on **hash_formula** for a **Folder**
```python
print(f.hash)
# 53e45f841fb6c7b352b80504c2a530a73d4aa2a6e4f249b57ce1f4d5
```
Get the size of a **Folder** in bytes
```python
print(f.size)
# 215
```
Get the number of folders inside a **Folder** (including sub-folders)
```python
print(f.FOLDERS_NUM)
# 3
```
Get the number of files inside a **Folder** (including sub-files)
```python
print(f.FILES_NUM)
# 7
```
## Get File info
Assuming that ```file``` = ```f["other.txt"]```

Get the full directory of a **File**
```python
print(f.dir)
# ../MyDirectory/other.txt
```
Get the name of a **File**
```python
print(file.name)
# other.txt
```
Get the extention of a **File**
```python
print(file.ext)
# .txt
```
Get the size of a **File**
```python
print(file.size)
# 16
```
Get the content of a **File**
```python
print(file.content)
# this is a test
```
Get the creation time of a **File** as a [DateTime](https://pypi.org/project/DateTime/) object
```python
print(file.created)
# 2020-01-25 12:40:00.000000
```
Get the last modified time of a **File** as a [DateTime](https://pypi.org/project/DateTime/) object
```python
print(file.modified)
# 2020-01-25 12:45:00.000000
```
Get the last accessed time of a **File** as a [DateTime](https://pypi.org/project/DateTime/) object
```python
print(file.accessed)
# 2020-01-25 12:45:00.000000
```
Get the owner of a **File**
```python
print(file.owner)
# kokos
```
Get the PC name to which a **File** belongs to
```python
print(file.pc_name)
# PC
```
Get the PC number to which a **File** belongs to (star counting from **1**)
```python
print(file.pc_number)
# 1
```
Get the permissions of a **File** that the current user has (in [octal](https://www.google.com/search?q=octal+permissions))
```python
print(file.permissions)
# 777
```
Get a [sha224](https://www.google.com/search?q=sha224+hash+algorithm) hash based on **hash_formula** for a **File**
```python
print(file.hash)
# acbe87ee112f6f73eba29442998d033b7ab9fa12569a05cd7224840a
```
