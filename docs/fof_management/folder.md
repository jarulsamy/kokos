## Get Folder info
Assuming that:
* ```dir``` = ```"../kokos/docs/MyDirectory```
* ```f``` = ``Folder(dir=dir)``
* ```f1``` = ```f["Code"]```
* ```f2``` = ```f["Notes"]```
* ```test_program``` = ```f["Code"]["test.py"]```

Get the full directory of a **Folder**
```python
print(f.dir)
# ../kokos/docs/MyDirectory
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
# 66
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
## Operations between Folders
Note that all of the following changes are virtual and no actual [FOF](../general/what_is_fof.md) will be effected

Check if 2 folders are equivalent
```python
print(f1 == f2)
# False
```
Check if 2 folders are not equivalent
```python
print(f1 != f2)
# True
```
Check if a [FOF](../general/what_is_fof.md) is in a folder
```python
print(test_program in f1)
# True
```
Add 2 folders together
```python
f3 = f1 + f2

for fof in f3:
	print(fof)
# amazon_web_scraper.py
# some_python_script.py
# test.py
# notes.txt
```
<!-- add - -->
<!-- add += -->
<!-- add -= -->
"Select" a [FOF](../general/what_is_fof.md) (return **None** if no [FOF](../general/what_is_fof.md) was found)
```python
web_scraper = f1["amazon_web_scraper.py"]

print(web_scraper.ext)
# .py
```
Get the number of [FOF](../general/what_is_fof.md) inside a **Folder**
```python
# get files and folders
print(len(f1))
# 4

# get number of folders (including subfolders)
print(f.FOLDERS_NUM)
# 3

# get number of files (including subfiles)
print(f.FILES_NUM)
# 7
```
Check if a **Folder** has something in it
```python
print(bool(f1))
# True
```
Get files and folders inside a **Folder**
```python
for fof in f1:
	print(fof)
# amazon_web_scraper.py
# some_python_script.py
# test.py
```
Check if an object is **File** or **Folder**
```python
print(f1.IsFolder())
# True

print(f1.IsFile())
# False

print(test_program.IsFolder())
# False

print(test_program.IsFile())
# True
```
