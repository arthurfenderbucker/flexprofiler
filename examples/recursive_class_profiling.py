
import time
from flexprofiler import track_all, stats

@track_all()
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

Foo().example_method()
Foo().calling_subclass_method()

stats()