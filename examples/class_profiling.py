"""Class profiling example — demonstrates using @track_all to profile all methods of a class."""
import time
from flexprofiler import track_instance, stats

# use @track_instance decorator to profile the function
@track_instance
class Foo:
    def example_method(self):
        self.another_method()
        time.sleep(0.1)
    def another_method(self):
        time.sleep(0.2)

Foo().example_method()
Foo().another_method()

stats() # display the profiling statistics