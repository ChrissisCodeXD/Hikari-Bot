from imports import *

from Bot.DataBase.Connection import DBConnection


class DBLevel:

    def __init__(self, dbconnection):
        self.dbConnection = dbconnection

    def create(self):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `levelsys` (id int auto_increment,user_id BIGINT,exp BIGINT,lastmsg timestamp,guild_id BIGINT,lvl BIGINT, name varchar(255),avatar_url LONGTEXT,PRIMARY KEY (id))DEFAULT CHARACTER SET utf8mb4;"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"CREATE TABLE IF NOT EXISTS `levelguilds` (ison TINYINT,guildid BIGINT,channels LONGTEXT,xpmult DECIMAL,doubleexp TINYINT, lvlmsg Longtext,PRIMARY KEY (guildid));"
        mycursor.execute(query)
        mycursor.close()
        mydb.close()

    def add(self, author: int, exp: int, guild: int, username: str, avatar_url: str):
        """Adds a User to Databse"""
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `levelsys` (`user_id`, `exp`,`guild_id`,`lvl`,`name`,`avatar_url`) VALUES (%s, %s, %s,%s,%s,%s);"
        val = (int(author), exp, int(guild), 0, username, avatar_url)
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def get_settings(self, guildid: int) -> dict:
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelguilds WHERE guildid = %s;"
        mycursor.execute(query, [int(guildid)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            toreturn = {}
            toreturn["ison"] = result[0][0]
            toreturn["guildid"] = result[0][1]
            toreturn["channels"] = json.loads(result[0][2])
            toreturn["xpmult"] = result[0][3]
            toreturn["doubleexp"] = result[0][4]
            toreturn["lvlmsg"] = result[0][5]
            return toreturn
        else:
            return None

    def update_settings(self, guild_id, setting, value):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE levelguilds SET {setting} = %s WHERE guildid = %s;"
        val = (value, int(guild_id))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def addtoguilds(self, guild_id):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `levelguilds` (`ison`, `guildid`,`channels`) VALUES ( %s, %s,%s);"
        val = (0, int(guild_id), "[]")
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def isindatabase(self, author: int, guild: int):
        """checks if user is in Database"""
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelsys WHERE user_id = %s AND guild_id = %s;"
        val = (int(author), int(guild))
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            return result[0]
        else:
            return False

    def isindatabaseguilds(self, guild: int):
        """checks if user is in Database"""
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelguilds WHERE guildid = %s;"
        mycursor.execute(query, [int(guild)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            return result[0]
        else:
            return False

    def addEXP(self, author: int, guild: int, exp: int):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelsys WHERE user_id = %s AND guild_id = %s;"
        val = (int(author), int(guild))
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        exp = result[0][2] + exp
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"UPDATE levelsys SET exp = %s WHERE user_id = %s AND guild_id = %s;"
        val = (int(exp), int(author), int(guild))
        mycursor.execute(query, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    def checkLVL(self, author: int, guild: int):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelsys WHERE user_id = %s AND guild_id = %s;"
        val = (int(author), int(guild))
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        experience = result[0][2]
        lvl = result[0][5]
        lvl_end = 5 * (lvl ** 2) + (50 * lvl) + 100
        if lvl_end <= experience:
            mydb = self.dbConnection.getConnection()
            mycursor = mydb.cursor()
            query = f"UPDATE levelsys SET exp = %s, lvl = %s WHERE user_id = %s AND guild_id = %s;"
            lvl += 1
            experience = experience - lvl_end
            val = (int(experience), int(lvl), int(author), int(guild))
            mycursor.execute(query, val)
            mydb.commit()
            mycursor.close()
            mydb.close()
            return lvl
        return False

    def getlvlupchannels(self, guildid: int):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelguilds WHERE guildid = %s;"
        mycursor.execute(query, [int(guildid)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            if len(list(result[0][2])) > 0:
                return json.loads(result[0][2])

    def get_level_settings(self, guildid: int):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelguilds WHERE guildid = %s;"
        mycursor.execute(query, [int(guildid)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            return [result[0][0], result[0][1], json.loads(result[0][2]), result[0][3], result[0][4], result[0][5]]
        else:
            return False

    def gettop10(self, guildid):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelsys WHERE guild_id = %s ORDER BY lvl DESC, exp DESC;"
        mycursor.execute(query, [int(guildid)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result

    def add_lvlup_channel(self, guildid: int, channelid: int):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelguilds WHERE guildid = %s;"
        mycursor.execute(query, [int(guildid)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            new_channels = json.loads(result[0][2])
            new_channels.append(int(channelid))
            mydb = self.dbConnection.getConnection()
            mycursor = mydb.cursor()
            query = f"UPDATE levelguilds SET channels = %s WHERE guildid = %s;"
            val = (json.dumps(new_channels), int(guildid))
            mycursor.execute(query, val)
            mydb.commit()
            mycursor.close()
            mydb.close()
        else:
            self.addtoguilds(guildid)
            self.add_lvlup_channel(guildid, channelid)

    def remove_lvlup_channels(self, guildid: int, channelid: int):
        mydb = self.dbConnection.getConnection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM levelguilds WHERE guildid = %s;"
        mycursor.execute(query, [int(guildid)])
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if len(result) > 0:
            new_channels = json.loads(result[0][2])
            new_channels.remove(int(channelid))
            mydb = self.dbConnection.getConnection()
            mycursor = mydb.cursor()
            query = f"UPDATE levelguilds SET channels = %s WHERE guildid = %s;"
            val = (json.dumps(new_channels), int(guildid))
            mycursor.execute(query, val)
            mydb.commit()
            mycursor.close()
            mydb.close()
        else:
            self.addtoguilds(guildid)
            self.remove_lvlup_channels(guildid, channelid)
