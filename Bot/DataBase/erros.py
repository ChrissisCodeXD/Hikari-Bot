from imports import *

from Bot.DataBase.Connection import DBConnection


class DBErros:

    def __init__(self, dbConnection):
        self.dbConnection = dbConnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `errors` (id int auto_increment,err_id BIGINT,err_cmd varchar(255),err_text varchar(255), PRIMARY KEY (id));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def add(self,err_id,cmd,trc):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO errors (err_id, err_cmd,err_text)VALUES (%s, %s,%s)"
        val = (int(err_id), str(cmd),str(trc))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()