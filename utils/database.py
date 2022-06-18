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
    
    
    def get_user_exp(self, uid: int):
        query = 'SELECT `messages`, `voice` FROM `members` WHERE `id`={uid}'
        
        res = self.execute_query(query.format(uid=uid), res=True)[0]
        
        return res['messages'] + (res['voice'] // VOICE_EXP)
    
    
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
    
    
    def add_user(self, uid: int):
        query = 'INSERT INTO `members` (`id`) VALUES ({uid})'
        
        self.execute_query(query.format(uid=uid))
