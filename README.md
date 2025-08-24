# flexprofiler

A flexible profiling utility for Python.

## Installation

```bash
pip install flexprofiler
```
## Usage
A lightweight summary showing the most common ways to use flexprofiler.

Basic concepts:

- `@track()` - decorate a function to collect call counts and timing statistics. Args:
    - `lines`: boolean, collect per-line timing inside the function.
- `@track_all()` - Decorate a class to profile all its methods. Args:
    - `max_depth`: integer, how deep to recursively profile composed objects (default: 10).
    - `include`: list of method names to track (default: None to track all).
    - `exclude`: list of method names to skip (default: None to skip none).
    - `arg_sensitive`: list of method names to track argument values (default: None).
- `stats()` - print aggregated profiling statistics (function-level and, when enabled, line-level). Args:
    - `unit`: the time unit to use for displaying statistics (default: "ms").
    
---

## Examples

### 1. Tracking a Simple Function

```python
import time
from flexprofiler import stats, track

@track()  # Use @track() decorator to profile the function
def simple_func():
    time.sleep(0.1)

simple_func()
simple_func()

stats() # display the profiling statistics
```

output:

<pre>
Detailed Function Call Statistics:
<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">simple_func</span>: ───2 calls, 200.43ms, <span style="color:#ff0000;">Avg: 100.21ms</span>, Std: 0.01ms, Median: 100.21ms
</pre>

### 2. Tracking All Methods in a Class

```python
import time
from flexprofiler import track_all, stats

@track_all()  # Use @track_all() decorator to profile all methods in the class
class Foo:
    def example_method(self):
        self.another_method()
        time.sleep(0.1)
    def another_method(self):
        time.sleep(0.2)

Foo().example_method()
Foo().another_method()

stats()
```

output:
<pre>
Detailed Function Call Statistics:
<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">Foo.example_method</span>: ────────1 calls, 300.23ms, <span style="color:#ff0000;">Avg: 300.23ms</span>
  └──<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">Foo.another_method</span>: ───1 calls, 200.10ms, <span style="color:#ff0000;">Avg: 200.10ms</span>
<span style="color:#ffaf87;"></span><span style="font-weight:bold;color:#ffaf87;">Foo.another_method</span>: ────────1 calls, 200.11ms, <span style="color:#ffaf87;">Avg: 200.11ms</span>
</pre>


### 3. Tracking All Methods in a Class Recursively

```python
import time
from flexprofiler import track_all, stats

@track_all(max_depth=3)
class Foo:
    def __init__(self):
        self.sub_class = Bar()
    def example_method(self):
        self.another_method()
        time.sleep(0.1)
    def another_method(self):
        time.sleep(0.2)
    def calling_subclass_method(self):
        for i in range(3):
            self.sub_class.subclass_method_1()
            self.sub_class.subclass_method_2()
            self.sub_class.subclass_method_3()

class Bar:
    def subclass_method_1(self):
        time.sleep(0.05)
    def subclass_method_2(self):
        self.a()
        self.b()
    def subclass_method_3(self):
        self.a()
        self.b()
    def a(self):
        time.sleep(0.02)
    def b(self):
        time.sleep(0.01)

obj = Foo()
obj.example_method()
obj.calling_subclass_method()

stats()
```

output:
<pre>
Detailed Function Call Statistics:
<span style="color:#00ff00;"></span><span style="font-weight:bold;color:#00ff00;">Foo.__init__</span>: ───────────────────2 calls, 0.11ms, <span style="color:#00ff00;">Avg: 0.06ms</span>, Std: 0.08ms, Median: 0.06ms
<span style="color:#ff5f00;"></span><span style="font-weight:bold;color:#ff5f00;">Foo.example_method</span>: ────────────1 calls, 300.29ms, <span style="color:#ff5f00;">Avg: 300.29ms</span>
  └──<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">Foo.another_method</span>: ───────1 calls, 200.12ms, <span style="color:#ff0000;">Avg: 200.12ms</span>
