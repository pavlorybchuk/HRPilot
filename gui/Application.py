import random
from PIL import Image
from customtkinter import *
import json
from models import *
import pyperclip
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
import tkinter as tk
from datetime import datetime, date
import hashlib
import string


class Application(CTk):
    opened_windows = []
    today = date(datetime.now().year, date.today().month, date.today().day)

    def __init__(self):
        """
        Створює вікно, об'єкт Admin та заповняє його.
        """
        super().__init__()
        self.opened_windows.append(self)
        self.title('HRPilot')
        set_appearance_mode("light")
        self.iconbitmap('DB/public/hr_software_icon.ico')
        self.users = Application.load_base("DB/users.json")
        self.configure(fg_color=("#F7F7F2", "#131200"))
        if not self.users:
            CTkMessagebox(self, message="Can't start the program. No admin exist.", title="Error", icon="cancel")
            self.destroy()
        self.__admin = Admin(
            name=self.users["admin"]["name"],
            age=self.users["admin"]["age"],
            sex=self.users["admin"]["sex"],
            phone=self.users["admin"]["phone"],
            email=self.users["admin"]["email"],
            address=self.users["admin"]["address"],
            hdate=self.users["admin"]["hdate"],
            seniority=self.users["admin"]["seniority"],
            docs=self.users["admin"]["docs"],
            duties=self.users["admin"]["duties"],
            days=self.users["admin"]["days"],
            next_vacation=self.users["admin"]["next_vacation"],
            status=self.users["admin"]["status"],
            salary=self.users["admin"]["salary"],
            staff_id=self.users["admin"]["staff_id"],
            photo=self.users["admin"]["photo"],
            workspace=self.users["admin"]["workspace"],
            notes=self.users["admin"]["notes"]
        )
        for action in self.users["admin"]["actions_history"]:
            self.__admin.action_history = Action(
                action["action_name"],
                action["describe"],
                action["creator_id"],
                action["date_of_creating"],
            )
        for project in self.users["admin"]["projects"]:
            self.__admin.projects = Project(
                project["name"],
                project["description"],
                project["date_of_start"],
                project["date_of_end"],
                project["importance"],
                project["executed"]
            )
        self.employees = []
        for emp in self.users["employees"]:
            w_p = self.users["employees"][emp]
            self.employees.append(
                Employee(w_p["name"], w_p["age"], w_p["sex"], w_p["phone"], w_p["email"], w_p["address"], w_p["hdate"],
                         w_p["seniority"], w_p["docs"], w_p["duties"], w_p["days"], w_p["next_vacation"],
                         w_p["status"], w_p["salary"], emp, w_p["photo"], w_p["workspace"], w_p["position"],
                         w_p["rate"])
            )
        self.create_login_window()
        self.protocol("WM_DELETE_WINDOW", self.close_windows)

    def check_user(self, username: str, password: str) -> bool:
        """
        Перевіряє логін і пароль.
        :param username: логін
        :param password: пароль
        :return: bool
        """
        if self.users["admin"]["login"] == username and self.users["admin"]["password"] == hashlib.sha256(
                password.encode()).hexdigest():
            return True
        return False

    def create_login_window(self) -> None:
        """
        Створює вікно логування.
        :return: None
        """

        def handle_click() -> None:
            """
            Перехоплює натискання на кнопку submit_btn і, якщо логін і пароль правильні, змінює надпис на
            відповідне повідомлення і запускає іншу функцію створення всього UI.
            :return: None
            """
            res = self.check_user(login_entry.get(), password_entry.get())
            if res:
                header.configure(text="Starting program...")
                self.after(1000, self.create_ui)
            else:
                header.configure(text="Invalid username or password")

        for i in self.winfo_children():
            i.destroy()
        header = CTkLabel(self, text='Login', font=('Arial', 28), text_color=("black", "white"),
                          fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
        header.pack(pady=20, padx=30)
        login_entry = CTkEntry(self, placeholder_text="Username", font=('Arial', 18), width=200, height=40)
        password_entry = CTkEntry(self, placeholder_text="Password", font=('Arial', 18), width=200, height=40)
        submit_btn = CTkButton(self, text="Submit", fg_color=("#C5D86D", "#BBD5ED"), font=('Arial', 18),
                               text_color="black", corner_radius=10,
                               width=200, height=40, hover_color=("#B8D04E", "#9EC3E5"), command=handle_click)
        login_entry.pack(pady=5, padx=30)
        password_entry.pack(pady=5, padx=30)
        submit_btn.pack(pady=10)

    def create_ui(self) -> None:
        """
        Створює інтерфейс програми.
        :return: None
        """
        for i in self.winfo_children():
            i.destroy()
        self.geometry("1100x700+250+100")
        self.resizable(False, False)
        header_plate = CTkFrame(self, width=1100, height=70, fg_color=("#C5D86D", "#0A2239"), corner_radius=0)
        header_plate.pack()
        header_plate.pack_propagate(False)
        header_title = CTkLabel(header_plate, text='HRPilot', font=('Arial', 28),
                                text_color=("black", "white"),
                                fg_color="transparent", bg_color=("#C5D86D", "#0A2239"))
        header_title.pack(pady=10, padx=30, side=LEFT)
        theme_switcher = CTkSwitch(header_plate, text='Theme', font=('Arial', 16), command=Application.theme_switcher)
        theme_switcher.pack(pady=10, padx=30, side=RIGHT)
        if self.users["admin"]["theme"] != "light":
            theme_switcher.toggle()
        self.tabs = CTkTabview(self, width=1060, height=580, fg_color=("#E4E6C3", "#496A81"), corner_radius=10,
                               segmented_button_unselected_color=("#C5D86D", "#BBD5ED"),
                               segmented_button_selected_color=("#E4E6C3", "#496A81"),
                               segmented_button_unselected_hover_color=("#C5D86D", "#BBD5ED"),
                               segmented_button_selected_hover_color=("#E4E6C3", "#496A81"),
                               text_color="black",
                               segmented_button_fg_color=("#C5D86D", "#BBD5ED"))
        self.tabs.pack(padx=20, pady=20, side=BOTTOM)
        self.tabs.add("Profile")
        self.tabs.add("Employees")
        self.tabs.add("Projects")
        self.tabs.add("History")
        self.tabs.add("Notes")
        self.create_profile()
        self.create_emploees_tab()
        self.create_projects_tab()
        actions = self.tabs.tab("History")
        actions_wrapper = CTkScrollableFrame(actions, fg_color="transparent",
                                             scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                             scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
        actions_wrapper.pack(fill="both", expand=True)
        self.render_actions(actions_wrapper)

        notes = CTkTextbox(self.tabs.tab("Notes"), font=('Arial', 18), border_color="grey80",
                           fg_color=("#F7F7F2", "#BBD5ED"), corner_radius=10, border_width=1, text_color="black")
        notes.pack(pady=10, padx=10, fill=BOTH, expand=True)
        notes.insert("0.0", self.__admin.notes)

        def on_notes_input() -> None:
            """
            Перехоплює ввід символів у поле notes і відразу зберігає до властивості notes об'єкта Admin.
            :return: None
            """
            self.__admin.notes = notes.get("0.0", END)

        notes.bind("<KeyRelease>", lambda event: on_notes_input())

    def create_profile(self) -> None:
        """
        Створює вкладку з профілем адміністратора.
        :return: None
        """

        def change_profile() -> None:
            """
            Відслідковує нажаття на кнопку change_btn і створює нове вікно з формою, де можна
            вводити нові значення для властивостей об'єкта Admin.
            :return: None
            """

            def save_changes() -> None:
                """
                Витягує дані з форми та вставляє їх у відповідні властивості об'єкту Admin, а також закриває вікно.
                :return: None
                """
                try:
                    if entries[0].get().strip().replace(" ", "").isalpha():
                        self.__admin.name = entries[0].get().strip().title()
                    else:
                        raise ValueError("Name must be alphabetic")
                    self.__admin.age = entries[1].get().strip()
                    self.__admin.sex = "Male" if not sex_var.get() else "Female"
                    self.__admin.phone = entries[3].get().strip()
                    self.__admin.email = entries[4].get().strip()
                    self.__admin.address = entries[5].get().strip()
                    self.__admin.hdate = entries[6].get()
                    self.__admin.seniority = entries[7].get().strip()
                    if datetime.strptime(entries[8].get(), "%d.%m.%Y") > self.__admin.hdate:
                        self.__admin.next_vacation = entries[8].get()
                    else:
                        raise ValueError(
                            "The date of the next vacation cannot coincide with or be earlier than the date of hire")
                    temp = []
                    for i in days_vars:
                        if i.get():
                            temp.append(i.get())
                    self.__admin.days = temp
                    self.__admin.status = entries[10].get().strip().capitalize() if entries[
                        10].get().strip().capitalize() else "not mentioned"
                    self.__admin.salary = entries[11].get().strip()
                    self.__admin.workspace = entries[12].get().strip().capitalize() if entries[
                        12].get().strip().capitalize() else "not mentioned"
                    self.__admin.photo = path_labels[0].cget("text")
                    if "not mentioned" not in (path_labels[0].cget("text"),
                                               path_labels[1].cget("text"),
                                               path_labels[2].cget("text"),
                                               path_labels[3].cget("text"),
                                               path_labels[4].cget("text")):
                        self.__admin.photo = path_labels[0].cget("text")
                        self.__admin.docs = {"passport": path_labels[1].cget("text"),
                                             "graduation": path_labels[1].cget("text"),
                                             "medcard": path_labels[3].cget("text"),
                                             "mil_accounting": path_labels[4].cget("text")}
                    else:
                        raise ValueError("All documents and photo required")
                    current_user_info_label.configure(text=f"ID: {self.__admin.staff_id};\n"
                                                           f"Phone: {self.__admin.phone};\n"
                                                           f"Email: {self.__admin.email};\n"
                                                           f"Address: {self.__admin.address if self.__admin.address else "not mentioned"};")
                    image.close()
                    new_image = Image.open(self.__admin.photo)
                    resized_new_image = Application.crop_center(new_image, (300, 400))
                    ctk_new_image = CTkImage(light_image=resized_new_image, dark_image=resized_new_image,
                                             size=(200, 300))
                    current_user_image.configure(image=ctk_new_image)
                    current_user_image.image = ctk_new_image
                    self.__admin.action_history = Action("CHANGE",
                                                         f"User {self.__admin.staff_id} changed profile",
                                                         self.__admin.staff_id, datetime.strftime(
                            datetime.now(), "%d.%m.%Y %H:%M"))
                    self.render_actions(self.recent_actions, True)
                    self.render_actions(self.tabs.tab("History").winfo_children()[0])
                    CTkMessagebox(self, message="Profile was changed", title="Success", icon="check")
                    self.on_close(new_window)
                except Exception as e:
                    CTkMessagebox(self, message=str(e), title="Error", icon="cancel")

            new_window = CTk()
            self.opened_windows.append(new_window)
            new_window.configure(fg_color=("#F7F7F2", "#131200"))
            new_window.iconbitmap('DB/public/hr_software_icon.ico')
            new_window.title("Change")
            new_window.geometry("1000x500+0+0")
            new_window.minsize(700, 500)

            chng_profile_frame = CTkScrollableFrame(new_window, fg_color="transparent",
                                                    scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                                    scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
            chng_profile_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

            properties = ["Name:", "Age:", "Gender:", "Phone:", "Email:", "Address:", "Hire date:", "Seniority:",
                          "Next vacation:", "Days:", "Status:", "Salary:", "Workspace:", "Photo:", "Passport:",
                          "Graduation:", "Medical card:", "Military accounting:"]
            path_labels = []
            values = [
                self.__admin.name.title(),
                self.__admin.age,
                self.__admin.sex,
                self.__admin.phone,
                self.__admin.email,
                self.__admin.address,
                self.__admin.hdate,
                self.__admin.seniority,
                self.__admin.next_vacation,
                self.__admin.days,
                self.__admin.status,
                self.__admin.salary,
                self.__admin.workspace,
                self.__admin.photo,
                self.__admin.docs["passport"],
                self.__admin.docs["graduation"],
                self.__admin.docs["medcard"],
                self.__admin.docs["mil_accounting"]
            ]
            entries = []
            row = 0
            for prop in properties:
                label = CTkLabel(chng_profile_frame, text=prop, font=('Arial', 18), text_color=("black", "white"),
                                 fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
                label.grid(row=row, column=0, pady=4, sticky="w")
                if row < 13:
                    if row == 2:
                        sex_var = IntVar(value=(0 if values[row] == "Male" else 1))
                        sex_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                        sex_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        male_btn = CTkRadioButton(sex_wrapper, text="Male", font=('Arial', 18), variable=sex_var,
                                                  value=0)
                        male_btn.grid(row=0, column=0)
                        female_btn = CTkRadioButton(sex_wrapper, text="Female", font=('Arial', 18), value=1,
                                                    variable=sex_var)
                        female_btn.grid(row=0, column=1)
                        entries.append(sex_wrapper)
                    elif row == 6:
                        hdate_picker = DateEntry(chng_profile_frame, font=('Arial', 18), justify=CENTER,
                                                 text_color=("black", "white"),
                                                 width=12, height=40,
                                                 date_pattern='dd.mm.yyyy',
                                                 year=values[row].year if values[row].year else self.today.year,
                                                 month=values[row].month if values[row].month else self.today.month,
                                                 day=values[row].day if values[row].day else self.today.day,
                                                 maxdate=self.today)
                        hdate_picker.bind("<<DateEntrySelected>>",
                                          lambda x: Application.on_hdate_change(hdate_picker, next_vacation_picker))
                        hdate_picker.grid(row=row, column=1, padx=10, sticky="w")
                        entries.append(hdate_picker)
                    elif row == 8:
                        next_vacation_picker = DateEntry(chng_profile_frame, font=('Arial', 18), justify=CENTER,
                                                         width=12, height=40, text_color=("black", "white"),
                                                         date_pattern='dd.mm.yyyy',
                                                         year=values[row].year + 1 if values[
                                                             row].year else self.today.year,
                                                         month=values[row].month if values[
                                                             row].month else self.today.month,
                                                         day=values[row].day if values[row].day else self.today.day,
                                                         mindate=date(values[row].year, values[row].month,
                                                                      values[row].day))
                        next_vacation_picker.grid(row=row, column=1, padx=10, sticky="w")
                        entries.append(next_vacation_picker)
                    elif row == 9:
                        days_vars = []
                        days_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                        days_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                        column = 0
                        for day in days:
                            days_vars.append(StringVar(value=("" if day not in values[row] else day)))
                            radio = CTkCheckBox(days_wrapper, text=day, font=('Arial', 18),
                                                variable=days_vars[column],
                                                onvalue=day, offvalue="", text_color=("black", "white"))
                            radio.grid(row=0, column=column)
                            column += 1
                        entries.append(days_wrapper)
                    else:
                        entry = CTkEntry(chng_profile_frame, width=500, height=40, font=("Arial", 18),
                                         text_color=("black", "white"))
                        entry.insert(0, values[row])
                        entry.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        entries.append(entry)
                else:
                    path_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                    path_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                    path_label = CTkLabel(path_wrapper, text=values[row], font=('Arial', 18), wraplength=300,
                                          text_color=("black", "white"),
                                          fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
                    path_label.grid(row=0, column=0)
                    path_labels.append(path_label)
                    path_copier = CTkButton(path_wrapper, text="Copy", width=130, height=40, font=("Arial", 18),
                                            command=lambda x=path_label: pyperclip.copy(x.cget("text")),
                                            corner_radius=10,
                                            fg_color=("#C5D86D", "#BBD5ED"), hover_color=("#B8D04E", "#9EC3E5"),
                                            text_color="black")
                    path_chooser = CTkButton(path_wrapper, text="Change", width=130, height=40, font=("Arial", 18),
                                             command=lambda x=path_label, y=path_copier: Application.choose_file(x, y),
                                             corner_radius=10,
                                             fg_color=("#C5D86D", "#BBD5ED"), hover_color=("#B8D04E", "#9EC3E5"),
                                             text_color="black")
                    path_chooser.grid(row=0, column=1, padx=10)
                    path_copier.grid(row=0, column=2, padx=10)
                    entries.append(path_wrapper)
                row += 1
            save_btn = CTkButton(new_window, text="Save", width=200, height=40, font=("Arial", 18),
                                 fg_color=("#C5D86D", "#BBD5ED"), command=save_changes, corner_radius=10,
                                 hover_color=("#B8D04E", "#9EC3E5"), text_color="black")
            save_btn.pack(padx=10, pady=10)

            new_window.protocol("WM_DELETE_WINDOW", lambda x=new_window: self.on_close(x))
            new_window.mainloop()

        def show_details() -> None:
            """
            Створює нове вікно з детальною інформацією про користувача (адміністратора відповідно).
            :return: None
            """
            new_window = CTk()
            self.opened_windows.append(new_window)
            new_window.configure(fg_color=("#F7F7F2", "#131200"))
            new_window.title("Details")
            new_window.iconbitmap('DB/public/hr_software_icon.ico')
            new_window.resizable(False, False)
            new_window.geometry("600x600")
            show_details_frame = CTkScrollableFrame(new_window, fg_color="transparent",
                                                    scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                                    scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
            show_details_frame.pack(fill=BOTH, expand=True)

            cur_user_info_label = CTkLabel(show_details_frame,
                                           text=self.__admin.show_info(),
                                           font=('Arial', 18), justify=LEFT, text_color=("black", "white"),
                                           fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
            cur_user_info_label.pack(pady=10)

            chng_btn = CTkButton(show_details_frame, width=200, height=40, text="Change",
                                 fg_color=("#C5D86D", "#BBD5ED"),
                                 hover_color=("#B8D04E", "#9EC3E5"), corner_radius=10, text_color="black",
                                 font=('Arial', 18),
                                 command=change_profile)
            chng_btn.pack(pady=10)

            documents_label = CTkLabel(show_details_frame, text="Documents", font=('Arial', 20),
                                       text_color=("black", "white"),
                                       fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
            documents_label.pack(pady=10)

            documents_frame = CTkFrame(show_details_frame, fg_color="transparent")
            documents_frame.pack()
            self.__admin.show_docs(documents_frame)

            projects_label = CTkLabel(show_details_frame, text="Projects", font=('Arial', 20),
                                      text_color=("black", "white"),
                                      fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
            projects_label.pack(pady=10)
            projects = CTkLabel(show_details_frame, text=self.__admin.show_projects(), font=('Arial', 18),
                                text_color=("black", "white"),
                                justify=LEFT,
                                fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
            projects.pack()
            new_window.protocol("WM_DELETE_WINDOW", lambda x=new_window: self.on_close(x))

            new_window.mainloop()

        frame = CTkScrollableFrame(self.tabs.tab("Profile"), fg_color="transparent",
                                   scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                   scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"),
                                   width=1040, height=500)
        frame.pack()
        image = Image.open(self.__admin.photo)
        resized_image = Application.crop_center(image, (200, 300))
        ctk_image = CTkImage(light_image=resized_image, dark_image=resized_image, size=(200, 300))
        current_user_image = CTkLabel(frame, text="",
                                      image=ctk_image)
        current_user_image.grid(row=0, column=0, rowspan=2, sticky="e", padx=30)

        current_user_info_label = CTkLabel(frame,
                                           text=f"ID: {self.__admin.staff_id};\n"
                                                f"Phone: {self.__admin.phone};\n"
                                                f"Email: {self.__admin.email};\n"
                                                f"Address: {self.__admin.address if self.__admin.address else "not mentioned"};",
                                           font=('Arial', 20), justify=LEFT, text_color=("black", "white"),
                                           fg_color="transparent", bg_color=("#E4E6C3", "#496A81"))
        current_user_info_label.grid(row=0, column=1, sticky="sw", pady=10)

        actions_frame = CTkFrame(frame, fg_color="transparent", bg_color=("#E4E6C3", "#496A81"))
        actions_frame.grid(row=1, column=1, sticky="nw")

        show_details = CTkButton(actions_frame, width=200, height=40, text="Details", fg_color=("#C5D86D", "#BBD5ED"),
                                 hover_color=("#B8D04E", "#9EC3E5"), corner_radius=10, text_color="black",
                                 font=('Arial', 18),
                                 command=show_details, bg_color=("#E4E6C3", "#496A81"))
        show_details.grid(row=0, column=0)
        change_btn = CTkButton(actions_frame, width=200, height=40, text="Change", fg_color=("#C5D86D", "#BBD5ED"),
                               hover_color=("#B8D04E", "#9EC3E5"), corner_radius=10, text_color="black",
                               font=('Arial', 18),
                               command=change_profile, bg_color=("#E4E6C3", "#496A81"))
        change_btn.grid(row=0, column=1, padx=10)

        recent_actions_label = CTkLabel(frame, text="Recent actions", font=('Arial', 20), justify=LEFT,
                                        width=1025, text_color=("black", "white"),
                                        fg_color="transparent", bg_color=("#E4E6C3", "#496A81"))
        recent_actions_label.grid(row=2, column=0, columnspan=2, pady=20)

        self.recent_actions = CTkFrame(frame, fg_color="transparent", width=1025, bg_color=("#E4E6C3", "#496A81"))
        self.recent_actions.grid(row=3, column=0, columnspan=2)
        self.render_actions(self.recent_actions, True)

    def create_emploees_tab(self) -> None:
        """
        Створює вкладку з працівниками, пошуком та фільтром для сортування працівників у списку.
        :return: None
        """

        def update_list() -> None:
            """
            При виборі значення у фільтрі (CTkOptionMenu),
            або при вводі будь-якого символу в пошук,
            перемальовує список працівників.
            :return: None
            """
            self.render_employees(employees_frame, filter_drop_down.get(), search_entry.get())

        def add_emp() -> None:
            """
            Створює нове вікно з формою для заповнення і створення нового користувача.
            :return: None
            """

            def add_employee() -> None:
                """
                Витягує дані з форми, створює новий об'єкт Employee і заповняє його властивості.
                :return: None
                """
                # try:
                new_emp = Employee("", 0, "", "",
                                   "", "", "", 0,
                                   {}, [], [], "", "",
                                   0, "", "", "", "", 0)
                if entries[0].get().strip().replace(" ", "").isalpha():
                    new_emp.name = entries[0].get().strip().title()
                else:
                    raise ValueError("Name must be alphabetic")
                new_emp.age = entries[1].get().strip()
                new_emp.sex = "Male" if not sex_var.get() else "Female"

                new_emp.phone = entries[3].get().strip()
                new_emp.email = entries[4].get().strip()
                new_emp.address = entries[5].get().strip()
                new_emp.hdate = entries[6].get()
                new_emp.seniority = entries[7].get().strip()
                if datetime.strptime(entries[8].get(), "%d.%m.%Y") > new_emp.hdate:
                    new_emp.next_vacation = entries[8].get()
                else:
                    raise ValueError(
                        "The date of the next vacation cannot coincide with or be earlier than the date of hire")
                temp = []
                for x in days_vars:
                    if x.get():
                        temp.append(x.get())
                new_emp.days = temp
                new_emp.status = entries[10].get().strip().capitalize() if entries[
                    10].get().strip().capitalize() else "not mentioned"
                new_emp.salary = entries[11].get().strip()
                new_emp.workspace = entries[12].get().strip().capitalize() if entries[
                    12].get().strip().capitalize() else "not mentioned"
                new_emp.position = entries[13].get().strip().capitalize() if entries[
                    13].get().strip() else "not mentioned"
                new_emp.rate = entries[14].get()
                if "not mentioned" not in (path_labels[0].cget("text"),
                                           path_labels[1].cget("text"),
                                           path_labels[2].cget("text"),
                                           path_labels[3].cget("text"),
                                           path_labels[4].cget("text")):
                    new_emp.photo = path_labels[0].cget("text")
                    new_emp.docs = {"passport": path_labels[1].cget("text"),
                                    "graduation": path_labels[1].cget("text"),
                                    "medcard": path_labels[3].cget("text"),
                                    "mil_accounting": path_labels[4].cget("text")}
                else:
                    raise ValueError("All documents and photo required")
                new_emp.staff_id = Application.generate_id([i.staff_id for i in self.employees])
                self.employees.append(new_emp)
                self.render_employees(employees_frame, filter_drop_down.get(), search_entry.get())
                self.__admin.action_history = Action("HIRE",
                                                     f"User {self.__admin.staff_id} hired the employee {
                                                     new_emp.staff_id}", self.__admin.staff_id, datetime.strftime(
                        datetime.now(), "%d.%m.%Y %H:%M"))
                self.render_actions(self.recent_actions, True)
                self.render_actions(self.tabs.tab("History").winfo_children()[0])
                CTkMessagebox(self, message="The new employee was hired", title="Success", icon="check")
                self.on_close(new_window)
                # except Exception as e:
                #     CTkMessagebox(new_window, message=str(e), title="Error", icon="cancel")

            new_window = CTk()
            self.opened_windows.append(new_window)
            new_window.iconbitmap('DB/public/hr_software_icon.ico')
            new_window.configure(fg_color=("#F7F7F2", "#131200"))
            new_window.title("Change")
            new_window.geometry("1000x500+0+0")
            new_window.minsize(700, 500)

            chng_profile_frame = CTkScrollableFrame(new_window, fg_color="transparent",
                                                    scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                                    scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
            chng_profile_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

            properties = ["Name:", "Age:", "Gender:", "Phone:", "Email:", "Address:", "Hire date:", "Seniority:",
                          "Next vacation:", "Days:", "Status:", "Salary:", "Workspace:", "Position:", "Rate:",
                          "Photo:", "Passport:", "Graduation:", "Medical card:", "Military accounting:"]
            path_labels = []
            entries = []
            row = 0
            for prop in properties:
                label = CTkLabel(chng_profile_frame, text=prop, font=('Arial', 18), text_color=("black", "white"),
                                 fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
                label.grid(row=row, column=0, pady=4, sticky="w")
                if row < 15:
                    if row == 2:
                        sex_var = IntVar(value=0)
                        sex_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                        sex_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        male_btn = CTkRadioButton(sex_wrapper, text="Male", font=('Arial', 18), variable=sex_var,
                                                  value=0)
                        male_btn.grid(row=0, column=0)
                        female_btn = CTkRadioButton(sex_wrapper, text="Female", font=('Arial', 18), value=1,
                                                    variable=sex_var)
                        female_btn.grid(row=0, column=1)
                        entries.append(sex_wrapper)
                    elif row == 6:
                        hdate_picker = DateEntry(chng_profile_frame, font=('Arial', 18), justify=CENTER,
                                                 text_color=("black", "white"),
                                                 width=12, height=40,
                                                 date_pattern='dd.mm.yyyy',
                                                 year=self.today.year,
                                                 month=self.today.month,
                                                 day=self.today.day,
                                                 maxdate=self.today)
                        hdate_picker.bind("<<DateEntrySelected>>",
                                          lambda x: Application.on_hdate_change(hdate_picker, next_vacation_picker))
                        hdate_picker.grid(row=row, column=1, padx=10, sticky="w")
                        entries.append(hdate_picker)
                    elif row == 8:
                        next_vacation_picker = DateEntry(chng_profile_frame, font=('Arial', 18), justify=CENTER,
                                                         width=12, height=40, text_color=("black", "white"),
                                                         date_pattern='dd.mm.yyyy',
                                                         year=self.today.year+1,
                                                         month=self.today.month,
                                                         day=self.today.day,
                                                         mindate=date(self.today.year, self.today.month,
                                                                      self.today.day + 1))
                        next_vacation_picker.grid(row=row, column=1, padx=10, sticky="w")
                        entries.append(next_vacation_picker)
                    elif row == 9:
                        days_vars = []
                        days_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                        days_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                        column = 0
                        for day in days:
                            days_vars.append(StringVar(value=""))
                            radio = CTkCheckBox(days_wrapper, text=day, font=('Arial', 18),
                                                variable=days_vars[column],
                                                onvalue=day, offvalue="", text_color=("black", "white"))
                            radio.grid(row=0, column=column)
                            column += 1
                        entries.append(days_wrapper)
                    elif row == 14:
                        spinbox = tk.Spinbox(chng_profile_frame, justify=CENTER, from_=0, to=10, width=4,
                                             font=("Arial", 18), state="readonly")
                        spinbox.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        entries.append(spinbox)
                    else:
                        entry = CTkEntry(chng_profile_frame, width=500, height=40, font=("Arial", 18),
                                         text_color=("black", "white"))
                        if row == 10:
                            entry.insert(0, "normal")
                        entry.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        entries.append(entry)
                else:
                    path_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                    path_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                    path_label = CTkLabel(path_wrapper, text="Not menitoned", font=('Arial', 18), wraplength=300,
                                          text_color=("black", "white"),
                                          fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
                    path_label.grid(row=0, column=0)
                    path_labels.append(path_label)
                    path_copier = CTkButton(path_wrapper, text="Copy", width=130, height=40, font=("Arial", 18),
                                            command=lambda x=path_label: pyperclip.copy(x.cget("text")),
                                            corner_radius=10,
                                            fg_color=("#C5D86D", "#BBD5ED"), hover_color=("#B8D04E", "#9EC3E5"),
                                            text_color="black")
                    path_chooser = CTkButton(path_wrapper, text="Change", width=130, height=40, font=("Arial", 18),
                                             command=lambda x=path_label, y=path_copier: Application.choose_file(x, y),
                                             corner_radius=10,
                                             fg_color=("#C5D86D", "#BBD5ED"), hover_color=("#B8D04E", "#9EC3E5"),
                                             text_color="black")
                    path_chooser.grid(row=0, column=1, padx=10)
                    path_copier.grid(row=0, column=2, padx=10)
                    entries.append(path_wrapper)
                row += 1
            add_btn = CTkButton(new_window, text="Add", width=200, height=40, font=("Arial", 18),
                                fg_color=("#C5D86D", "#BBD5ED"),
                                command=add_employee, corner_radius=10, hover_color=("#B8D04E", "#9EC3E5"),
                                text_color="black")
            add_btn.pack(padx=10, pady=10)

            new_window.protocol("WM_DELETE_WINDOW", lambda x=new_window: self.on_close(x))
            new_window.mainloop()

        top_actions = CTkFrame(self.tabs.tab("Employees"), fg_color="transparent", width=1025)
        top_actions.pack(padx=10)
        search_wrapper = CTkFrame(top_actions, fg_color="transparent")
        search_wrapper.pack(side="left")

        search_entry = CTkEntry(search_wrapper, width=400, height=40,
                                placeholder_text="Search by ID or name...", corner_radius=10)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", lambda x: update_list())
        filter_drop_down = CTkOptionMenu(search_wrapper, width=150, height=40, fg_color=("#C5D86D", "#BBD5ED"),
                                         dropdown_fg_color=("#C5D86D", "#BBD5ED"),
                                         dropdown_hover_color=("#B8D04E", "#9EC3E5"),
                                         corner_radius=10, bg_color="transparent", text_color="black",
                                         dropdown_text_color="black", button_color=("#B8D04E", "#9EC3E5"),
                                         button_hover_color=("#B8D04E", "#9EC3E5"),
                                         values=["Hire date ↓", "Hire date ↑", "Age ↓", "Age ↑", "Seniority ↓",
                                                 "Seniority ↑",
                                                 "Next vacation ↓", "Next vacation ↑", "Salary ↓", "Salary ↑"],
                                         command=lambda x: update_list)
        filter_drop_down.pack(padx=10, side="right")

        add_emp_btn = CTkButton(top_actions, width=100, height=40, text="Add +", hover_color=("#B8D04E", "#9EC3E5"),
                                fg_color=("#C5D86D", "#BBD5ED"), corner_radius=10, text_color="black",
                                command=add_emp)
        add_emp_btn.pack(side="right")

        employees_frame = CTkScrollableFrame(self.tabs.tab("Employees"), fg_color="transparent",
                                             scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                             scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
        employees_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.render_employees(employees_frame, filter_drop_down.get(), "")

    def render_actions(self, master, minify=False) -> None:
        """
        Відмальовує картки подій у фреймі master. Якщо minify є True, то створиться тільки три картки.
        :param master: Батьківский фрейм
        :param minify: Переключатель між розширеною та зменшеною формою списку подій
        :return: None
        """
        count = 0
        for i in master.winfo_children():
            i.destroy()
        if not self.__admin.action_history:
            label = CTkLabel(master, text="No actions", font=('Arial', 18), text_color=("black", "white"),
                             fg_color="transparent", bg_color=("#E4E6C3", "#496A81"))
            label.pack(pady=10, side=TOP)
            return
        for action in self.__admin.action_history[::-1]:
            if minify:
                count += 1
                if count > 3:
                    break
            action_frame = CTkFrame(master, fg_color=("#F7F7F2", "#0A2239"), bg_color=("#E4E6C3", "#496A81"),
                                    width=1000, corner_radius=10)
            action_frame.pack(pady=5, fill="x", expand=True)
            action_info = CTkFrame(action_frame, fg_color="transparent")
            action_info.pack(padx=16, side="left")
            action_name = CTkLabel(action_info, text=action.action_name, font=('Arial', 20),
                                   text_color=("black", "white"),
                                   fg_color="transparent", bg_color=("#F7F7F2", "#0A2239"))
            action_name.grid(row=0, column=0, pady=7, sticky="sw")
            action_creator = CTkLabel(action_info, text=self.__admin.name, font=('Arial', 16),
                                      text_color=("black", "white"),
                                      fg_color="transparent", bg_color=("#F7F7F2", "#0A2239"))
            action_creator.grid(row=1, column=0, sticky="w")
            action_date = CTkLabel(action_info, text=action.date_of_creating, font=('Arial', 16),
                                   text_color=("black", "white"),
                                   fg_color="transparent", bg_color=("#F7F7F2", "#0A2239"))
            action_date.grid(row=2, column=0, pady=7, sticky="nw")
            action_description = CTkLabel(action_frame, text=action.describe, font=('Arial', 16), wraplength=500,
                                          text_color=("black", "white"),
                                          fg_color="transparent", bg_color=("#F7F7F2", "#0A2239"))
            action_description.pack(padx=16, side="right")

    def sort_employees(self, prop_filter: str, start_symbols=None) -> list:
        """
        Сортує список працівників за певним фільтром та початковими символами.
        :param prop_filter: Властивість, за якою фільтрується список
        :param start_symbols: Початкові символи, за якими фільтрується список
        :return: list
        """
        if not self.users["employees"]:
            return []
        temp = []
        if start_symbols is not None:
            if start_symbols == "":
                temp = self.employees
            elif start_symbols[0] in list(string.ascii_letters) + list(
                    "абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"):
                for emp in self.employees:
                    if start_symbols in emp.name:
                        temp.append(emp)
            elif start_symbols[0] in list(string.digits):
                for emp in self.employees:
                    if start_symbols in emp.staff_id:
                        temp.append(emp)
            else:
                temp = self.employees
        else:
            temp = self.employees
        match prop_filter:
            case "Hire date ↓":
                temp = temp[::-1]
            case "Seniority ↓":
                temp = sorted(temp, key=lambda x: int(x.seniority), reverse=True)
            case "Seniority ↑":
                temp = sorted(temp, key=lambda x: int(x.seniority))
            case "Age ↓":
                temp = sorted(temp, key=lambda x: int(x.age), reverse=True)
            case "Age ↑":
                temp = sorted(temp, key=lambda x: int(x.age))
            case "Next vacation ↓":
                temp = sorted(temp, key=lambda x: x.next_vacation, reverse=True)
            case "Next vacation ↑":
                temp = sorted(temp, key=lambda x: x.next_vacation)
            case "Salary ↓":
                temp = sorted(temp, key=lambda x: int(x.salary), reverse=True)
            case "Salary ↑":
                temp = sorted(temp, key=lambda x: int(x.salary))
            case _:
                pass
        return temp

    def render_employees(self, master, prop_filter: str, start_symbols: str) -> None:
        """
        Відмальовує картки працівників.
        :param master: Батьківський фрейм
        :param prop_filter: Властивість, за якою фільтрується список
        :param start_symbols: Початкові символи, за якими фільтрується список
        :return: None
        """

        def fire_emp(emp, parent_element) -> None:
            """
            Видаляє об'єкт працівника зі списку.
            :param emp: об'єкт (працівник)
            :param parent_element: батьківський елемент (потрібен для закривання вікна)
            :return: None
            """
            confirm = CTkMessagebox(self, title="Confirm",
                                    message=f"Do you want to fire employee {emp.staff_id} - {emp.name}?",
                                    options=["Yes", "No"], icon="question")
            if confirm.get() == "Yes":
                self.employees.remove(emp)
                self.render_employees(master, prop_filter, start_symbols)
                CTkMessagebox(self, title="Success", message="Employess was deleted", icon="check")
                self.opened_windows.remove(parent_element)
                parent_element.destroy()
                self.__admin.action_history = Action("FIRE",
                                                     f"User {
                                                     self.__admin.staff_id} fired employee {emp.staff_id}",
                                                     self.__admin.staff_id, None)
                self.render_actions(self.recent_actions, True)
                self.render_actions(self.tabs.tab("History").winfo_children()[0])

        def change_emp_info(emp) -> None:
            """
            Створює вікно з формою.
            :param emp: Об'єкт (працівник), в якого була викликана ця функція
            :return: None
            """

            def save_emp_changes() -> None:
                """
                Витягує дані з форми, і вставляє їх у відповідні властивості об'єкту emp (працівника).
                :return: None
                """
                try:
                    if entries[0].get().strip().replace(" ", "").isalpha():
                        emp.name = entries[0].get().strip().title()
                    else:
                        raise ValueError("Name must be alphabetic")
                    emp.age = entries[1].get().strip()
                    emp.sex = "Male" if not sex_var.get() else "Female"
                    emp.phone = entries[3].get().strip()
                    emp.email = entries[4].get().strip()
                    emp.address = entries[5].get().strip()
                    emp.hdate = entries[6].get()
                    emp.seniority = entries[7].get().strip()
                    if datetime.strptime(entries[8].get(), "%d.%m.%Y") > emp.hdate:
                        emp.next_vacation = entries[8].get()
                    else:
                        raise ValueError(
                            "The date of the next vacation cannot coincide with or be earlier than the date of hire")
                    temp = []
                    for x in days_vars:
                        if x.get():
                            temp.append(x.get())
                    emp.days = temp
                    emp.status = entries[10].get().strip().capitalize() if entries[
                        10].get().strip().capitalize() else "not mentioned"
                    emp.salary = entries[11].get().strip()
                    emp.workspace = entries[12].get().strip().capitalize() if entries[
                        12].get().strip().capitalize() else "not mentioned"
                    emp.position = entries[13].get().strip().capitalize() if entries[
                        13].get().strip() else "not mentioned"
                    emp.rate = spinvar.get()
                    emp.photo = path_labels[0].cget("text")
                    if "not mentioned" not in (path_labels[0].cget("text"),
                                               path_labels[1].cget("text"),
                                               path_labels[2].cget("text"),
                                               path_labels[3].cget("text"),
                                               path_labels[4].cget("text")):
                        emp.photo = path_labels[0].cget("text")
                        emp.docs = {"passport": path_labels[1].cget("text"),
                                    "graduation": path_labels[1].cget("text"),
                                    "medcard": path_labels[3].cget("text"),
                                    "mil_accounting": path_labels[4].cget("text")}
                    else:
                        raise ValueError("All documents and photo required")
                    employee_description.configure(text=f"Name: {emp.name};\n"
                                                        f"ID: {emp.staff_id};\n"
                                                        f"Age: {emp.age};\n"
                                                        f"Phone: {emp.phone};\n"
                                                        f"Email: {emp.email};\n"
                                                        f"Address: {emp.address if emp.address else "not mentioned"};"
                                                        f"Seniority: {emp.seniority};\n"
                                                        f"Hire date: {datetime.strftime(emp.hdate, "%d.%m.%Y")};\n"
                                                        f"Salary: {int(emp.salary):.2f};")
                    image.close()
                    new_image = Image.open(emp.photo)
                    resized_new_image = Application.crop_center(new_image, (300, 400))
                    ctk_new_image = CTkImage(light_image=resized_new_image, dark_image=resized_new_image,
                                             size=(200, 300))
                    employee_image.configure(image=ctk_new_image)
                    employee_image.image = ctk_new_image
                    self.__admin.action_history = Action("CHANGE",
                                                         f"User {self.__admin.staff_id} changed profile of user {
                                                         emp.staff_id}",
                                                         emp.staff_id,
                                                         datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M"))
                    self.render_actions(self.recent_actions, True)
                    self.render_actions(self.tabs.tab("History").winfo_children()[0])
                    CTkMessagebox(self, message="Profile was changed", title="Success", icon="check")
                    self.on_close(new_window)
                except Exception as e:
                    CTkMessagebox(self, message=str(e), title="Error", icon="cancel")

            new_window = CTk()
            self.opened_windows.append(new_window)
            new_window.iconbitmap('DB/public/hr_software_icon.ico')
            new_window.configure(fg_color=("#F7F7F2", "#131200"))
            new_window.title("Change")
            new_window.geometry("1000x500+0+0")
            new_window.minsize(700, 500)

            chng_profile_frame = CTkScrollableFrame(new_window, fg_color="transparent",
                                                    scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                                    scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
            chng_profile_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

            properties = ["Name:", "Age:", "Gender:", "Phone:", "Email:", "Address:", "Hire date:", "Seniority:",
                          "Next vacation:", "Days:", "Status:", "Salary:", "Workspace:", "Position:", "Rate:", "Photo:",
                          "Passport:", "Graduation:", "Medical card:", "Military accounting:"]
            path_labels = []
            values = [
                emp.name,
                emp.age,
                emp.sex,
                emp.phone,
                emp.email,
                emp.address,
                emp.hdate,
                emp.seniority,
                emp.next_vacation,
                emp.days,
                emp.status,
                emp.salary,
                emp.workspace,
                emp.position,
                emp.rate,
                emp.photo,
                emp.docs["passport"],
                emp.docs["graduation"],
                emp.docs["medcard"],
                emp.docs["mil_accounting"]
            ]
            entries = []
            row = 0
            for prop in properties:
                label = CTkLabel(chng_profile_frame, text=prop, font=('Arial', 18), text_color=("black", "white"),
                                 fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
                label.grid(row=row, column=0, pady=4, sticky="w")
                if row < 15:
                    if row == 2:
                        sex_var = IntVar(value=(0 if values[row] == "Male" else 1))
                        sex_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                        sex_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        male_btn = CTkRadioButton(sex_wrapper, text="Male", font=('Arial', 18), variable=sex_var,
                                                  value=0)
                        male_btn.grid(row=0, column=0)
                        female_btn = CTkRadioButton(sex_wrapper, text="Female", font=('Arial', 18), value=1,
                                                    variable=sex_var)
                        female_btn.grid(row=0, column=1)
                        entries.append(sex_wrapper)
                    elif row == 6:
                        hdate_picker = DateEntry(chng_profile_frame, font=('Arial', 18), justify=CENTER,
                                                 text_color=("black", "white"),
                                                 width=12, height=40,
                                                 date_pattern='dd.mm.yyyy',
                                                 year=values[row].year if values[row].year else self.today.year,
                                                 month=values[row].month if values[row].month else self.today.month,
                                                 day=values[row].day if values[row].day else self.today.day,
                                                 maxdate=self.today)
                        hdate_picker.bind("<<DateEntrySelected>>",
                                          lambda x: Application.on_hdate_change(hdate_picker, next_vacation_picker))
                        hdate_picker.grid(row=row, column=1, padx=10, sticky="w")
                        entries.append(hdate_picker)
                    elif row == 8:
                        next_vacation_picker = DateEntry(chng_profile_frame, font=('Arial', 18), justify=CENTER,
                                                         width=12, height=40, text_color=("black", "white"),
                                                         date_pattern='dd.mm.yyyy',
                                                         year=values[row].year + 1 if values[
                                                             row].year else self.today.year,
                                                         month=values[row].month if values[
                                                             row].month else self.today.month,
                                                         day=values[row].day if values[row].day else self.today.day,
                                                         mindate=date(values[row].year, values[row].month,
                                                                      values[row].day))
                        next_vacation_picker.grid(row=row, column=1, padx=10, sticky="w")
                        entries.append(next_vacation_picker)
                    elif row == 9:
                        days_vars = []
                        days_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                        days_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                        column = 0
                        for day in days:
                            days_vars.append(StringVar(value=("" if day not in values[row] else day)))
                            radio = CTkCheckBox(days_wrapper, text=day, font=('Arial', 18),
                                                variable=days_vars[column],
                                                onvalue=day, offvalue="", text_color=("black", "white"))
                            radio.grid(row=0, column=column)
                            column += 1
                        entries.append(days_wrapper)
                    elif row == 14:
                        spinvar = tk.StringVar()
                        spinbox = tk.Spinbox(chng_profile_frame, justify=CENTER, from_=0, to=10,
                                             width=4, font=("Arial", 18), textvariable=spinvar, state="readonly")
                        spinbox.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        spinvar.set(str(values[row]))
                        entries.append(spinbox)
                    else:
                        entry = CTkEntry(chng_profile_frame, width=500, height=40, font=("Arial", 18),
                                         text_color=("black", "white"))
                        entry.insert(0, str(values[row]))
                        entry.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                        entries.append(entry)
                else:
                    path_wrapper = CTkFrame(chng_profile_frame, fg_color="transparent")
                    path_wrapper.grid(row=row, column=1, pady=4, padx=10, sticky="w")
                    path_label = CTkLabel(path_wrapper, text=values[row], font=('Arial', 18), wraplength=300,
                                          text_color=("black", "white"),
                                          fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
                    path_label.grid(row=0, column=0)
                    path_labels.append(path_label)
                    path_copier = CTkButton(path_wrapper, text="Copy", width=130, height=40, font=("Arial", 18),
                                            command=lambda x=path_label: pyperclip.copy(x.cget("text")),
                                            corner_radius=10,
                                            fg_color=("#C5D86D", "#BBD5ED"), hover_color=("#B8D04E", "#9EC3E5"),
                                            text_color="black")
                    path_chooser = CTkButton(path_wrapper, text="Change", width=130, height=40, font=("Arial", 18),
                                             command=lambda x=path_label, y=path_copier: Application.choose_file(x, y),
                                             corner_radius=10,
                                             fg_color=("#C5D86D", "#BBD5ED"), hover_color=("#B8D04E", "#9EC3E5"),
                                             text_color="black")
                    path_chooser.grid(row=0, column=1, padx=10)
                    path_copier.grid(row=0, column=2, padx=10)
                    entries.append(path_wrapper)
                row += 1
            save_btn = CTkButton(new_window, text="Save", width=200, height=40, font=("Arial", 18),
                                 fg_color=("#C5D86D", "#BBD5ED"),
                                 command=save_emp_changes, corner_radius=10, hover_color=("#B8D04E", "#9EC3E5"),
                                 text_color="black")
            save_btn.pack(padx=10, pady=10)

            new_window.protocol("WM_DELETE_WINDOW", lambda x=new_window: self.on_close(x))
            new_window.mainloop()

        def show_emp_details(emp) -> None:
            """
            Створює вікно з розширеною інформацією про працівника.
            :param emp: Об'єкт (працівник)
            :return: none
            """

            def add_new_duty(duty: str) -> None:
                """
                Зчитує новий обов'язок з поля duty_entry, і додає його до списку обов'язків працівника.
                :param duty: Новий обов'язок
                :return: None
                """
                try:
                    emp.duties = duty
                    duties_label.configure(text="Duties")
                    duties.configure(text=emp.show_duties())
                    duty_entry.delete(0, END)
                    self.__admin.action_history = Action("CHANGE",
                                                         f"User {
                                                         self.__admin.staff_id} added duty to employee {emp.staff_id}",
                                                         self.__admin.staff_id,
                                                         None)
                    self.render_actions(self.recent_actions, True)
                    self.render_actions(self.tabs.tab("History").winfo_children()[0])
                except Exception as e:
                    duties_label.configure(text=str(e))

            def delete_duty(num_of_duty: str) -> None:
                """
                Видаляє обов'язок зі списку обов'язків працівника
                :param num_of_duty: номер обов'язку
                :return: None
                """
                if not num_of_duty.strip().isdigit() or len(num_of_duty.strip()) != 1:
                    duties_label.configure(text="Input a number of duty!")
                    return
                duties_label.configure(text="Duties")
                num_of_duty = int(num_of_duty)
                try:
                    emp.remove_duty(num_of_duty - 1)
                except Exception as e:
                    duties_label.configure(text=str(e))
                    return
                duty_entry.delete(0, END)
                self.__admin.action_history = Action("CHANGE",
                                                     f"User {
                                                     self.__admin.staff_id} removed duty to employee {emp.staff_id}",
                                                     self.__admin.staff_id,
                                                     None)
                self.render_actions(self.recent_actions, True)
                self.render_actions(self.tabs.tab("History").winfo_children()[0])
                duties.configure(text=emp.show_duties())

            new_window = CTk()
            self.opened_windows.append(new_window)
            new_window.configure(fg_color=("#F7F7F2", "#131200"))
            new_window.title("Employee details")
            new_window.iconbitmap('DB/public/hr_software_icon.ico')
            new_window.resizable(False, False)
            new_window.geometry("600x600")
            show_details_frame = CTkScrollableFrame(new_window, fg_color="transparent",
                                                    scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                                    scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
            show_details_frame.pack(fill=BOTH, expand=True)

            emp_info_label = CTkLabel(show_details_frame,
                                      text=emp.show_info(),
                                      font=('Arial', 18), justify=LEFT, text_color=("black", "white"),
                                      fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
            emp_info_label.pack(pady=10)

            chng_btn = CTkButton(show_details_frame, width=200, height=40, text="Change",
                                 fg_color=("#C5D86D", "#BBD5ED"),
                                 hover_color=("#B8D04E", "#9EC3E5"), corner_radius=10, text_color="black",
                                 font=('Arial', 18),
                                 command=lambda: change_emp_info(emp))
            chng_btn.pack(pady=10)

            documents_label = CTkLabel(show_details_frame, text="Documents", font=('Arial', 20),
                                       text_color=("black", "white"),
                                       fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
            documents_label.pack(pady=10)

            documents_frame = CTkFrame(show_details_frame, fg_color="transparent")
            documents_frame.pack()
            emp.show_docs(documents_frame)

            duties_label = CTkLabel(show_details_frame, text="Duties", font=('Arial', 20),
                                    text_color=("black", "white"),
                                    fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
            duties_label.pack(pady=10)

            duties = CTkLabel(show_details_frame, text=emp.show_duties(), font=('Arial', 18),
                              text_color=("black", "white"),
                              fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
            duties.pack()

            chng_duties_wrapper = CTkFrame(show_details_frame, fg_color="transparent")
            chng_duties_wrapper.pack(pady=10)

            duty_entry = CTkEntry(chng_duties_wrapper, font=('Arial', 18),
                                  placeholder_text="Enter new dutie or number of dutie to delete", width=400,
                                  height=40)
            duty_actions = CTkFrame(chng_duties_wrapper, fg_color="transparent")
            add_duty = CTkButton(duty_actions, width=100, height=40, text="Add", fg_color=("#C5D86D", "#BBD5ED"),
                                 hover_color=("#B8D04E", "#9EC3E5"), text_color="black", corner_radius=10,
                                 command=lambda: add_new_duty(duty_entry.get()))
            del_duty = CTkButton(duty_actions, width=100, height=40, text="Delete", fg_color=("#C5D86D", "#BBD5ED"),
                                 hover_color=("#B8D04E", "#9EC3E5"), text_color="black", corner_radius=10,
                                 command=lambda: delete_duty(duty_entry.get()))
            duty_entry.pack()
            duty_actions.pack(pady=7)
            add_duty.pack(padx=5, side="left")
            del_duty.pack(padx=5, side="right")

            fire_btn = CTkButton(show_details_frame, width=150, height=40, text="Fire", fg_color="orange red",
                                 hover_color="red", text_color="white",
                                 command=lambda: fire_emp(emp, new_window), corner_radius=10,
                                 font=("Arial", 18))
            fire_btn.pack(pady=30)

            new_window.protocol("WM_DELETE_WINDOW", lambda x=new_window: self.on_close(x))
            new_window.mainloop()

        list_of_emps = self.sort_employees(prop_filter, start_symbols)

        for i in master.winfo_children():
            i.destroy()

        if not list_of_emps:
            label = CTkLabel(master, text="No employees", font=('Arial', 18), text_color=("black", "white"),
                             fg_color="transparent", bg_color=("#E4E6C3", "#496A81"))
            label.pack(pady=10)
            return

        for employee in list_of_emps:
            employee_frame = CTkFrame(master, fg_color=("#F7F7F2", "#0A2239"), bg_color=("#E4E6C3", "#496A81"))
            employee_frame.pack(fill="x", expand=True, pady=5)
            employee_info = CTkFrame(employee_frame, fg_color="transparent")
            employee_info.pack(padx=10, pady=10, side="left")
            image = Image.open(employee.photo)
            resized_image = Application.crop_center(image, (200, 300))
            ctk_image = CTkImage(light_image=resized_image, dark_image=resized_image, size=(200, 300))
            employee_image = CTkLabel(employee_info, text="", image=ctk_image)
            employee_image.pack(side="left")
            employee_description = CTkLabel(employee_info, text=f"Name: {employee.name};\n"
                                                                f"ID: {employee.staff_id};\n"
                                                                f"Age: {employee.age};\n"
                                                                f"Phone: {employee.phone};\n"
                                                                f"Email: {employee.email};\n"
                                                                f"Address: {employee.address if employee.address else "not mentioned"};\n"
                                                                f"Seniority: {employee.seniority};\n"
                                                                f"Hire date: {datetime.strftime(employee.hdate, "%d.%m.%Y")};\n"
                                                                f"Salary: {float(employee.salary):.2f};",
                                            font=('Arial', 20), justify=LEFT, text_color=("black", "white"),
                                            fg_color="transparent", bg_color=("#F7F7F2", "#0A2239"))
            employee_description.pack(side="right", padx=10)
            employee_actions = CTkFrame(employee_frame, fg_color="transparent")
            employee_actions.pack(side="right", pady=10, padx=10)
            show_details = CTkButton(employee_actions, width=150, height=40, text="Show details",
                                     command=lambda x=employee: show_emp_details(x),
                                     font=('Arial', 18), corner_radius=10, text_color="black",
                                     fg_color=("#C5D86D", "#BBD5ED"), hover_color=("#B8D04E", "#9EC3E5"))
            show_details.pack(pady=5)
            change_btn = CTkButton(employee_actions, width=150, height=40, text="Change",
                                   command=lambda x=employee: change_emp_info(x),
                                   font=('Arial', 18), corner_radius=10, text_color="black",
                                   fg_color=("#C5D86D", "#BBD5ED"), hover_color=("#B8D04E", "#9EC3E5"))
            change_btn.pack(pady=5)

    def create_projects_tab(self) -> None:
        """
        Створює вкладку з проектами.
        :return: None
        """

        def update_projects_list() -> None:
            """
            Перехоплює зміну фільтра або ввід символів у пошук,
            і запускає перемалювання списку проектів.
            :return: None
            """
            self.render_projects(projects_frame, filter_drop_down.get(), search_entry.get())

        def add_project() -> None:
            """
            Створює нове вікно з формою для створення нового проекту.
            :return: None
            """

            def add() -> None:
                """
                Витягує дані з форми, створює новий об'єкт Project і заповняє його.
                :return: None
                """
                try:
                    if entries[0].get().strip().isalnum():
                        name = entries[0].get().strip().capitalize()
                    else:
                        raise ValueError("Name must be alpha-numeric")
                    if entries[1].get().strip():
                        description = entries[1].get().strip()
                    else:
                        raise ValueError("Description can't be empty")
                    if name in [i.name.capitalize for i in self.__admin.projects]:
                        raise IndexError("This project already exists")
                    self.__admin.projects = Project(name, description, datetime.strftime(self.today, "%d.%m.%Y"),
                                                    deadline_chooser.get(), importance_chooser.get(), 0)
                    self.render_projects(self.tabs.tab("Projects"), filter_drop_down.get(), search_entry.get())
                    self.__admin.action_history = Action("CREATE",
                                                         f"User {self.__admin.staff_id} created new project {name}",
                                                         self.__admin.staff_id, datetime.strftime(datetime.now(),
                                                                                                  "%d.%m.%Y %H:%M"))
                    self.render_actions(self.recent_actions, True)
                    self.render_actions(self.tabs.tab("History").winfo_children()[0])
                    self.on_close(new_window)
                    CTkMessagebox(self, message="Project was created", title="Success", icon="check")
                except Exception as e:
                    CTkMessagebox(new_window, message=str(e), title="Error", icon="cancel")

            new_window = CTk()
            new_window.title("Create project")
            new_window.configure(fg_color=("#F7F7F2", "#131200"))
            new_window.iconbitmap('DB/public/hr_software_icon.ico')
            new_window.geometry("700x300+200+0")
            new_window.minsize(700, 300)
            self.opened_windows.append(new_window)

            content = CTkScrollableFrame(new_window, fg_color="transparent",
                                         scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                         scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
            content.pack(fill=BOTH, expand=True)

            properties = ["Name:", "Description:", "Deadline:", "Importance:"]
            entries = []

            row = 0
            for prop in properties:
                label = CTkLabel(content, text=prop, font=('Arial', 18), text_color=("black", "white"),
                                 fg_color="transparent", bg_color=("#F7F7F2", "#131200"))
                label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
                if row == 2:
                    deadline_chooser = DateEntry(content, font=('Arial', 18), justify=CENTER,
                                                 text_color=("black", "white"),
                                                 width=12, height=40,
                                                 date_pattern='dd.mm.yyyy',
                                                 year=self.today.year + 1,
                                                 month=self.today.month,
                                                 day=self.today.day,
                                                 mindate=self.today)
                    deadline_chooser.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                    entries.append(deadline_chooser)
                elif row == 3:
                    importance_chooser = CTkOptionMenu(content, width=150, height=40, text_color="black",
                                                       dropdown_text_color="black",
                                                       fg_color=("#C5D86D", "#BBD5ED"),
                                                       dropdown_fg_color=("#C5D86D", "#BBD5ED"),
                                                       dropdown_hover_color=("#B8D04E", "#9EC3E5"),
                                                       button_color=("#B8D04E", "#9EC3E5"),
                                                       button_hover_color=("#B8D04E", "#9EC3E5"),
                                                       corner_radius=10,
                                                       values=["Low", "Medium", "High"], font=('Arial', 18))
                    importance_chooser.grid(row=row, column=1, pady=5, sticky="w", padx=10)
                    entries.append(importance_chooser)
                else:
                    entry = CTkEntry(content, font=('Arial', 18), width=450, height=40, corner_radius=10)
                    entry.grid(row=row, column=1, sticky="w", padx=10, pady=5)
                    entries.append(entry)
                row += 1
            add_btn = CTkButton(new_window, width=150, height=40, fg_color=("#C5D86D", "#BBD5ED"),
                                text="Create project",
                                hover_color=("#B8D04E", "#9EC3E5"), corner_radius=10, text_color="black",
                                command=add, font=("Arial", 18))
            add_btn.pack(pady=20)
            new_window.mainloop()

        top_actions = CTkFrame(self.tabs.tab("Projects"), fg_color="transparent", width=1025)
        top_actions.pack(padx=10)
        search_wrapper = CTkFrame(top_actions, fg_color="transparent")
        search_wrapper.pack(side="left")

        search_entry = CTkEntry(search_wrapper, width=400, height=40,
                                placeholder_text="Search by name...", corner_radius=10)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", lambda x: update_projects_list())
        filter_drop_down = CTkOptionMenu(search_wrapper, width=150, height=40, text_color="black",
                                         dropdown_text_color="black",
                                         fg_color=("#C5D86D", "#BBD5ED"),
                                         dropdown_fg_color=("#C5D86D", "#BBD5ED"),
                                         dropdown_hover_color=("#B8D04E", "#9EC3E5"),
                                         button_color=("#B8D04E", "#9EC3E5"),
                                         button_hover_color=("#B8D04E", "#9EC3E5"),
                                         corner_radius=10,
                                         values=["Date of start ↓", "Date of start ↑", "Date of end ↓", "Date of end ↑",
                                                 "Importance ↓", "Importance ↑", "Execute ↓", "Execute ↑"],
                                         command=lambda x: update_projects_list)
        filter_drop_down.pack(padx=10, side="right")

        add_emp_btn = CTkButton(top_actions, width=100, height=40, text="Add +", hover_color=("#B8D04E", "#9EC3E5"),
                                fg_color=("#C5D86D", "#BBD5ED"), corner_radius=10, text_color="black",
                                command=add_project)
        add_emp_btn.pack(side="right")

        projects_frame = CTkScrollableFrame(self.tabs.tab("Projects"), fg_color="transparent",
                                            scrollbar_button_color=("#C5D86D", "#BBD5ED"),
                                            scrollbar_button_hover_color=("#B8D04E", "#9EC3E5"))
        projects_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.render_projects(projects_frame, filter_drop_down.get(), "")

    def sort_projects(self, prop_filter: str, start_symbols: str) -> list:
        """
        Сортує список проектів за властивістю prop_filter та за початковими символами start_symbols.
        :param prop_filter: Властивість, за якою фільтрується список
        :param start_symbols: Початкові символи, за якими фільтрується список
        :return: list
        """
        if not self.__admin.projects:
            return []
        temp = []
        if start_symbols is not None:
            if start_symbols == "":
                temp = self.__admin.projects
            elif start_symbols[0] in list(string.ascii_letters) + list(
                    "абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"):
                for emp in self.__admin.projects:
                    if start_symbols in emp.name:
                        temp.append(emp)
            else:
                temp = self.__admin.projects
        else:
            temp = self.__admin.projects
        match prop_filter:
            case "Date of start ↓":
                temp = temp[::-1]
            case "Date of end ↓":
                temp = sorted(temp, key=lambda x: x.date_of_end, reverse=True)
            case "Date of end ↑":
                temp = sorted(temp, key=lambda x: x.date_of_end)
            case "Importance ↓":
                important_projects = [i for i in self.__admin.projects if i.importance == "High"]
                medium_projects = [i for i in self.__admin.projects if i.importance == "Medium"]
                low_projects = [i for i in self.__admin.projects if i.importance == "Low"]
                temp = low_projects + medium_projects + important_projects
                temp.reverse()
            case "Importance ↑":
                important_projects = [i for i in self.__admin.projects if i.importance == "High"]
                medium_projects = [i for i in self.__admin.projects if i.importance == "Medium"]
                low_projects = [i for i in self.__admin.projects if i.importance == "Low"]
                temp = low_projects + medium_projects + important_projects
            case "Execute ↓":
                temp = sorted(temp, key=lambda x: int(x.executed), reverse=True)
            case "Execute ↑":
                temp = sorted(temp, key=lambda x: int(x.executed))
        return temp

    def render_projects(self, master, prop_filter: str, start_symbols: str) -> None:
        """
        Відмальовує картки проектів у батьківському фреймі master.
        :param master: Батьківський фрейм
        :param prop_filter: Властивість, за якою фільтрується список
        :param start_symbols: Початкові символи, за якими фільтрується список
        :return: None
        """
        list_of_projects = self.sort_projects(prop_filter, start_symbols)
        for i in master.winfo_children():
            i.destroy()

        if not list_of_projects:
            label = CTkLabel(master, text="No projects", font=('Arial', 18), text_color=("black", "white"),
                             fg_color="transparent", bg_color=("#E4E6C3", "#496A81"))
            label.pack(pady=10)
            return

        for project in list_of_projects:
            project_frame = CTkFrame(master, fg_color=("#F7F7F2", "#0A2239"), bg_color=("#E4E6C3", "#496A81"),
                                     corner_radius=10)
            project_frame.pack(fill="x", expand=True, pady=5)
            name_label = CTkLabel(project_frame, text=f"{project.name} — {project.executed}%", font=('Arial', 22),
                                  text_color=("black", "white"),
                                  fg_color="transparent", bg_color=("#F7F7F2", "#0A2239"))
            name_label.grid(row=0, column=0, sticky="w", padx=10)
            info = CTkLabel(project_frame, text=f"Start: {datetime.strftime(project.date_of_start, "%d.%m.%Y")}\n"
                                                f"End: {datetime.strftime(project.date_of_end, "%d.%m.%Y")}\n"
                                                f"Importance: {project.importance}", justify=LEFT, font=("Arial", 18),
                            text_color=("black", "white"),
                            fg_color="transparent", bg_color=("#F7F7F2", "#0A2239"))
            info.grid(row=0, column=1, sticky="e", padx=10, pady=10)

            separator = CTkFrame(project_frame, fg_color="light grey", width=950, height=2)
            separator.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
            description_label = CTkLabel(project_frame, text=project.description, font=("Arial", 18),
                                         text_color=("black", "white"), wraplength=900,
                                         fg_color="transparent", bg_color=("#F7F7F2", "#0A2239"))
            description_label.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    def update_base(self) -> None:
        """
        Оновляє базу даних.
        :return: None
        """
        for proj in self.__admin.projects:
            proj.date_of_start = datetime.strftime(proj.date_of_start, "%d.%m.%Y")
            proj.date_of_end = datetime.strftime(proj.date_of_end, "%d.%m.%Y")
        self.users["admin"] = {
            "name": self.__admin.name,
            "age": self.__admin.age,
            "sex": self.__admin.sex,
            "phone": self.__admin.phone,
            "email": self.__admin.email,
            "address": self.__admin.address,
            "hdate": datetime.strftime(self.__admin.hdate, "%d.%m.%Y"),
            "seniority": self.__admin.seniority,
            "docs": {
                "passport": self.__admin.docs["passport"],
                "graduation": self.__admin.docs["graduation"],
                "medcard": self.__admin.docs["medcard"],
                "mil_accounting": self.__admin.docs["mil_accounting"],
            },
            "duties": self.__admin.duties,
            "days": self.__admin.days if self.__admin.days else [],
            "next_vacation": datetime.strftime(self.__admin.next_vacation, "%d.%m.%Y"),
            "status": self.__admin.status,
            "salary": self.__admin.salary,
            "photo": self.__admin.photo,
            "actions_history": [i.__dict__ for i in self.__admin.action_history],
            "projects": [i.__dict__ for i in self.__admin.projects],
            "login": "pavlo2009",
            "password": "0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c",
            "theme": "light" if get_appearance_mode() == "Light" else "dark",
            "staff_id": self.__admin.staff_id,
            "workspace": self.__admin.workspace,
            "notes": self.__admin.notes
        }
        self.users["employees"] = {}
        for emp in self.employees:
            self.users["employees"][emp.staff_id] = {
                "name": emp.name,
                "age": emp.age,
                "sex": emp.sex,
                "phone": emp.phone,
                "email": emp.email,
                "address": emp.address,
                "hdate": datetime.strftime(emp.hdate, "%d.%m.%Y"),
                "seniority": emp.seniority,
                "docs": emp.docs,
                "duties": emp.duties,
                "days": emp.days if emp.days else [],
                "next_vacation": datetime.strftime(emp.next_vacation, "%d.%m.%Y"),
                "status": emp.status,
                "salary": emp.salary,
                "photo": emp.photo,
                "workspace": emp.workspace,
                "position": emp.position,
                "rate": emp.rate
            }

    def close_windows(self) -> None:
        """
        Закриває програму, перед тим змінивши базу даних.
        :return: None
        """
        self.update_base()
        self.save_to_base("DB/users.json")
        for window in self.opened_windows:
            window.destroy()

    def save_to_base(self, filepath: str) -> None:
        """
        Зберігає базу даних в файл json.
        :param filepath: Шлях, де повинен міститися файл.
        :return: None
        """
        try:
            with open(filepath, 'w', encoding="utf-8") as file:
                json.dump(self.users, file, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            CTkMessagebox(message="Can't save resources.")

    def on_close(self, window) -> None:
        """
        Перехплює закриття вікна для того, щоб видалити його зі списку відкритих вікон.
        :param window: Відкрите вікно
        :return: None
        """
        self.opened_windows.remove(window)
        window.destroy()

    @staticmethod
    def choose_file(p_label, p_copier) -> None:
        """
        Запитує шлях до файлу у користувача. Якщо користувач вибере файл,
        то функція змінює текст p_label на новий шлях,
        а також вставляє його в функцію копіювання шляху.
        :param p_label: Надпис (CTkLabel) зі шляхом до файлу
        :param p_copier: Кнопка копіювання шляху
        :return: None
        """
        file_name = filedialog.askopenfilename()
        if file_name:
            p_label.configure(text=file_name)
            p_copier.configure(command=lambda: pyperclip.copy(p_label.cget("text")))

    @staticmethod
    def on_hdate_change(hdate_picker, next_vacation_picker) -> None:
        """
        Відслідковує зміну дати у hdate_picker,
        і перевіряє, чи не є вибрана дата більша за дату в next_vacation_picker,
        якщо так, то змінює дату в next_vacation_picker на наступний день від дати в hdate_picker,
        і потім в обох випадках задає мінімальну дату для next_vacation_picker.
        :hdate_picker: Поле вводу дати найму (DateEntry)
        :next_vacation_picker: Поле вводу дати найму (DateEntry)
        :return: None
        """
        hdate = datetime.strptime(hdate_picker.get(), "%d.%m.%Y")
        next_vacation = datetime.strptime(next_vacation_picker.get(), "%d.%m.%Y")
        if hdate >= next_vacation:
            next_vacation_picker.set_date(date(hdate.year, hdate.month, hdate.day + 1))
            next_vacation_picker.configure(mindate=date(hdate.year, hdate.month, hdate.day + 1))
            return
        next_vacation_picker.configure(mindate=date(hdate.year, hdate.month, hdate.day + 1))

    @staticmethod
    def generate_id(list_of_ids: list[str]) -> str:
        """
        Генерує випадковий ID для працівників
        :param list_of_ids: Список існуючих ID
        :return: str
        """
        list_of_symbols = list(string.digits)[0:7]
        new_id = "ID" + "".join([random.choice(list_of_symbols) for _ in range(6)])
        return new_id if new_id not in list_of_ids else Application.generate_id(list_of_ids)

    @staticmethod
    def load_base(filepath: str) -> dict:
        """
        Зчитує файл json з даними про працівників і користувачів.
        :param filepath: Шлях до файлу
        :return: dict
        """
        try:
            with open(filepath, 'r', encoding="utf-8") as file:
                data = json.load(file)
                return data
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            CTkMessagebox(message="Can't load resources.")
            return {}

    @staticmethod
    def theme_switcher() -> None:
        """
        Змінює тему програми.
        :return: None
        """
        if get_appearance_mode() == "Light":
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")

    @staticmethod
    def crop_center(image: Image.Image, target_size: tuple[int, int]) -> Image.Image:
        """
        Обрізає зображення до вказаних розмірів.
        :param image: Зображення, яке буде обрізане
        :param target_size: Потрібні розміри
        :return: Обрізане зображення (Image.Image)
        """
        target_width, target_height = target_size
        original_width, original_height = image.size
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height
        if original_ratio > target_ratio:
            new_width = int(original_height * target_ratio)
            new_height = original_height
        else:
            new_width = original_width
            new_height = int(original_width / target_ratio)
        left = (original_width - new_width) // 2
        top = (original_height - new_height) // 2
        right = left + new_width
        bottom = top + new_height
        cropped = image.crop((left, top, right, bottom))
        resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return resized
