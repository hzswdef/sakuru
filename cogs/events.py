import discord

from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name='PRXJEK'
            )
        )

        self.log.bot_started(self.bot.env.DEBUG)
    
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(self.bot.env.PREFIX):
            try:
                command = message.content.split()[0].split(self.bot.env.PREFIX)[1]
            except:
                command = None
            
            bot_commands = [
                *[_.name for _ in self.bot.commands],
                *sum([[a for a in _.aliases] for _ in self.bot.commands], [])
            ]
            
            if command in bot_commands:
                self.log.command(
                    message.author.id,
                    f'{message.author.name}#{message.author.discriminator}',
                    message.content
                )


async def setup(bot):
    await bot.add_cog(Events(bot))
