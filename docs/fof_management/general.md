Assuming that current directory's structure is the following (see [MyDirectory](../MyDirectory)):
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
from kokos import Folder
import os

dir = os.getcwd()
f = Folder(dir=dir)
print(f)
# MyDirectory
```
All arguments need to be passed by name (see [why_only_named_arguments.md](../general/why_only_named_arguments.md)).
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
Get a string that represents **f**'s structure
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
## Navigate through [FOF](../general/what_is_fof.md)
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
Loop thought [FOF](../general/what_is_fof.md)
```python
for fof in f:
	print(fof)
# Code
# Notes
# Photos
# other.txt
```
"Select" a [FOF](../general/what_is_fof.md)
```python
# Folder object
code_folder = f["Code"]

print(code_folder.files)
# [amazon_web_scraper.py, some_python_script.py, test.py]

# File object
test_program = code_folder["test.py"]

print(test_program.content)
# for i in range(100):
#         print(i)
```



Get [FOF](../general/what_is_fof.md)'s data
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
# Size: 31
# Permissions: 777

print(f["Code"]["test.py"].size)
# 31

print(f["other.txt"].content)
# this is a test
```
## Benchmark
After the first time running, will be faster because some data will be stored in cache
```python
from time import time

st = time()
f = Folder(dir=dir)

print("FOF a second: %s" % round((f.FOLDERS_NUM + f.FILES_NUM) / (time() - st)))
# first time:	360
# after:		1666
```
