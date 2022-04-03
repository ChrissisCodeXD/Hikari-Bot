import time


class mute_class:
    def __init__(self,
                 id: int,
                 unique_id: str,
                 guild_id: int,
                 user_id: int,
                 author_id: int,
                 reason: str,
                 timee: int,
                 currenttime: int):
        self.id = int(id)
        self.unique_id = unique_id
        self.guild_id = int(guild_id)
        self.user_id = int(user_id)
        self.author_id = int(author_id)
        self.reason = reason
        self.time = int(timee)
        self.currenttime = currenttime

    @property
    def isstillmuted(self):
        if self.time == 0: return True
        return True if int(time.time()) < int(self.time) else False
