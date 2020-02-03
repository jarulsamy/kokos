## Get File info
Assuming that:
* ```dir``` = ```"../kokos/docs/MyDirectory```
* ```f``` = ```Folder(dir=dir)```
* ```file``` = ```f["other.txt"]```
* ```test_file``` = ```f["Code"]["test.py"]```

Get the full directory of a **File**
```python
print(file.dir)
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
## Operations between Files
Check if 2 files are equivalent
```python
print(file == test_file)
# False
```
Check if 2 files are not equivalent
```python
print(file != test_file)
# True
```
Check if an object is **File** or **Folder**
```python
print(file.IsFile())
# True

print(file.IsFolder())
# False

print(f.IsFile())
# False

print(f.IsFolder())
# True
```
