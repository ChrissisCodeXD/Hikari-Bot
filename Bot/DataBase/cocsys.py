from imports import *

from Bot.DataBase.Connection import DBConnection


class DBCoc:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection


    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `coc` (id int auto_increment,guild_id BIGINT,channel_id BIGINT,message_id BIGINT,PRIMARY KEY (id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def get(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM coc WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result

    def add(self, guild_id, channel_id,mgs_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO coc (guild_id, channel_id)VALUES (%s, %s)"
        val = (int(guild_id), int(channel_id))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()