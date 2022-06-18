from config import PATH

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
            
            if key == 'DEBUG':
                setattr(env, key, True if value == 'True' else False)
                continue
            
            if key in ['ADMIN', 'GUILD']:
                setattr(env, key, int(value))
                continue
            
            setattr(env, key, value)
        return env
    