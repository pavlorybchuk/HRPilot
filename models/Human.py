from datetime import datetime
from customtkinter import *
import phonenumbers
from email_validator import validate_email, EmailNotValidError
import os
from CTkMessagebox import CTkMessagebox


class Human:
    def __init__(self, name, age, sex, phone, email, address, hdate, seniority, docs, duties, days, next_vacation,
                 status, salary, staff_id, photo, workspace):
        self.name = name.title() if name else None
        self._age = age
        self.sex = sex
        self._phone = phone
        self._email = email
        self._address = address
        self._hdate = datetime.strptime(hdate, "%d.%m.%Y") if hdate else datetime.now()
        self._seniority = int(seniority)
        self.docs = docs
        self._duties = duties
        self.days = days
        self._next_vacation = datetime.strptime(next_vacation,
                                                "%d.%m.%Y") if next_vacation else datetime.strptime(
            f"{self._hdate.day}.{self._hdate.month}.{self._hdate.year}", "%d.%m.%Y")
        self.status = status
        self._salary = float(salary)
        self.staff_id = staff_id
        self.workspace = workspace
        self.photo = photo

    def show_info(self) -> str:
        """
        Повертає стрічку з інформацію про об'єкт.
        :return: str
        """
        return (f"Name: {self.name};\n"
                f"ID: {self.staff_id};\n"
                f"Age: {self.age} years old;\n"
                f"Gender: {self.sex};\n"
                f"Phone: {self._phone};\n"
                f"Email: {self._email};\n"
                f"Address: {self.address if self.address else "not mentioned"};\n"
                f"Hire date: {datetime.strftime(self.hdate, "%d.%m.%Y")};\n"
                f"Next vacation: {datetime.strftime(self._next_vacation, "%d.%m.%Y")};\n"
                f"Work days: {", ".join(self.days) if self.days else "not mentioned"};")

    @property
    def phone(self) -> str:
        """
        Повертає номер телефону.
        :return: str
        """
        return self._phone

    @phone.setter
    def phone(self, number: str) -> None:
        """
        Задає значення номеру телефону.
        :param number: Новий номер телефону
        :return: None
        """
        try:
            parsed = phonenumbers.parse(number, None)
            if phonenumbers.is_valid_number(parsed) and phonenumbers.is_possible_number(parsed):
                self._phone = number
                return
        except phonenumbers.NumberParseException:
            raise ValueError("Phone is invalid")

    @property
    def age(self) -> str:
        """
        Повертає вік.
        :return: str
        """
        return self._age

    @age.setter
    def age(self, age: str) -> None:
        """
        Задає новий вік.
        :param age: Новий вік
        :return: None
        """
        if not age.isdigit():
            raise ValueError("Age must be an integer.")
        age = int(age)
        if age < 18 or age > 120:
            raise ValueError("Age is invalid.")

    @property
    def seniority(self) -> int:
        """
        Повертає стаж.
        :return: str
        """
        return self._seniority

    @seniority.setter
    def seniority(self, seniority: str) -> None:
        """
        Задає новий стаж.
        :param seniority: Новий стаж
        :return: None
        """
        if not seniority.strip():
            self._seniority = "not mentioned"
            return
        if not seniority.strip().isdigit():
            raise ValueError("Seniority must be an integer.")
        seniority = int(seniority.strip())
        if seniority > 50:
            raise ValueError("Seniority is invalid.")
        self._seniority = seniority

    @property
    def email(self) -> str:
        """
        Повертає електронну пошту.
        :return: str
        """
        return self._email

    @email.setter
    def email(self, email: str) -> None:
        """
        Задає нову електронну пошту.
        :param email: Нова електронна пошта
        :return: None
        """
        try:
            validate_email(email)
            self._email = email
        except EmailNotValidError:
            raise ValueError("Email is invalid")

    @property
    def address(self) -> str:
        """
        Повертає адресу проживання.
        :return: str
        """
        return self._address

    @address.setter
    def address(self, address: str) -> None:
        """
        Задає нову адресу проживання.
        :param address: Нова адреса проживання
        :return: None
        """
        if address.strip():
            self._address = address
            return
        else:
            self._address = "not mentioned"

    @property
    def duties(self) -> list:
        """
        Повертає список обов'язків.
        :return: list
        """
        return self._duties

    @duties.setter
    def duties(self, duty: str) -> None:
        """
        Додає новий обо'вязок до списку.
        :param duty: Новий обов'язок
        :return: None
        """
        if not duty.strip():
            raise ValueError("Duty is invalid")
        if duty.strip().lower() in [i.lower() for i in self._duties]:
            raise IndexError("This duty exists already!")
        self._duties.append(duty.strip())
        return

    def remove_duty(self, duty_index: int) -> None:
        """
        Видаляє обов'язок зі списку.
        :param duty_index: Індекс обов'язку
        :return: none
        """
        if duty_index >= len(self.duties) or duty_index < 0:
            raise IndexError("Duty index is out of range")
        self._duties.pop(duty_index)

    def show_duties(self) -> str:
        """
        Повертає стрічку зі списком обов'язків.
        :return: str
        """
        if not self._duties:
            return "not mentioned"
        line = ""
        count = 0
        for i in self._duties:
            count += 1
            line += f"{count}. {i};{"\n" if self._duties.index(i) != len(self._duties) - 1 else ""}"
        return line

    def show_docs(self, master) -> None:
        """
        Створює 4 пари надпис-кнопка у фреймі master, де надпис - це назва документа, а кнопка відкриває його.
        :param master: батьківський фрейм
        :return: None
        """
        def open_file(filepath):
            try:
                os.startfile(filepath)
            except FileNotFoundError:
                CTkMessagebox(master, message="This file doesn't exist", title="Error", icon="cancel")

        doc_frame = CTkFrame(master, fg_color="transparent")
        doc_frame.pack()
        passport_label = CTkLabel(doc_frame, text="Passport:", font=('Arial', 18))
        passport_label.grid(row=0, column=0, pady=2, sticky="w")
        open_passport = CTkButton(doc_frame, text="Open", font=("Arial", 18), width=150, height=40,
                                  command=lambda: open_file(self.docs["passport"]), fg_color=("#C5D86D", "#BBD5ED"),
                                  hover_color=("#B8D04E", "#9EC3E5"), text_color="black", corner_radius=10)
        open_passport.grid(row=0, column=1, pady=2, padx=10)
        graduation_label = CTkLabel(doc_frame, text="Graduation:", font=('Arial', 18))
        graduation_label.grid(row=1, column=0, pady=2, sticky="w")
        open_graduation = CTkButton(doc_frame, text="Open", font=("Arial", 18), width=150, height=40,
                                    command=lambda: open_file(self.docs["graduation"]), fg_color=("#C5D86D", "#BBD5ED"),
                                    hover_color=("#B8D04E", "#9EC3E5"), text_color="black", corner_radius=10)
        open_graduation.grid(row=1, column=1, pady=2, padx=10)
        med_card_label = CTkLabel(doc_frame, text="Medical card:", font=('Arial', 18))
        med_card_label.grid(row=2, column=0, pady=2, sticky="w")
        open_med_card = CTkButton(doc_frame, text="Open", font=("Arial", 18), width=150, height=40,
                                  command=lambda: open_file(self.docs["medcard"]), fg_color=("#C5D86D", "#BBD5ED"),
                                  hover_color=("#B8D04E", "#9EC3E5"), text_color="black", corner_radius=10)
        open_med_card.grid(row=2, column=1, pady=2, padx=10)
        mil_acc_label = CTkLabel(doc_frame, text="Military accounting:", font=('Arial', 18))
        mil_acc_label.grid(row=3, column=0, pady=2, sticky="w")
        open_mil_acc = CTkButton(doc_frame, text="Open", font=("Arial", 18), width=150, height=40,
                                 command=lambda: open_file(self.docs["mil_accounting"]),
                                 fg_color=("#C5D86D", "#BBD5ED"),
                                 hover_color=("#B8D04E", "#9EC3E5"), text_color="black", corner_radius=10)
        open_mil_acc.grid(row=3, column=1, pady=2, padx=10)

    @property
    def next_vacation(self) -> datetime:
        """
        Повертає дату наступної відпустки.
        :return: datetime
        """
        return self._next_vacation

    @next_vacation.setter
    def next_vacation(self, next_vacation: str) -> None:
        """
        Задає нову дату відпустки.
        :param next_vacation: Нова дата
        :return: None
        """
        if next_vacation.strip():
            self._next_vacation = datetime.strptime(next_vacation, "%d.%m.%Y")
        else:
            raise ValueError("Vacation date can't be empty")

    @property
    def hdate(self) -> datetime:
        """
        Повертає дату найму.
        :return: datetime
        """
        return self._hdate

    @hdate.setter
    def hdate(self, hdate: str) -> None:
        """
        Задає нову дату найму.
        :param hdate: Нова дата найму
        :return: None
        """
        if hdate.strip():
            self._hdate = datetime.strptime(hdate, "%d.%m.%Y")
            return
        raise ValueError("Hire date can't be empty")

    @property
    def salary(self) -> float:
        """
        Повертає зарплату.
        :return: str
        """
        return self._salary

    @salary.setter
    def salary(self, salary: str) -> None:
        """
        Задає нову зарплату.
        :param salary: Нова зарплата.
        :return: None
        """
        if not salary.strip().replace(".", "", 1).isdigit():
            raise ValueError("Salary must be a number")
        salary = float(salary.strip())
        if salary <= 0:
            raise ValueError("Salary must be greater than 0")
        self._salary = salary
