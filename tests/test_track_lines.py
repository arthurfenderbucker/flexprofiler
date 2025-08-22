import time
from flexprofiler import FlexProfiler


def test_line_level_tracking():
    profiler = FlexProfiler(detailed=False, record_each_call=True)

    @profiler.track(lines=True)
    def foo(x):
        a = x + 1
        time.sleep(0.01)
        b = a * 2
        time.sleep(0.005)
        return b

    # Call function a few times to collect per-line timings
    foo(1)
    foo(2)

    key = 'foo'
    # Ensure we have recorded some line timings for this function
    assert key in profiler.line_stats
    # At least two distinct line numbers should have non-zero accumulated time
    nonzero_lines = [ln for ln, t in profiler.line_stats[key].items() if t > 0]
    assert len(nonzero_lines) >= 2
    # Ensure counts recorded
    counts = profiler.line_counts[key]
    assert any(c > 0 for c in counts.values())
