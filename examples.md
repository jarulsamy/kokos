## cpu_stress_test
Stress test your CPU to see its performance and temperature (temperature not supported).

> cpu_stress_test.Start(TIME=300, MULTI_PROCESSES=20)

The score is calculated based on how many strings manages to hash using the [bcrypt](https://www.google.com/search?q=bcrypt "bcrypt") hashing algorithm.

```python
from kokos import cpu_stress_test
score = cpu_stress_test.Start()
print(score)
```
From command line:
```
cpu_stress_test -t 300 -mt 20
```		
* **-t** stress test time (in seconds)
* **-mt** number of processes

<b>* Note that you can use it from the command line, only on **Windows**.</b>

---
Note that stress tests are using **100%** of the CPU, so save and close anything important before you start.
