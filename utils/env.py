from config import PATH

class ENV_VALUE_ERROR(Exception):
    pass

class _env(object):
    def __init__(self):
        pass

def load():
    env = _env()
    
    with open(f'{PATH}/.env') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            
            if value == '' or value == ' ':
                raise ENV_VALUE_ERROR
            
            if key in ['DEBUG', 'DISPLAY_BOTS']:
                setattr(env, key, True if value == 'True' else False)
            elif key in ['ADMIN', 'GUILD', 'NOTIFY_CHANNEL', 'NEWBEE_CHANNEL']:
                setattr(env, key, int(value))
            else:
                setattr(env, key, value)
        return env

def check_env():
    try:
        env = load()
    except Exception as err:
        print(f"Invalid .env file\n\n{err}")
        
        import sys
        sys.exit()
    
    import pymysql
    from pymysql.cursors import DictCursor
    
    try:
        pymysql.connect(
            host=env.HOST,
            user=env.USER,
            password=env.PASS,
            db=env.DATABASE,
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True
        )
    except Exception as err:
        print(f'Couldn\'t connect to MySQL. Be sure your MySQL login data is correct and MySQL Server is up.\n\n{err}')
        
        import sys
        sys.exit()
    