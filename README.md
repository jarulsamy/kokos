# kokos
---
kokos is a multi-use Python package which includes all of my public Python packages.

Supports Python [3.7](https://www.python.org/downloads/release/python-370/ "Python 3.7") and [3.8](https://www.python.org/downloads/release/python-380/ "Python 3.8")

---
Installation ([pip page](https://pypi.org/project/kokos/)):

```
pip install kokos
```
You can use it like a normal package or from the command like (see [examples.md](examples.md "examples.md")):
```python
from kokos import cpu_stress_test
score = cpu_stress_test.Start()
print(score)
```
