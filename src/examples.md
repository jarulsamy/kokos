>**GetFOF**(**multithreading**=**False**, **calculate_hash**=**True**, **hash_formula**=**["dir", "name", "ext", "size", "content", "owner"]**, **adding_action**=**"r"**, **max_file_size**=**10000**, **max_depth**=**3**)

* **multithreading** => If set to **True**, it will use many threads to search for [FOF](what_is_fof.md "What is FOF?"), for performance reasons, set it **False** for very small directories.
* **calculate_hash** => If set to **True**, it will calculate a hash based on **hash_formula** for each file and folder.
* **hash_formula** => **hash_formula** is used to tell **calculate_hash** on what data to base the [FOF](what_is_fof.md "What is FOF?") hash on. **hash_formula** will effect the result of **==** operation between objects because **==** is checking if hashes from both objects are same.
* **adding_action** => What action to take when adding 2 objects that have one or more same [FOF](what_is_fof.md "What is FOF?").
* * **r** => Skip
* * **w** => Overwrite
* * **a** => Append
* **max_file_size** => The [FOF](what_is_fof.md "What is FOF?") size limit which it will read its content up to (in **bytes**).
* **max_depth** => The [FOF](what_is_fof.md "What is FOF?") depth which it will search trough when **CreateFileStructure()** is called by **__repr__**.

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
f = FOF(dir=current_directory)
# returns folders, files
f.GetFOF()
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
>**Save**(**path**=**"data.pickle"**)
* **path** => Path to the file that will save the object to
>**Load**(**path**=**"data.pickle"**, **loading_action**=**"w"**)
* **loading_action** => What action to take while loading
* * **w** => Overwrite the existing object data with the loaded ones
* * **r** => Return the loaded object

All of the examples bellow assume that you have create a **FOF** object and call the **GetFOF()** method:
```python
from kokos import FOF
import os
current_directory = os.getcwd()
f = FOF(dir=current_directory)
f.GetFOF()
```
Save:
```python
f.Save(path="MyCustomName.something")
```
Load:
```python
# Overwrite the existing object
f.Load(path="MyCustomName.something")
# Return the object
f2 = f.Load(path="MyCustomName.something", loading_action="r")
```
Operations between objects:
```python
print(f == f2)
# True

# When 2 objects are being added the result will be based on "adding_action"
# which can be specified when GetFOF() is called (default is "s").
f + f2
```
