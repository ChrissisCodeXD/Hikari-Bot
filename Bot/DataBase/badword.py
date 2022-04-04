from imports import *

from Bot.DataBase.Connection import DBConnection


class DBBadWord:

    def __init__(self, debconnection):
        self.dbConnection = debconnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `badwords`(id int auto_increment, guild_id BIGINT, words LONGTEXT DEFAULT '[]', ison TINYINT, PRIMARY KEY(id))"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def set_onoroff(self, guild_id, onoroff):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        onoroff = 1 if onoroff else 0
        query = "UPDATE badwords SET ison = %s WHERE guild_id = %s"
        mycursor.execute(query, [int(onoroff), int(guild_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()


    def get_bad_words(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = "SELECT words FROM badwords WHERE guild_id = %s"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        return json.loads(result[0])

    def add_bad_word(self, guild_id, word):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = "SELECT words FROM badwords WHERE guild_id = %s"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchone()
        if result:
            words = json.loads(result[0])
            if word in words:
                return False
            words.append(word)
            query = "UPDATE badwords SET words = %s WHERE guild_id = %s"
            mycursor.execute(query, [json.dumps(words), int(guild_id)])
            mydb.commit()
            mycursor.close()
            mydb.close()
            return True
        else:
            self.add(guild_id)
            return self.add_bad_word(guild_id, word)

    def add(self,guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = "INSERT INTO badwords (guild_id, words,ison) VALUES (%s, '[]',0)"
        mycursor.execute(query, [int(guild_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()



    def remove_bad_word(self, guild_id, word):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = "SELECT words FROM badwords WHERE guild_id = %s"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchone()
        if not result:
            words = []
        else:
            words = json.loads(result[0])
        if word not in words:
            return False
        words.remove(word)
        query = "UPDATE badwords SET words = %s WHERE guild_id = %s"
        mycursor.execute(query, [json.dumps(words), int(guild_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()
        return True

    def clear_bad_words(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = "UPDATE badwords SET words = '[]' WHERE guild_id = %s"
        mycursor.execute(query, [int(guild_id)])
        mydb.commit()
        mycursor.close()
        mydb.close()

    def get_onoroff(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = "SELECT ison FROM badwords WHERE guild_id = %s"
        mycursor.execute(query, [int(guild_id)])
        result = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        return True if result[0] == 1 else False
