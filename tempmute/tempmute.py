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

class MuteCog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot    

    

    @commands.command()

    @checks.has_permissions(PermissionLevel.MODERATOR)

    async def tempmute(self, ctx, member:discord.Member, *, time:TimeConverter = None):

        """Mutes a member for the specified time- time in 2d 10h 3m 2s format ex:

        &mute @Someone 1d"""

        print(1)

        if time == None:

            embed = discord.Embed(

                title= "Error",

                description= "Please specify a time",

                color= 0xFF0000

            )

            await ctx.send(embed=embed)

            print(2)

        if member == None:

            embed = discord.Embed(

                title= "Error",

                description= "Please specify a member to mute",

                color= 0xFF0000

            )

            await ctx.send(embed=embed)

            print(3)

        else:

            role = discord.utils.get(ctx.guild.roles, name="yu-mute")

            if role == None:

                role = await ctx.guild.create_role(name="yu-mute")

                for channel in ctx.guild.text_channels:

                    await channel.set_permissions(role, send_messages=False)

                await member.add_roles(role)

                embed = discord.Embed(

                    title= "Mute",

                    description= f"{member.mention} has been muted by {ctx.message.author.mention} for {time}s",

                    color=0x00FF00

                )

                await ctx.send(embed=embed)

                print(4)

                embed = discord.Embed(

                    title= "Muted",

                    description= f"You have been muted in {ctx.guiild.name} by {ctx.author.mention} for {time}",

                    color=0x06c9ff

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

                description="You do not have permissions to tempmute members!",

                color=0xFF0000

            )

            await ctx.send(embed=embed)

            

def setup(bot):

    bot.add_cog(MuteCog(bot))
