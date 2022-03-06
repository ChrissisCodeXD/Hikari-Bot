from imports import *

from Bot.DataBase.Connection import DBConnection


class DBMute:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `mute` (id int auto_increment,guild_id BIGINT,user_id BIGINT,author_id BIGINT, reason varchar(255),time BIGINT, PRIMARY KEY (id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `mute_settings` (guild_id BIGINT,mute_role BIGINT, PRIMARY KEY (guild_id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()


    def get_settings(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT guild_id, mute_role FROM mute_settings WHERE guild_id = %s;"
        mycursor.execute(query,[int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = {}
        for guild_id, mute_role in result:
            toret[str(guild_id)] = mute_role
        return toret

    def get_mute_roles(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT guild_id, mute_role FROM mute_settings"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = {}
        for guild_id, mute_role in result:
            toret[str(guild_id)] = mute_role
        return toret

    def add_settings(self, guild_id, mute_role):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO mute_settings (guild_id, mute_role)VALUES (%s, %s)"
        val = (int(guild_id), int(mute_role))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()