import discord
import asyncio
import argparse

import utils.env
import utils.log

from discord.ext import commands
from config import MODULES

env = utils.env.load()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(env.PREFIX),
    intents=discord.Intents.all(),
    help_command=None
)

async def main(args):
    async with bot:
        setattr(bot, 'log', utils.log.log(env.DEBUG, args.quiet))
        setattr(bot, 'env', env)
        bot.log.load_env()
        
        if args.debug:
            try:
                await bot.load_extension('cogs.' + args.debug)
                bot.log.load_cog(args.debug)
            except Exception as err:
                bot.log.load_cog(args.debug, False)
                bot.log._raise(err)
        else:
            for module in MODULES:
                try:
                    await bot.load_extension('cogs.' + module)
                    bot.log.load_cog(module)
                except Exception as err:
                    bot.log.load_cog(module, False)
                    bot.log._raise(err)
        
        await bot.start(bot.env.TOKEN)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discord bot.')
    parser.add_argument('-D', '--debug', default=None, type=str, help='Debug cog. Example "music".')
    parser.add_argument('-q', '--quiet', default=False, type=bool, help='Quiet mode, turn off / on logging, default False. Example - True / False')
    args = parser.parse_args()
    
    asyncio.run(main(args))