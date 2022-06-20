import pymysql
 
from pymysql.cursors import DictCursor
from contextlib import closing

from config import VOICE_EXP


class DATABASE(object):
    def __init__(self):
        import utils.env
        env = utils.env.load()
        
        self.host  = env.HOST
        self.db    = env.DATABASE
        self.user  = env.USER
        self.passw = env.PASS
        
        self.DISPLAY_BOTS = env.DISPLAY_BOTS
        
        del utils.env, env
    
    
    def conn(self):
        connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.passw,
            db=self.db,
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True
        )
        
        return connection
    
    
    def execute_query(self, query: str, res=False):
        with closing(self.conn()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                
                if res == True:
                    return cursor.fetchall()


class Lvl(DATABASE):
    def __init__(self):
        super(Lvl, self).__init__()
    
    
    def get_users_count(self):
        query = 'SELECT `id` FROM `members`'
        
        if not self.DISPLAY_BOTS:
            query += ' WHERE `bot`=0'
        
        return len(self.execute_query(query, res=True))
        
    
    
    def get_user_exp(self, uid: int):
        query = 'SELECT `messages`, `voice` FROM `members` WHERE `id`={uid}'
        
        res = self.execute_query(query.format(uid=uid), res=True)[0]
        
        return res['messages'] + (res['voice'] // VOICE_EXP)
    
    
    def get_user_data(self, uid: int):
        query = 'SELECT `messages`, `voice` FROM `members` WHERE `id`={uid}'
        
        return self.execute_query(query.format(uid=uid), res=True)[0]
    
    
    def add_exp(self, uid: int, time: int=None):
        if time == None:
            query = 'UPDATE `members` SET `messages`=`messages`+1 WHERE `id`={uid}'
        else:
            query = 'UPDATE `members` SET `voice`=`voice`+{time} WHERE `id`={uid}'
        
        self.execute_query(query.format(time=time, uid=uid))
    
    
    def user_exists(self, uid: int):
        """ return True | False """
        
        query = 'SELECT * FROM `members` WHERE `id`={uid}'
        
        return True if self.execute_query(query.format(uid=uid), res=True) != () else False
    
    
    def add_user(self, uid: int, bot: bool):
        query = 'INSERT INTO `members` (`id`, `bot`) VALUES ({uid}, {bot})'
        
        self.execute_query(query.format(uid=uid, bot=bot))
    
    
    def get_user_pos(self, uid: int):
        if self.DISPLAY_BOTS:
            query = 'SELECT @i:=@i+1, `id` FROM `members`, (select @i:=0)x ORDER BY `messages`+`voice`/{divide} DESC'
        else:
            query = 'SELECT @i:=@i+1, `id` FROM `members`, (select @i:=0)x WHERE `bot`=false ORDER BY `messages`+`voice`/{divide} DESC'
        
        res = self.execute_query(query.format(divide=VOICE_EXP), res=True)
         
        for member in res:
            if member['id'] == uid:
                return int(member['@i:=@i+1'])
    
    def get_top_users(self, count: int):
        if self.DISPLAY_BOTS:
            query = 'SELECT * FROM `members` ORDER BY `messages`+`voice`/{divide} DESC LIMIT {limit}'
        else:
            query = 'SELECT * FROM `members` WHERE `bot`=false ORDER BY `messages`+`voice`/{divide} DESC LIMIT {limit}'
        
        return self.execute_query(query.format(divide=VOICE_EXP, limit=count), res=True)
