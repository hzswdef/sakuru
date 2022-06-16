import discord

from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send('yolo')


async def setup(bot):
    await bot.add_cog(Test(bot))
