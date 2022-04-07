from imports import *


from Bot.DataBase.Connection import *


class DBAuditLog:

    def __init__(self,db):
        self.dbConnection = db

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `auditlog`"\
                "(id int auto_increment, guild_id BIGINT, ban TINYINT DEFAULT 0,"\
                " guild_change TINYINT DEFAULT 0, audit_log TINYINT DEFAULT 0, mod_logs TINYINT DEFAULT 0,"\
                " PRIMARY KEY(id))"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()