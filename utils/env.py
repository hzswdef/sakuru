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
            
            if key in ['DEBUG', 'DISPLAY_BOTS']:
                setattr(env, key, True if value == 'True' else False)
            elif key in ['ADMIN', 'GUILD', 'NOTIFY_CHANNEL']:
                setattr(env, key, int(value))
            else:
                setattr(env, key, value)
        return env
    