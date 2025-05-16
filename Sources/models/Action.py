from datetime import datetime

class Action:
    def __init__(self, date_of_creating: str, describe: str, creator_name: str, action_name: str):
        self.__date_of_creating = date_of_creating
        self.describe = describe
        self.creator_name = creator_name
        self.action_name = action_name.capitalize()

    @property
    def date_of_creating(self):
        return self.__date_of_creating

    @date_of_creating.setter
    def date_of_creating(self, date_of_creating):
        self.__date_of_creating = datetime.strptime(date_of_creating, '%d.%m.%Y')

