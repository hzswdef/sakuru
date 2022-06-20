import discord

import utils.welcome

from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send('yolo')
    
    
    @commands.command()
    @commands.is_owner()
    async def newbee(self, ctx: commands.Context):
        guild = self.bot.get_guild(self.bot.env.GUILD)
        
        for member in guild.members:
            await utils.welcome.Welcome(self.bot, member, debug=ctx.channel.id).welcome()


async def setup(bot):
    await bot.add_cog(Test(bot))