<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">Foo.calling_subclass_method</span>: ───1 calls, 334.50ms, <span style="color:#ff0000;">Avg: 334.50ms</span>
  ├──<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">Bar.subclass_method_1</span>: ────3 calls, 150.31ms, <span style="color:#ff0000;">Avg: 50.10ms</span>, Std: 0.03ms, Median: 50.09ms
  ├──<span style="color:#ffafff;"></span><span style="font-weight:bold;color:#ffafff;">Bar.subclass_method_2</span>: ────3 calls, 91.64ms, <span style="color:#ffafff;">Avg: 30.55ms</span>, Std: 0.04ms, Median: 30.56ms
  │    ├──<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">Bar.a</span>: ───────────────3 calls, 60.27ms, <span style="color:#ff0000;">Avg: 20.09ms</span>, Std: 0.02ms, Median: 20.10ms
  │    └──<span style="color:#ffd7ff;"></span><span style="font-weight:bold;color:#ffd7ff;">Bar.b</span>: ───────────────3 calls, 30.36ms, <span style="color:#ffd7ff;">Avg: 10.12ms</span>, Std: 0.05ms, Median: 10.09ms
  └──<span style="color:#ffafff;"></span><span style="font-weight:bold;color:#ffafff;">Bar.subclass_method_3</span>: ────3 calls, 91.45ms, <span style="color:#ffafff;">Avg: 30.48ms</span>, Std: 0.18ms, Median: 30.46ms
       ├──<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">Bar.a</span>: ───────────────3 calls, 60.29ms, <span style="color:#ff0000;">Avg: 20.10ms</span>, Std: 0.02ms, Median: 20.10ms
       └──<span style="color:#ffd7ff;"></span><span style="font-weight:bold;color:#ffd7ff;">Bar.b</span>: ───────────────3 calls, 30.28ms, <span style="color:#ffd7ff;">Avg: 10.09ms</span>, Std: 0.01ms, Median: 10.09ms
</pre>

### 4. Track All lines in a function

```python
import time
from flexprofiler import track, stats

@track(lines=True)
def bar(n):
    total = 0
    for i in range(n):
        total += i
        if i % 2 == 0:
            time.sleep(0.001)
        else:
            time.sleep(0.0005)
    return total

@track()
def foo():
    for _ in range(3):
        bar(50)
```

outputs:
<pre>
Detailed Function Call Statistics:
<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">foo</span>: ──────────────────────────1 calls, 129.46ms, <span style="color:#ff0000;">Avg: 129.46ms</span>
  └──<span style="color:#ff0000;"></span><span style="font-weight:bold;color:#ff0000;">bar</span>: ─────────────────────3 calls, 128.98ms, <span style="color:#ff0000;">Avg: 42.99ms</span>, Std: 0.59ms, Median: 42.82ms
     <span style="font-style:italic;">12</span>:     total = 0────────────────────3 calls, 0.14ms, Avg: 0.05ms
     <span style="font-style:italic;">13</span>:     for i in range(n):───────────153 calls, 1.64ms, Avg: 0.01ms
     <span style="font-style:italic;">14</span>:         total += i───────────────150 calls, 0.80ms, Avg: 0.01ms
     <span style="font-style:italic;">15</span>:         if i % 2 == 0:───────────150 calls, 0.65ms, Avg: 0.00ms
     <span style="font-style:italic;">16</span>:             time.sleep(0.001)────75 calls, 81.61ms, Avg: 1.09ms
     <span style="font-style:italic;">18</span>:             time.sleep(0.0005)───75 calls, 43.88ms, Avg: 0.59ms
     <span style="font-style:italic;">19</span>:     return total─────────────────3 calls, 0.01ms, Avg: 0.00ms
</pre>



## Author
Arthur Bucker (<abucker@andrew.cmu.edu>)
