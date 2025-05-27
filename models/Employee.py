from .Human import *


class Employee(Human):
    def __init__(self, name, age, sex, phone, email, address, hdate, seniority, docs, duties, days, next_vacation,
                 status, salary, staff_id, photo, workspace, position, rate):
        super().__init__(name, age, sex, phone, email, address, hdate, seniority, docs, duties, days, next_vacation,
                         status, salary, staff_id, photo, workspace)
        self.position = position
        self.rate = rate

    def show_info(self) -> str:
        """
        Повертає стрічку з інформацію про об'єкт.
        :return: str
        """
        base_info = super().show_info()
        return base_info + (f"\nPosition: {self.position if self.position else "not mentioned"};\n"
                            f"Rate: {self.rate}/10;")
