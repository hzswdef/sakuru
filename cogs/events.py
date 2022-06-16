import discord

from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name='PRXJEK'
            )
        )

        self.bot.log.bot_started(self.bot.env.DEBUG)

async def setup(bot):
    await bot.add_cog(Events(bot))
