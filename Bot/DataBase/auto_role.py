from imports import *

from Bot.DataBase.Connection import DBConnection


class DBRole:

    def __init__(self, dbconnection):
        self.dbConnection = dbconnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `auto_roles`(id int auto_increment, guild_id BIGINT, roles LONGTEXT DEFAULT '[]', PRIMARY KEY(id))"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def add_role(self, guild_id, role_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM auto_roles WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            new_channels = json.loads(result[0][2])
            if role_id in new_channels:
                return False
            new_channels.append(int(role_id))
            mydb = self.dbConnection.getConnection()
            mycursor = mydb.cursor()
            query = f"UPDATE auto_roles SET roles = %s WHERE guild_id = %s;"
            val = (json.dumps(new_channels), int(guild_id))
            mycursor.execute(query, val)
            mydb.commit()
            mycursor.close()
            mydb.close()
            return True
        else:
            self.addtoguilds(guild_id)
            return self.add_role(guild_id, role_id)

    def addtoguilds(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO auto_roles (guild_id) VALUES (%s);"
        mycursor.execute(query, [int(guild_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()

    def get_auto_roles(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM auto_roles WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            return json.loads(result[0][2])
        else:
            self.addtoguilds(guild_id)
            return self.get_auto_roles(guild_id)

    def remove_role(self, guild_id, role_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM auto_roles WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            new_channels = json.loads(result[0][2])
            if role_id in new_channels:
                new_channels.remove(int(role_id))
                mydb = self.dbConnection.getConnection()
                mycursor = mydb.cursor()
                query = f"UPDATE auto_roles SET roles = %s WHERE guild_id = %s;"
                val = (json.dumps(new_channels), int(guild_id))
                mycursor.execute(query, val)
                mydb.commit()
                mycursor.close()
                mydb.close()
                return True
            else:
                return False
        else:
            return False

    def delete_all_from_guild(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM auto_roles WHERE guild_id = %s;"
        mycursor.execute(query, [int(guild_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()
