import logging

from config import PATH

class log:
    def __init__(self, debug: bool):
        import os
        from datetime import datetime
        
        self.log_file = f'{datetime.today().strftime("%d_%m_%Y-%H:%M:%S")}.log'
        
        if not os.path.exists(f'{PATH}/log'):
            os.makedirs(f'{PATH}/log')
        
        del os
        del datetime
        
        logging.basicConfig(
            filename=f'{PATH}/log/{self.log_file}', 
            format='[ %(asctime)s ] %(message)s', 
            filemode='w'
        )
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    
    @classmethod
    def _raise(cls, output: str):
        logging.info(output)
    
    
    @classmethod
    def load_env(cls):
        logging.info('load .env')
    
    
    @classmethod
    def load_cog(cls, cog: str, status: bool = True):
        if status:
            logging.info(f'load cogs.{cog}')
        else:
            logging.info(f'unexpected error while loading cogs.{cog}')
    
    
    @classmethod
    def bot_started(cls, debug: bool):
        if not debug:
            logging.info('bot started.')
        else:
            logging.info('bot started. DEBUG MODE!')