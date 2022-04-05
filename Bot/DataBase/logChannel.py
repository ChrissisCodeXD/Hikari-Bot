from imports import *

from Bot.DataBase.Connection import DBConnection


class DBlog:

    def __init__(self,dbconnection):
        self.dbConnection = dbconnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `logchannels`(id int auto_increment, guild_id BIGINT, all_logs BIGINT DEFAULT 0, message_delete BIGINT DEFAULT 0, audit_log BIGINT DEFAULT 0, mod_logs BIGINT DEFAULT 0, PRIMARY KEY(id))"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def add_log_channel(self,guild_id,log_type: str,channel_id: int):
        res = self.get(guild_id)
        if not res:
            self.add(guild_id)
        match log_type:
            case "all":
                log_type = "all_logs"
            case "message_delete":
                log_type = "message_delete"
            case "audit_log":
                log_type = "audit_log"
            case "mod_logs":
                log_type = "mod_logs"
            case _:
                raise ValueError("Invalid log type")

        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE `logchannels` SET %s = %s WHERE guild_id = %s"
        mycursor.execute(query,(log_type,channel_id,guild_id))
        mydb.commit()
        mycursor.close()
        mydb.close()

    def get(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM `logchannels` WHERE guild_id = %s"
        mycursor.execute(query,(guild_id,))
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        return result

    def add(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `logchannels` (guild_id) VALUES (%s)"
        mycursor.execute(query,(guild_id,))
        mydb.commit()
        mycursor.close()
        mydb.close()

    def __remove_log_channel(self,guild_id,log_type: str):
        match log_type:
            case "all":
                log_type = "all_logs"
            case "message_delete":
                log_type = "message_delete"
            case "audit_log":
                log_type = "audit_log"
            case "mod_logs":
                log_type = "mod_logs"
            case _:
                raise ValueError("Invalid log type")

        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE `logchannels` SET %s = 0 WHERE guild_id = %s"
        mycursor.execute(query,(log_type,guild_id))
        mydb.commit()
        mycursor.close()
        mydb.close()


    def get_type_by_channel_id(self,channel_id,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM `logchannels` WHERE guild_id = %s"
        mycursor.execute(query,(guild_id,))
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        for id, guildid, all_logs, message_delete, audit_log, mod_logs in result[0]:
            res = {"guild_id": guildid, "all_logs": all_logs, "message_delete": message_delete, "audit_log": audit_log, "mod_logs": mod_logs}

        for i in res:
            if res[i] == channel_id and i != "guild_id":
                return i
        return None

    def remove_log_channel(self,channel_id,guild_id):
        type = self.get_type_by_channel_id(channel_id,guild_id)
        if type:
            self.__remove_log_channel(guild_id,type)
            return True
        else: return None



