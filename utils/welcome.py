import requests

from discord import File
from requests import get
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

from config import PATH


class Build(object):
    def __init__(self):
        pass
    
    
    def build_mask(self, size):
        mask_size = (size[0] * 3, size[1] * 3)
        
        mask = Image.new('L', mask_size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + mask_size, fill=255)
        mask = mask.resize(size, Image.ANTIALIAS)
    
        return mask
    
    
    def build_image(
        self,
        mention: tuple,
        avatar_url: str,
        members_count: int # guild members count
    ):
        image = Image.open(f'{PATH}/assets/background.png')
        text = ImageDraw.Draw(image)
        
        # download and resize member avatar
        avatar = Image.open(
            get(avatar_url, stream=True).raw if avatar_url else f'{PATH}/assets/no_avatar.png'
        ).resize(
            (400, 400),
            Image.ANTIALIAS
        )
        
        # put avatar in eclipse mask
        mask = self.build_mask(avatar.size)
        avatar.putalpha(mask)
        
        image.paste(
            avatar,
            (50, 50), # x, y pos
            mask=mask
        )
        
        font_light = ImageFont.truetype(
            f'{PATH}/assets/fonts/Dongle-Light.ttf',
            size=96
        )
        font_regular = ImageFont.truetype(
            f'{PATH}/assets/fonts/Dongle-Regular.ttf',
            size=128
        )
        
        text.text(
            (60, image.size[1] - 210),
            f'Member #{members_count}',
            font=font_light,
            fill='#9c9c9c' # gray color
        )
        text.text(
            (60, image.size[1] - 150),
            f'{mention[0]}#{mention[1]} joined to party',
            font=font_regular,
            fill='#ffffff'
        )
        
        return image


class Welcome(Build):
    def __init__(self, bot, user, debug=False):
        super(Welcome, self).__init__()
        self.bot = bot
        self.user = user
        self.debug = debug
    
    
    async def welcome(self):
        image = self.build_image(
            (self.user.name, self.user.discriminator),
            self.user.avatar,
            len(self.bot.get_guild(self.bot.env.GUILD).members)
        )
        
        await self.send_msg(image)
    
    
    async def send_msg(self, image):
        with BytesIO() as img:
            image.save(img, 'PNG')
            img.seek(0)
            
            file = File(img, 'newbee.png')
            
            if self.debug:
                channel = await self.bot.fetch_channel(self.debug)
                return await channel.send('debug', file=file)
            
            channel = await self.bot.fetch_channel(self.bot.env.NEWBEE_CHANNEL)
            await channel.send(file=file)
