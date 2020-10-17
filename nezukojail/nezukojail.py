import discord 
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import re
import asyncio
import sys
import traceback

class JailCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
    

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
                        color = 0xffc2ff
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
