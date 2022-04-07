from imports import *

from Bot.DataBase.Connection import *


class DBAuditLog:

    def __init__(self, db):
        self.dbConnection = db

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `auditlog` (" \
                "`id` int(11) NOT NULL AUTO_INCREMENT," \
                "`guild_id` bigint(20) NOT NULL," \
                "`ban` tinyint(4) DEFAULT 0," \
                "`guild_change` tinyint(4) DEFAULT 0," \
                "`channel_change` tinyint(4) DEFAULT 0," \
                "`invites` tinyint(4) DEFAULT 0," \
                "`member` tinyint(4) DEFAULT 0," \
                "`message` tinyint(4) DEFAULT 0," \
                "`role` tinyint(4) DEFAULT 0," \
                "`voice` tinyint(4) DEFAULT 0," \
                "PRIMARY KEY (`id`)" \
                ") ENGINE = InnoDB DEFAULT CHARSET = utf8mb4"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def add(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `auditlog` (`guild_id`) VALUES (%s)"
        values = (int(guild_id),)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def is_in_database(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM `auditlog` WHERE `guild_id` = %s"
        values = (int(guild_id),)
        mycursor.execute(query, values)
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if result:
            return True
        else:
            return False

    def set(self, guild_id, key, value):
        if self.is_in_database(guild_id):
            mydb = self.dbConnection.getConnection()
            mycursor = mydb.cursor()
            query = f"UPDATE `auditlog` SET `{key}` = %s WHERE `guild_id` = %s"
            values = (int(value), int(guild_id))
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()
            mydb.close()
        else:
            self.add(guild_id)
            self.set(guild_id, key, value)

    def get_settings(self, guild_id):
        if self.is_in_database(guild_id):
            mydb = self.dbConnection.getConnection()
            mycursor = mydb.cursor()
            query = f"SELECT * FROM `auditlog` WHERE `guild_id` = %s"
            values = (int(guild_id),)
            mycursor.execute(query, values)
            result = mycursor.fetchone()
            mycursor.close()
            mydb.close()
            toret = {
                "ban": True if result[2] == 1 else False,
                "guild_change": True if result[3] == 1 else False,
                "channel_change": True if result[4] == 1 else False,
                "invites": True if result[5] == 1 else False,
                "member": True if result[6] == 1 else False,
                "message": True if result[7] == 1 else False,
                "role": True if result[8] == 1 else False,
                "voice": True if result[9] == 1 else False
            }
            return toret
        else:
            self.add(guild_id)
            return self.get_settings(guild_id)
