from imports import *

from Bot.DataBase.Connection import DBConnection


class DBLink:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `link_settings` (guild_id BIGINT,social_media TINYINT, google TINYINT, bitly TINYINT, all_links TINYINT,discord TINYINT, GIF TINYINT, ignored_roles LONGTEXT,ignored_users LONGTEXT,PRIMARY KEY (guild_id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def get_settings(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM link_settings WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = {}
        for guild_id, social_media, google, bitly, alllinks, discord, GIF, ignored_roles, ignored_users in result:
            toret["social_media"] = True if social_media == 1 else False
            toret["google"] = True if google == 1 else False
            toret["bitly"] = True if bitly == 1 else False
            toret["all_links"] = True if alllinks == 1 else False
            ignored_roles = json.loads(ignored_roles)
            toret["ignored_roles"] = ignored_roles
            ignored_users = json.loads(ignored_users)
            toret["ignored_users"] = ignored_users
            toret["discord"] = True if discord == 1 else False
            toret["gif"] = True if GIF == 1 else False
        return toret

    def update_settings(self, guild_id: int, do_update: str, new_value: any):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE link_settings SET {do_update} = %s WHERE guild_id = %s;"
        mycursor.execute(query, [new_value, int(guild_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()

    def create_settings(self, guild_id: int):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO link_settings (guild_id,social_media,google,bitly,all_links,discord,GIF,ignored_roles,ignored_users) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        mycursor.execute(query, [int(guild_id), 0, 0, 0, 0, 0, 0, "[]", "[]"])
        mydb.commit()
        mycursor.close()
        mydb.close()
        toret = {}
        toret["social_media"] = False
        toret["google"] = False
        toret["bitly"] = False
        toret["all_links"] = False
        toret["ignored_roles"] = []
        toret["ignored_users"] = []
        toret["discord"] = False
        toret["gif"] = False
        return toret
