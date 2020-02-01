## cpu_stress_test
Stress test your CPU to see its performance

> Start(TIME=300, THREADS=20)

The score is calculated based on how many strings manages to hash using the [bcrypt](https://www.google.com/search?q=bcrypt "bcrypt") hashing algorithm in a given time.

```python
from kokos import Start

score = Start(TIME=300, THREADS=20)

print(score)
```

>* **TIME** => Duration of test in seconds
>* **THREADS** => Number of threads to use
