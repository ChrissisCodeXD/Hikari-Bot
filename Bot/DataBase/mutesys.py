from imports import *

import utils
from Bot.DataBase.Connection import DBConnection


class DBMute:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `mute` (id int auto_increment,unique_id VARCHAR(255),guild_id BIGINT,user_id BIGINT,author_id BIGINT, reason varchar(255),time BIGINT,currenttime BIGINT, PRIMARY KEY (id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `mute_settings` (guild_id BIGINT,mute_role BIGINT, PRIMARY KEY (guild_id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def get_settings(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT guild_id, mute_role FROM mute_settings WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = {}
        for guild_id, mute_role in result:
            toret[str(guild_id)] = mute_role
        return toret

    def get_all_settings(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT guild_id, mute_role FROM mute_settings;"
        mycursor.execute(query)
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

    def get_mute_role(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT mute_role FROM mute_settings WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if result:
            toret = result[0]
            return toret
        else:
            return None

    def create_mute(self, ctx, reason, timee):
        current_time = int(time.time())
        g_id = True
        while g_id:
            id = utils.generate_id()
            res = self.get_mute(id)
            if not res:
                g_id = False
                break
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO mute (unique_id ,guild_id,user_id ,author_id , reason ,time,currenttime )VALUES (%s, %s,%s, %s,%s, %s, %s)"
        val = (id, int(ctx.guild_id), int(ctx.options.member.id), int(ctx.author.id), reason, timee, current_time)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        return id

    def get_mute(self, cid):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM mute WHERE unique_id=%s;"
        mycursor.execute(query, [cid])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = []
        return result

    def get_all(self) -> list[utils.mute_class]:
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM mute ;"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = []
        for i in result:
            toret.append(
                utils.mute_class(
                    id=i[0],
                    unique_id=i[1],
                    guild_id=i[2],
                    user_id=i[3],
                    author_id=i[4],
                    reason=i[5],
                    timee=i[6],
                    currenttime=i[7]
                )
            )
        return toret

    def get_all_for_user(self, user_id, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM mute WHERE guild_id = %s AND user_id = %s;"
        mycursor.execute(query, [int(guild_id), int(user_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        toret = []
        for i in result:
            toret.append(
                utils.mute_class(
                    id=i[0],
                    unique_id=i[1],
                    guild_id=i[2],
                    user_id=i[3],
                    author_id=i[4],
                    reason=i[5],
                    timee=i[6],
                    currenttime=i[7]
                )
            )
        return toret

    def delete_mute_settings(self, g_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM mute_settings WHERE guild_id=%s;"
        mycursor.execute(query, [int(g_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()

    def delete_all_from_guild(self, g_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM mute WHERE guild_id=%s;"
        mycursor.execute(query, [int(g_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()

    def delete_mute(self, id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM mute WHERE unique_id=%s;"
        mycursor.execute(query, [id])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if not result: return False
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM mute WHERE unique_id=%s;"
        mycursor.execute(query, [id])
        mydb.commit()
        mycursor.close()
        mydb.close()
        return True

    def delete_all_mute_from(self, user_id, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM mute WHERE user_id=%s AND guild_id=%s;"
        mycursor.execute(query, [int(user_id), int(guild_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()
