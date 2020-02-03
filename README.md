# kokos
---
kokos is a multi-use Python package which includes many of my public Python projects.

Supports Python 3.
## Installation
```
git clone https://github.com/kokosxD/kokos
```
## CPU Stress Test
```python
from kokos import Start

score = Start()

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
See more in [examples](../docs)
