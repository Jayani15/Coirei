```markdown
# Performance Benchmark Report

Tests were conducted to measure the execution time and memory usage of the sandbox.

---

## Environment

Python Version: 3.x  
Framework: FastAPI  
Hardware: Local development machine

---

## Benchmark Results

| Test | Code | Time (ms) | Memory (MB) |
|-----|------|----------|-------------|
| Print | print("Hello") | 10-15 | 3 |
| Arithmetic | print(5+10) | 10-20 | 3 |
| Loop | for i in range(100000): pass | 20-30 | 4 |
| Fibonacci | recursive fib(20) | 60-80 | 5 |
| Infinite Loop | while True | 2000 (timeout) | 4 |

---

## Observations

- Simple programs execute in under **20ms**.
- Memory usage remains under **5MB** for most cases.
- Infinite loops are successfully terminated after **2 seconds**.

---

## Conclusion

The sandbox performs efficiently for small programs while maintaining security protections.