## cpu_stress_test
Stress test your CPU to see its performance and temperature (temperature not supported).

> cpu_stress_test.Start(TIME=None, THREADS=None, RETURN=False)

The score is calculated based on how many strings manages to hash using the [bcrypt](https://www.google.com/search?q=bcrypt "bcrypt") hashing algorithm.

```python
from kokos import cpu_stress_test
score = cpu_stress_test.Start()
print(score)
```
From command line:
```
kokos cst -t 300 -mt 20
```

>* **kokos** => package command
* **cst** => **c**pu **s**tress **t**est
* **-t** => stress test time (in seconds)
* **-mt** => number of threads

This is the only usage of the **kokos** command at this point.

>Note that you can use it from the command line, only on **Windows**.

---
Note that stress tests are using **100%** of the CPU, so save and close anything important before you start.
