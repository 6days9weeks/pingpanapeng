import discord 
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import re
import asyncio
import sys
import traceback

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

class JailCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
    
    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def tjail(self, ctx, member:discord.Member, *, time:TimeConverter = None):
        """Jails a member for the specified time- time in 2d 10h 3m 2s format ex:
        &mute @Someone 1d"""
        print(1)
        if time == None:
            embed = discord.Embed(
                title= "Error",
                description= "Please specify a time",
                color= 0xffc2ff
            )
            await ctx.send(embed=embed)
            print(2)
        if member == None:
            embed = discord.Embed(
                title= "Error",
                description= "Please specify a member to jail",
                color= 0xffc2ff
            )
            await ctx.send(embed=embed)
            print(3)
        else:
            role = discord.utils.get(ctx.guild.roles, name="horny timeout")
            if role == None:
                role = await ctx.guild.create_role(name="horny timeout")
                for channel in ctx.guild.text_channels:
                    await channel.set_permissions(role, send_messages=False)
                await member.add_roles(role)
                embed = discord.Embed(
                    title= "Jail",
                    description= f"{member.mention} has been jailed by {ctx.message.author.mention} for {time}s",
                    color=0xffc2ff
                )
                await ctx.send(embed=embed)
                print(4)
                embed = discord.Embed(
                    title= "Jail",
                    description= f"You have been jailed in {ctx.guiild.name} by {ctx.author.mention} for {time}",
                    color=0xffc2ff
                )
                await member.send(embed=embed)
                print(5)
            if time:
                await asyncio.sleep(time)
                await member.remove_roles(role)
                print(6)
             
    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error",
                description="You do not have permissions to tempjail members!",
                color=0xffc2ff
            )
            await ctx.send(embed=embed)

    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        if member == None:
            embed = discord.Embed(
                title = "Kick Error",
                description = "Please specify a member!",
                color = 0xffc2ff
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    title = "Kick Error",
                    description = "You can't kick yourself!",
                    color = 0xffc2ff
                )
                await ctx.send(embed = embed)
            else:
                if reason == None:
                    await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No reason proivded.")
                    embed = discord.Embed(
                        title = "Kick",
                        description = f"{member.mention} has been kicked by {ctx.message.author.mention}.",
                        color = 0xffc2ff
                    )
                    await ctx.send(embed = embed)
                else:
                    await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
                    embed = discord.Embed(
                        title = "Kick",
                        description = f"{member.mention} has been kicked by {ctx.message.author.mention} for {reason}",
                        color = 0xffc2ff
                    )
                    await ctx.send(embed = embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **staff** role!",
                color = 0xffc2ff
            )
            await ctx.send(embed = embed, delete_after = 5.0)


    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        if member == None:
            embed = discord.Embed(
                title = "Ban Error",
                description = "Please specify a user!",
                color = 0xffc2ff
            )
            await ctx.send(embed = embed)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    title = "Ban Error",
                    description = "You can't ban yourself!",
                    color = 0xffc2ff
                )
                await ctx.send(embed = embed)
            else:
                if reason == None:
                    await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No Reason Provided.")
                    embed = discord.Embed(
                        title = "Ban",
                        description = f"{member.mention} has been banned by {ctx.message.author.mention}.",
                        color = 0xffc2ff
                    )
                else:
                    await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
                    embed = discord.Embed(
                        title = "Ban",
                        description = f"{member.mention} has been banned by {ctx.message.author.mention} for {reason}",
                        color = 0xffc2ff
                    )
                    await ctx.send(embed = embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **staffr** role!",
                color = 0xffc2ff
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def jail(self, ctx, member : discord.Member = None, *, reason = None):
        if member == None:
            embed = discord.Embed(
                title = "Jail Error",
                description = "Please specify a user!",
                color = 0xffc2ff
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            if member.id == ctx.message.author.id:
                embed = discord.Embed(
                    title = "Jail Error",
                    description = "You can't jail yourself!",
                    color = 0xffc2ff
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                if reason == None:
                    role = discord.utils.get(ctx.guild.roles, name = "horny timeout")
                    await member.add_roles(role)
                    embed = discord.Embed(
                        title = "Jail",
                        description = f"{member.mention} has been jailed by {ctx.message.author.mention}.",
                        color = self.blurple
                    )
                    await ctx.send(embed = embed)

    @jail.error
    async def jail_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "You are missing the **staff** role!",
                color = 0xffc2ff
            )
            await ctx.send(embed = embed)

    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def unjail(self, ctx, member : discord.Member = None):
        if member == None:
            embed = discord.Embed(
                title = "Unmute Error",
                description = "Please specify a user!",
                color = 0xffc2ff
            )
            await ctx.send(embed = embed, delete_after = 5.0)
        else:
            role = discord.utils.get(ctx.guild.roles, name = "horny timeout")
            if role in member.roles:
                await member.remove_roles(role)
                embed = discord.Embed(
                    title = "Unjail",
                    description = f"{member.mention} has been unjailed by {ctx.message.author.mention}.",
                    color = 0xffc2ff
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = "Unjail Error",
                    description = f"{member.mention} is not jailed!",
                    color = 0xffc2ff
                )
                await ctx.send(embed = embed)

    @unjail.error
    async def unjal_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "You are missing the **staff** role!",
                color = 0xffc2ff
            )
            await ctx.send(embed = embed)
            
def setup(bot):
    bot.add_cog(JailCog(bot))
