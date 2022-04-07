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
        res = self.get(int(guild_id))
        if not res:
            self.add(int(guild_id))
        match log_type:
            case "all":
                log_type = "all_logs"
                index = 2
            case "message_delete":
                log_type = "message_delete"
                index = 3
            case "audit_log":
                log_type = "audit_log"
                index = 4
            case "mod_logs":
                log_type = "mod_logs"
                index = 5
            case _:
                raise ValueError("Invalid log type")

        if res[index] == channel_id:
            return False
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE `logchannels` SET {log_type} = %s WHERE guild_id = %s"
        mycursor.execute(query,(int(channel_id),int(guild_id)))
        mydb.commit()
        mycursor.close()
        mydb.close()
        return True

    def get(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM `logchannels` WHERE guild_id = %s"
        mycursor.execute(query,(int(guild_id),))
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        return result

    def get_dict(self,guild_id):
        res = self.get(int(guild_id))
        if not res:
            return None
        else:
            return {
                "all_logs": res[2],
                "message_delete": res[3],
                "audit_log": res[4],
                "mod_logs": res[5]
            }

    def add(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `logchannels` (guild_id) VALUES (%s)"
        mycursor.execute(query,(int(guild_id),))
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
        query = f"UPDATE `logchannels` SET {log_type} = 0 WHERE guild_id = %s"
        mycursor.execute(query,(int(guild_id),))
        mydb.commit()
        mycursor.close()
        mydb.close()


    def get_type_by_channel_id(self,channel_id,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM `logchannels` WHERE guild_id = %s"
        mycursor.execute(query,(int(guild_id),))
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        res = {"guild_id": result[1], "all": result[2], "message_delete": result[3], "audit_log": result[4], "mod_logs": result[5]}

        for i in res:
            if res[i] == channel_id and i != "guild_id":
                return i
        return None

    def remove_log_channel(self,guild_id,channel_id):
        typee = self.get_type_by_channel_id(channel_id,int(guild_id))
        if typee:
            self.__remove_log_channel(int(guild_id),typee)
            return True
        else: return None



