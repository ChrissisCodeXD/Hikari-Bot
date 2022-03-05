from imports import *

from Bot.DataBase.Connection import DBConnection


class DBPrefix:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `prefixes` (id int auto_increment,guild_id BIGINT,prefix varchar(255),PRIMARY KEY (id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def get_all_prefixes(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM prefixes;"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = {}
        for id, guild_id, prefix in result:
            toret[str(guild_id)] = prefix
        return toret

    def insert_one(self, guild_id, prefix):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO prefixes (guild_id, prefix) VALUES (%s, %s)"
        val = (int(guild_id), prefix)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def get_prefix_for_guild(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM prefixes WHERE guild_id = %s;"

        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = {}
        for id, guild_id, prefix in result:
            toret[str(guild_id)] = prefix
        return toret

    def update_one(self, guild_id, prefix):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE prefixes SET prefix = %s WHERE guild_id = %s;"
        val = (prefix, int(guild_id))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
