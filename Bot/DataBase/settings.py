from imports import *

from Bot.DataBase.Connection import DBConnection


class DBSettings:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `settings` (guild_id BIGINT,moderator_roles VARCHAR(255), PRIMARY KEY (guild_id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def get_settings(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM settings WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = {}
        for guild_id, moderator_roles in result:
            moderator_roles = json.loads(moderator_roles)
            toret[str(guild_id)] = [moderator_roles]
        return toret

    def add(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO settings (guild_id, moderator_roles)VALUES ( %s, %s)"
        val = (int(guild_id), "[]")
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()