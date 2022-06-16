import discord

import objects.color

from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

color = objects.color.color()


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(aliases=['c', 'cls', 'purge'])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int = 1):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        
        await ctx.channel.send(
            embed=discord.Embed(
                description=f'** Deleted {amount} messages.**',
                color=color.BLACK
            ),
            delete_after=3
        )
    
    
    @commands.command(aliases=['b'])
    @has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        if member.mention == ctx.author.mention:
            return await ctx.send(embed=discord.Embed(
                description=f'** {ctx.author.name}, you cannot ban yourself.**',
                color=color.BLACK
            ))
      
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned.')
    
    
    @commands.command(aliases=['k'])
    @has_permissions(ban_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason=None):
        if member.mention == ctx.author.mention:
            return await ctx.send(embed=discord.Embed(
                description=f'** {ctx.author.name}, you cannot kick yourself.**',
                color=color.BLACK
            ))
    
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kick.')
    
    
    @commands.command()
    @has_permissions(ban_members=True)
    async def mute(self, ctx: commands.Context, user: discord.Member):
        if ctx.guild.id == 789106846400643083:
            try:
                role = discord.utils.find(lambda r: r.name == 'MUTED', ctx.message.guild.roles)
            
                if role in user.roles:
                    await user.remove_roles(role)
                    await ctx.send(embed=discord.Embed(
                        description=f'** {user.name} has been unmuted.**',
                        color=color.BLACK
                    ))
                else:
                    await user.add_roles(role)
                    await ctx.send(embed=discord.Embed(
                        description=f'** {user.name} has been muted.**',
                        color=color.BLACK
                    ))
            except:
                await ctx.send(embed=discord.Embed(
                    description=f'** {user.name} something went wrong, try `??mute @user#0001`.**',
                    color=color.BLACK
                ))
    
    
    
    @ban.error
    @kick.error
    @mute.error
    @clear.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return await ctx.send(embed=discord.Embed(
                description=f'** {ctx.author.name}, you dont have permissions.**',
                color=0x0c0c0c
            ))
            
        return await ctx.send(embed=discord.Embed(
            description=f'** Unexpected error, please contact <@{self.bot.env.ADMIN}>.**\n\n```{error}\n```',
            color=0x0c0c0c
        ))


async def setup(bot):
    await bot.add_cog(Moderation(bot))