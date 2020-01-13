>**GetFOF**(**multithreading**=**False**, **calculate_hash**=**True**, **hash_formula**=**["dir", "name", "ext", "size", "content", "owner"]**, **adding_action**=**"r"**, **max_file_size**=**10000**, **max_depth**=**3**)

* **multithreading** => If set to **True**, it will use many threads to search for [FOF](what_is_fof.md "What is FOF?"), for performance reasons, set it **False** for very small directories.
* **calculate_hash** => If set to **True**, it will calculate a hash based on **hash_formula** for each file and folder.
* **hash_formula** => **hash_formula** is used to tell **calculate_hash** on what data to base the [FOF](what_is_fof.md "What is FOF?") hash on. **hash_formula** will effect the result of **==** operation between objects because **==** is checking if hashes from both objects are same.
* **adding_action** => What action to take when adding 2 objects that have one or more same [FOF](what_is_fof.md "What is FOF?").
* * **s** => Skip
* * **w** => Overwrite
* * **a** => Append
* **max_file_size** => The [FOF](what_is_fof.md "What is FOF?") size limit to which it will read its content up to (in **bytes**).
* **max_depth** => The [FOF](what_is_fof.md "What is FOF?") depth which it will search trough when **CreateFileStructure()** is called by **\__repr\__**.

Assuming that the current directory have this structure:
```
MyDirectory/

	Photos/
		dog.jpg
		cat.png

	Code/
		python_script.py
		game_engine.cpp

	Other/
		TEMP/
			some_file.txt
```
Visualize folder structure:

```python
from kokos import FOF
import os
current_directory = os.getcwd()
# You need to pass it by name (see why_only_named_arguments.md)
f = FOF()
# returns folders, files
f.GetFOF(dir=current_directory)
print(f)
```
If you want to get a better idea of how the directory structure looks like, you can use **CreateFileStructure()**.
Its recommended to use it for small directories. For large ones, Its not going to effect the performance on any noticeable amount but if **max_depth** is set to a big number the output won't be easy to read:
```python
print(f.CreateFileStructure())
```
Output:
```
├MyDirectory
├──Photos
├────cat.png
├────dog.jpg
├──Code
├────python_script.py
├────game_engine.cpp
├──Other
├────TEMP
├──────some_file.txt
```
How **max_depth** effects the output of **CreateFileStructure()**:

* **max_depth** = **1**
```
├MyDirectory
├──Photos
├────...
├──Code
├────...
├──Other
├────...
```
* **max_depth** = **2**
```
├MyDirectory
├──Photos
├────cat.png
├────dog.jpg
├──Code
├────python_script.py
├────game_engine.cpp
├──Other
├────TEMP
├──────...
```
* **max_depth** = **3**
```
├MyDirectory
├──Photos
├────cat.png
├────dog.jpg
├──Code
├────python_script.py
├────game_engine.cpp
├──Other
├────TEMP
├──────some_file.txt
```
>**Save**(**path**=**"data.pickle"**, **compress**=**True**, **ignore_errors**=**True**)
* **path** => Path to the file that will save the object to
* **compress** => If set to **True**, it will compress the file
* **ignore_errors** => If set to **True**, it will ignore any possible errors.
>**Load**(**path**=**"data.pickle"**, **loading_action**=**"w"**, **uncompress**=**True**, **ignore_errors**=**True**)
* **path** => The path which it will load the object from
* **loading_action** => What action to take while loading
* * **w** => Overwrite the existing object data with the loaded ones
* * **r** => Return the loaded object
* **uncompress** => Set it to the same that **compress** was set when the object was saved.
* **ignore_errors** => If set to **True**, it will ignore any possible errors.

All of the examples bellow assume you have create a **FOF** object and call the **GetFOF()** method like shown:
```python
from kokos import FOF
import os
current_directory = os.getcwd()
f1 = FOF()
f1.GetFOF(dir=current_directory)
```
Save:
```python
# Save f1 to MyCustomName.something file
f1.Save(path="MyCustomName.something")
```
Load:
```python
# Overwrite the existing object
f1.Load(path="MyCustomName.something")
```
---
Here is an example to get a better idea of how **Load()** works:

This:
```python
# "r" for return
f2 = f1.Load(path="MyCustomName.something", loading_action="r")
```
Its the same as this:
```python
f2 = FOF()
# "w" for overwrite
f2.Load(path="MyCustomName.something", loading_action="w")
```
In the first example **f1** will call **Load()**, return a object and assign it to **f2**.

In the second example, **f2** was created, used to call **Load()** and load the **f1** that was previously saved in **MyCustomName.something**.

---
# Operations between objects

You can also add objects:
```
all_dirs = dir_1 + dir_2
```
**dir1** structure:
```
dir_1/
	Games/
		old_game.exe
```
**dir2** structure:
```
dir_2/
	Code/
		python_script.py
```
Add the objects:
```python
dir_1 = FOF(dir="/dir_1")
dir_2 = FOF(dir="/dir_2")
dir_1.GetFOF()
dir_2.GetFOF()

all_dirs = dir_1 + dir_2
```
**all_dirs** structure:
```
all_dirs/
	Games/
		old_game.exe
	Code/
		python_script.py
```
When 2 objects are being added the result is a **"virtual"** folder. This means that there is not any actual new folder be created.

---
