import discord

import utils.database
import objects.color

from discord.ext import commands
from datetime import datetime
from re import findall

from config import VOICE_EXP, LVLS

color = objects.color.color()


class LvlSystem(utils.database.Lvl):
    def __init__(self, bot):
        super(LvlSystem, self).__init__()
        self.bot = bot
    
    
    @staticmethod
    def current_lvl(exp: int):
        for lvl, data in LVLS.items():
            if exp <= data['exp']:
                continue
            return lvl
    
    
    @staticmethod
    def lvl_up(exp: int, prev_exp: int=-1):
        """
        if member has lvl up - return hes new lvl number 
        else return False
        
        Note prev_exp specified for handle voice EXP
        """
        
        for lvl, data in LVLS.items():
            if exp == data['exp']:
                return lvl
            
            if prev_exp != -1:
                if exp >= data['exp'] and prev_exp < data['exp']:
                    return lvl
        
        return False
    
    
    @staticmethod
    def get_role_id(lvl: int):
        """ return LVL role ID """
        
        for _lvl, data in LVLS.items():
            if lvl == _lvl:
                return data['role_id']
    
    
    async def add_msg_exp(self, uid: int, bot: bool):
        if not self.user_exists(uid):
            self.add_user(uid, bot)
        
        self.add_exp(uid)
        
        if lvl := self.lvl_up(self.get_user_exp(uid)):
            await self.congrats(uid, lvl)
        
    
    async def add_voice_exp(self, uid: int, time: int, bot: bool):
        if not self.user_exists(uid):
            self.add_user(uid, bot)
        
        prev_exp = self.get_user_exp(uid)
        
        self.add_exp(uid, time=time)
        
        if lvl := self.lvl_up(self.get_user_exp(uid) + (time // VOICE_EXP), prev_exp=prev_exp):
            await self.congrats(uid, lvl)
    
    
    async def congrats(self, uid: int, lvl: int):
        guild = self.bot.get_guild(self.bot.env.GUILD)
        
        # Remove prev lvl role then add next lvl role
        member = guild.get_member(uid)
        await member.remove_roles(guild.get_role(self.get_role_id(lvl - 1)))
        await member.add_roles(guild.get_role(self.get_role_id(lvl)))
        
        channel = await guild.fetch_channel(self.bot.env.NOTIFY_CHANNEL)
        await channel.send(
            content=f'<@{uid}>',
            embed=discord.Embed(
                color=color.BLACK,
                title='Congratulations!',
                description=f'Reached **Level {lvl}**.'
            )
        )


class Lvl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log
        self.lvl = LvlSystem(bot)
        
        self.voice_active = dict()
    
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id != self.bot.env.GUILD:
            return
        
        # Grant user 1 EXP
        await self.lvl.add_msg_exp(message.author.id, message.author.bot)
    
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, b, a):
        uid = member.id
        
        # Save member DiscordID and current timestamp when user join the voice channel
        if a.channel != None and b.channel == None:
            self.voice_active[uid] = datetime.now().timestamp()
            
            self.log.info(f'{member.name} join to {a.channel.name}.')
        
        # Grant member EXP when he leaves from voice channel
        if a.channel == None and b.channel != None:
            if uid not in self.voice_active.keys():
                return
            
            time_in_vc = datetime.now().timestamp() - self.voice_active[uid]
            
            await self.lvl.add_voice_exp(uid, time_in_vc, member.bot)
            
            del self.voice_active[member.id]
        
            self.log.info(f'{member.name} leave from {b.channel.name}.')
    
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(self.bot.env.GUILD)
        uid = member.id
        
        if self.user_exists(uid):
            lvl = self.lvl.current_lvl(self.lvl.get_user_exp(uid))
            
            return await member.add_roles(guild.get_role(self.lvl.get_role_id(lvl)))
        
        await member.add_roles(guild.get_role(self.lvl.get_role_id(0)))
    
    
    @commands.command()
    async def lvl(self, ctx: commands.Context, user=None):
        if user:
            try:
                user = await self.bot.fetch_user(findall('\d+', user)[0])
            except Exception as err:
                return await ctx.send(f'Unexpected error. Try invoke command again by `{self.bot.env.PREFIX}{ctx.command} @.dmg#1272`.', delete_after=3600)
        else:
            user = ctx.author
        
        if not self.lvl.user_exists(user.id):
            return await ctx.send(f'{user.mention} doesn\'t exists in database.')
        
        data = self.lvl.get_user_data(user.id)
        
        exp = self.lvl.get_user_exp(user.id)
        lvl = self.lvl.current_lvl(exp)
        
        exp_to_next_lvl = 0 if lvl == list(LVLS.keys())[0] else LVLS[lvl+1]['exp']
        
        user_pos = self.lvl.get_user_pos(user.id)
        users_count = self.lvl.get_users_count()
        
        embed = discord.Embed(
            color=color.BLACK,
            title=f'User Stats  -  {user.name}',
        ).add_field(
            name=f'{lvl} lvl',
            value=f'{exp}exp  **/**  {exp_to_next_lvl}exp'
        ).add_field(
            name='Voice',
            value=f'{data["voice"] // VOICE_EXP}h, {data["voice"] % 60}m'
        ).set_thumbnail(
            url=user.avatar
        ).set_footer(
            text=f'top #{user_pos} / {users_count}'
        )
        
        await ctx.send(embed=embed)
    
    
    @commands.command()
    async def top(self, ctx: commands.Context, count: int=10):
        if count <= 0:
            return await ctx.send('Seriously?')
        
        await ctx.channel.typing()
        
        users = self.lvl.get_top_users(count)
        
        top = []
        for i, user in enumerate(users):
            discord_user = await self.bot.fetch_user(user['id'])
            username = discord_user.name + '#' + discord_user.discriminator
            
            exp = self.lvl.get_user_exp(user['id'])
            
            msg = '**{index}.** {username}  -  {exp}exp, {hh}h {mm}m'
            
            top.append(msg.format(
                index=i+1,
                username=username,
                exp=exp,
                hh=user["voice"] // VOICE_EXP,
                mm=user["voice"] % 60
            ))
        
        await ctx.send(embed=discord.Embed(
            color=color.BLACK,
            title=f'Top {len(users)} members.',
            description='\n'.join(top)
        ))


async def setup(bot):
    await bot.add_cog(Lvl(bot))
