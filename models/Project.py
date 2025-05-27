from datetime import datetime


class Project:
    def __init__(self, name: str, description: str, date_of_start: str, date_of_end: str,
                 importance: str, executed: int):
        self.name = name
        self.description = description
        self.date_of_start = datetime.strptime(date_of_start, '%d.%m.%Y')
        self.date_of_end = datetime.strptime(date_of_end, '%d.%m.%Y')
        self.importance = importance
        self.executed = executed
