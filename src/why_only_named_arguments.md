# Why only named arguments?
---
Its a little bit overkill to use such a complex object-variable-define system as I do, but this way it can't cause any possible errors if a user passes a wrong argument.

You can see it as a way to "protect" a user from itself. I think that the default arguments are pretty good for 99% of cases.

Another advantage in comparison with positional arguments, is that if I a method have required arguments:
```python
# class File
def __init__(self, **kwargs):
	self.required = ["dir"]
	self.optional = {"calculate_hash": False, "hash_formula": ["dir", "name", "ext", "size", "content", "owner"], "max_file_size": 10000}

```
I have full control of what will happen in case the user won't specify them:
```python
# class File
for required in self.required:
	if not hasattr(self, required):
		raise ArgumentRequired("\nArgument \"%s\" is required" % required)
```
