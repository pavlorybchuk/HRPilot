from datetime import datetime


class Project:
    def __init__(self, project_id: str, name: str, description: str, date_of_start: str, date_of_end: str,
                 importance: str):
        self.__project_id = project_id
        self.name = name
        self.description = description
        self.__date_of_start = date_of_start
        self.__date_of_end = date_of_end
        self.importance = importance

    @property
    def project_id(self):
        return self.__project_id

    @project_id.setter
    def project_id(self, list_of_params: list):
        if list_of_params[0] and list_of_params[0] not in list_of_params[1]:
            self.__project_id = list_of_params[0]
        raise ValueError("Project ID is not valid or it is in use")

    @property
    def date_of_start(self):
        return self.__date_of_start

    @date_of_start.setter
    def date_of_start(self, date_of_start: str):
        self.__date_of_start = datetime.strptime(date_of_start, "%m.%d.%Y")

    @property
    def date_of_end(self):
        return self.__date_of_end

    @date_of_end.setter
    def date_of_end(self, date_of_end: str):
        self.__date_of_end = datetime.strptime(date_of_end, "%m.%d.%Y")
