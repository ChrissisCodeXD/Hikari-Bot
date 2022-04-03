from imports import *

from Bot.DataBase.Connection import DBConnection


class DBWelcomeChannel:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection


    def indata(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM welcome_channels WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result if result else False


    def is_channel_indb(self,guild_id,welcome_channel):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT welcome_channel FROM welcome_channels WHERE guild_id = %s AND welcome_channel = %s;"
        mycursor.execute(query, [int(guild_id),int(welcome_channel)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return True if result else False

    def get_channels(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT welcome_channel FROM welcome_channels WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result if result else False

    def remove_channel(self,guild_id,welcome_channel):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM welcome_channels WHERE guild_id = %s AND welcome_channel = %s;"
        mycursor.execute(query, [int(guild_id),int(welcome_channel)])
        mydb.commit()
        mycursor.close()
        mydb.close()

    def add_channel(self,guild_id,welcome_channel,welcome_message,banner:int=0,banner_background:str=None,banner_color:str=None):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = "INSERT INTO welcome_channels (guild_id,welcome_channel,welcome_message,banner,banner_background,banner_color) VALUES (%s,%s,%s,%s,%s,%s);"
        mycursor.execute(query, [int(guild_id),int(welcome_channel),welcome_message,banner,banner_background,banner_color])
        mydb.commit()
        mycursor.close()
        mydb.close()


    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `welcome_channels` (id int auto_increment, guild_id BIGINT,welcome_channel BIGINT,welcome_message varchar(1000),banner TINYINT,banner_background varchar(1000), banner_color varchar(255) ,PRIMARY KEY (id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

class DBWelcomeDM:

    def __init__(self,dbConnection):
        self.dbConnection = dbConnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `welcome_dms` (guild_id BIGINT,dm_welcome_message  varchar(1000), PRIMARY KEY (guild_id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    #TODO: Add DM welcome message