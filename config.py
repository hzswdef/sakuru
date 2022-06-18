from os import getcwd

MODULES = (
    'events',
    'moderation',
    'lvl',
    'test'
)

PATH = getcwd()

# LVL CONFIG

# 1200 sec., 20 mins | Used to gain EXP to member
VOICE_EXP = 1200

LVLS = {
    10: {'exp': 10000, 'role_id': 852346024168914984},
    9:  {'exp': 4999,  'role_id': 852346822688505896},
    8:  {'exp': 2669,  'role_id': 852346634830217236},
    7:  {'exp': 1337,  'role_id': 852346477702545429},
    6:  {'exp': 666,   'role_id': 852346398388781086},
    5:  {'exp': 322,   'role_id': 852346284664553493},
    4:  {'exp': 100,   'role_id': 852346209548894298},
    3:  {'exp': 50,    'role_id': 852345904342237195},
    2:  {'exp': 25,    'role_id': 852345821500014612},
    1:  {'exp': 10,    'role_id': 852345644722028561},
    0:  {'exp': 0,     'role_id': 876601835450929212}
}