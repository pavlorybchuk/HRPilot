from datetime import datetime


class Action:
    def __init__(self, action_name: str, describe: str, creator_id: str, date_of_creating=None):
        self.date_of_creating = date_of_creating if date_of_creating else datetime.strftime(datetime.now(),
                                                                                            "%d.%m.%Y %H:%M")
        self.describe = describe
        self.creator_id = creator_id
        self.action_name = action_name.upper()
