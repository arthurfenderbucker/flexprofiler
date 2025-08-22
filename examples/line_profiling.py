"""Example showing line-by-line profiling with flexprofiler.

Run this script to see per-line timing collected by decorating a function
with @track(lines=True).
"""
import time
from flexprofiler import track, stats


@track(lines=True)
def compute(n):
    total = 0
    for i in range(n):
        total += i
        if i % 2 == 0:
            # Simulate work on some lines
            time.sleep(0.001)
        else:
            time.sleep(0.0005)
    return total


if __name__ == "__main__":
    for _ in range(3):
        compute(50)

    stats()  # display the profiling statistics