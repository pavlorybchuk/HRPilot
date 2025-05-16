from .Human import *


class Employee(Human):
    def __init__(self):
        super().__init__()
        self.position = None
        self.rate = 0

    def show_info(self):
        base_info = super().show_info()
        return base_info + (f"\nPosition: {self.position if self.position else "not mentioned"};\n"
                            f"Rate: {self.rate};\n")
