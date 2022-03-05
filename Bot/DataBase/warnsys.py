from imports import *

from Bot.DataBase.Connection import DBConnection

import datetime


class DBwarn:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection



    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `warn` (id int auto_increment,guild_id BIGINT,user_id BIGINT,author_id BIGINT, reason varchar(255), PRIMARY KEY (id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `warn_settings` (guild_id BIGINT,punishments LONGTEXT, PRIMARY KEY (guild_id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()


    def add(self,author_id,reason,user_id,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO warn (guild_id, user_id, author_id, reason)VALUES (%s, %s, %s, %s)"
        val = (int(guild_id),int(user_id),int(author_id),reason)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def get_warns(self,user_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM warn WHERE user_id = %s;"
        mycursor.execute(query, [int(user_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = []
        for id, guild_id, user_id, author_id, reason in result:
            toret.append([user_id, guild_id, author_id, reason])
        return toret

    def get_settings(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM warn_settings WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = {}
        for guild_id, punishments in result:
            res = json.loads(punishments)
            res = sorted(res,key=lambda x: x[0])
            toret[str(guild_id)] = res
        return toret

    def add_settings(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO warn_settings (guild_id, punishments)VALUES (%s, %s)"
        val = (int(guild_id), "[]")
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()