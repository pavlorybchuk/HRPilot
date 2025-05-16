from datetime import datetime
from customtkinter import *
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from PIL import Image


class Human:
    def __init__(self):
        self.name = None
        self.age = None
        self.sex = None
        self._phone = None
        self._email = None
        self._address = None
        self._hdate = None
        self.seniority = None
        self.seniority_bonus = 10
        self.premium_bonus = 80
        self._docs = {}
        self._duties = []
        self.days = []
        self._next_vacation = None
        self.status = "Normal"
        self._salary = None
        self._staff_id = None
        self.photo = None

    def show_info(self):
        return (f"Name: {self.name if self.name else "not mentioned"};\n"
                f"ID: {self._staff_id if self._staff_id else "not mentioned"};\n"
                f"Age: {self.age if self.age else "not mentioned"} years old;\n"
                f"Gender: {self.sex if self.sex else "not mentioned"}\n"
                f"Phone: {self._phone if self._phone else "not mentioned"};"
                f"Email: {self._email if self._email else "not mentioned"};\n"
                f"Address: {self.address if self.address else "not mentioned"};"
                f"Hire date: {self._hdate if self._hdate else "not mentioned"};")


    @property
    def staff_id(self):
        return self._staff_id

    @staff_id.setter
    def staff_id(self, staff_id: str, ids: list):
        if staff_id in ids:
            raise IndexError("This id is already in use.")
        if staff_id == "":
            raise ValueError("Id must be not empty.")
        self._staff_id = staff_id

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, number: str, default_region=None):
        try:
            parsed = phonenumbers.parse(number, default_region)
            if phonenumbers.is_valid_number(parsed) and phonenumbers.is_possible_number(parsed):
                self._phone = number
                return
        except phonenumbers.NumberParseException:
            raise ValueError

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        try:
            validate_email(email)
            self._email = email
            return
        except EmailNotValidError:
            raise ValueError("Email is invalid.")

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address: str):
        if address.strip():
            self._address = address
            return
        raise ValueError("Address is invalid.")

    @property
    def hdate(self):
        return self._hdate

    @hdate.setter
    def hdate(self, hdate: str):
        self._hdate = datetime.strptime(hdate, "%m.%d.%Y")

    @property
    def duties(self):
        return self._duties

    @duties.setter
    def duties(self, dutie: str):
        if dutie.strip():
            self._duties.append(dutie)
            return
        raise ValueError("Duties is invalid.")

    def show_duties(self):
        line = ""
        if not self._duties:
            return "Not mentioned"
        for i in range(len(self._duties)):
            line += f"{self._duties[i]}{", " if i != len(self._duties) - 1 else ''}"
        return line

    def show_docs(self, type_of_doc: int):
        top_level = CTkToplevel()
        top_level.resizable(False, False)
        if type_of_doc == 1:
            label = CTkLabel(top_level, text="", image=CTkImage(Image.open(self._docs["passport"])))
            label.pack()
        elif type_of_doc == 2:
            label = CTkLabel(top_level, text="", image=CTkImage(Image.open(self._docs["graduation"])))
            label.pack()
        elif type_of_doc == 3:
            label = CTkLabel(top_level, text="", image=CTkImage(Image.open((self._docs["medcart"]))))
            label.pack()
        else:
            label = CTkLabel(top_level, text="", image=CTkImage(Image.open((self._docs["mil_accounting"]))))
            label.pack()
        top_level.mainloop()

    @property
    def next_vacation(self):
        return self._next_vacation

    @next_vacation.setter
    def next_vacation(self, next_vacation: str):
        self._next_vacation = datetime.strptime(next_vacation, "%m.%d.%Y")
