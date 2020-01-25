# kokos
---
kokos is a multi-use Python package which includes all of my public Python packages.

Supports Python 3.

## CPU Stress Test
```python
from kokos import cpu_stress_test
score = cpu_stress_test.Start()
print(score)
```
## FOF Management
```python
from kokos import Folder
import os

dir = os.getcwd()
f = Folder(dir=dir)

print(f)
```
See more in [examples](../examples)
