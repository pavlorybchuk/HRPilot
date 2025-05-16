from .Human import *
from .Employee import Employee
from .Project import Project
from .Action import Action
import hashlib


class Manager(Human):
    def __init__(self):
        super().__init__()
        self.__subordinates = []
        self.__action_history = []
        self.__projects = []
        self.workspace = None
        self.notes = None

    def show_info(self):
        base_info = super().show_info()
        return base_info + f"\nWorkspace: {self.workspace};"

    @property
    def subordinates(self):
        return self.__subordinates

    @subordinates.setter
    def subordinates(self, subordinate: object):
        if not isinstance(subordinate, Employee):
            raise TypeError("Subordinate must be an instance")
        self.__subordinates.append(subordinate)

    @property
    def action_history(self):
        return self.__action_history

    @action_history.setter
    def action_history(self, action: object):
        if not isinstance(action, Action):
            raise TypeError("Action must be an instance")
        self.__action_history.append(action)

    @property
    def projects(self):
        return self.__projects

    @projects.setter
    def projects(self, project: object):
        if not isinstance(project, Project):
            raise TypeError("Project must be an instance")
        self.__projects.append(project)

    def remove_subordinate(self, subordinate_id: str):
        for subordinate in self.__subordinates:
            if subordinate.staff_id() == subordinate_id:
                self.__subordinates.remove(subordinate)
                return True
        raise IndexError("Subordinate not found")

    def remove_project(self, project_id: str):
        for project in self.__projects:
            if project.project_id() == project_id:
                self.__projects.remove(project)
                return True
        raise IndexError("Project not found")

