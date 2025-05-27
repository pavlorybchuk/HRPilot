from .Human import *
from .Action import Action
from .Project import Project


class Admin(Human):
    def __init__(self, name, age, sex, phone, email, address, hdate, seniority, docs, duties, days, next_vacation,
                 status, salary, staff_id, photo, workspace, notes):
        super().__init__(name, age, sex, phone, email, address, hdate, seniority, docs, duties, days, next_vacation,
                         status, salary, staff_id, photo, workspace)
        self.__action_history = []
        self._projects = []
        self.workspace = workspace.capitalize()
        self.notes = notes

    def show_info(self) -> str:
        """
        Повертає стрічку з інформацію про об'єкт.
        :return: str
        """
        base_info = super().show_info()
        return base_info + f"\nWorkspace: {self.workspace};"

    def show_projects(self) -> str:
        """
        Повертає стрічку з базовою інформацією про існуючі проекти.
        :return: str
        """
        line = ""
        if not self._projects:
            return "No projects yet"

        for project in range(len(self._projects)):
            line += (f"{self._projects[project].name} - {self._projects[project].executed}"
                     f"{"\n" if project != len(self._projects) - 1 else ""}")
        return line

    @property
    def action_history(self) -> list:
        """
        Повертає історію подій.
        :return:
        """
        return self.__action_history

    @action_history.setter
    def action_history(self, action: object) -> None:
        """
        Додає нову подію до списку.
        :param action: Нова подія
        :return: None
        """
        if not isinstance(action, Action):
            raise TypeError("Action must be an instance")
        self.__action_history.append(action)

    @property
    def projects(self) -> list:
        """
        Повертає список проектів
        :return:
        """
        return self._projects

    @projects.setter
    def projects(self, project: object) -> None:
        """
        Додає новий проект до списку.
        :param project: Новий проект
        :return: None
        """
        if not isinstance(project, Project):
            raise TypeError("Project must be an instance")
        self._projects.append(project)

    def remove_project(self, project_name: str) -> None:
        """
        Видаляє проект зі списку.
        :param project_name: Назва проекту
        :return: None
        """
        for project in self._projects:
            if project.name.lower() == project_name.lower():
                self._projects.remove(project)
                return
        raise IndexError("Project not found")
