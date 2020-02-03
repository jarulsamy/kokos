## Count lines
Get the number of lines in code in a given directory or file.
## Create an object
Assuming that the current directory is [MyDirectory]("../MyDirectory")
>GetLines(dir, exclude_ext=[], exclude_files=[], exclude_folders=[], exclude_blank_lines=True, exclude_comments=True, comment_prefixes={".py": "#"}, max_file_size=50000)

* **dir** => The directory from which to count lines (it can also be a file)
* **exclude_ext** => File extensions to exclude when counting
* **exclude_files** => File names to exclude when counting
* **exclude_folders** => Folder names to exclude when counting
* **exclude_blank_lines** => If set to **True**, it will not count blank lines
* **exclude_comments** => If set to **True**, it will not count comments (see **comment_prefixes**)
* **comment_prefixes** => A dictionary that specifies what comment prefix to use for each file extension.
* * **key** => File extension
* * **value** => Comment prefix

```python
from kokos import GetLines
import os

dir = os.getcwd()
gl = GetLines(dir=dir)

print(gl)
# 6
```
All arguments need to be passed by name (see [why_only_named_arguments.md](../general/why_only_named_arguments.md)).
## Visualize the object
---
### Get the number of lines in total
```python
print(gl.lines)
# 6
```
### Get the number of lines in all files with X extension
```python
print(gl.py)
# 2

print(gl.txt)
# 4
```
### Get all file extensions
```python
for ext in gl.GetExtensions():
	print(ext)
# .py
# .txt
```
---
## Object operations
Assuming that:
* ```gl1``` = ```GetLines(dir="../kokos/docs/MyDirectory/Code")```
* ```gl2``` = ```GetLines(dir="../kokos/docs/MyDirectory/Notes")```

```python
print(gl1.lines)
# 2

print(gl1.py)
# 2

print(gl2.lines)
# 3

print(gl2.txt)
# 3
```
**NOTE**:

An **AttributeError** will be raised if no file with **X** extension exists (in this case **.txt** for **gl1** and **.py** for **gl2**)
```python
print(gl1.txt)
# AttributeError: 'GetLines' object has no attribute 'txt'

print(gl2.py)
# AttributeError: 'GetLines' object has no attribute 'py'
```

Add 2 objects together
```python
gl3 = gl1 + gl2

print("gl3 total lines: %s" % gl3.lines)
print("gl3 .py lines: %s" % gl3.py)
print("gl3 .txt lines: %s" % gl3.txt)

# gl3 total lines: 5
# gl3 .py lines: 2
# gl3 .txt lines: 3
```
Check to see if an object is bigger than another based on their total lines
```python
print(gl1 > gl2)
# False
```
Check to see if an object is smaller than another based on their total lines
```python
print(gl1 < gl2)
# True
```
Check to see if an object is bigger or equal than/to another based on their total lines
```python
print(gl1 >= gl2)
# False
```
Check to see if an object is smaller or equal than/to another based on their total lines
```python
print(gl1 <= gl2)
# True
```
Check to see if 2 objects are equal
```python
print(gl1 == gl2)
# False
```
Check to see if 2 objects are not equal
```python
print(gl1 != gl2)
# True
```
<!-- add += -->
