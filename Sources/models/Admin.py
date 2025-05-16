from .Human import *
from .Action import Action
from .Project import Project


class Admin(Human):
    def __init__(self):
        super().__init__()
        self.__action_history = []
        self.__projects = []
        self.notes = None

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

    def remove_project(self, project_id: str):
        for project in self.__projects:
            if project.project_id() == project_id:
                self.__projects.remove(project)
                return True
        raise IndexError("Project not found")
