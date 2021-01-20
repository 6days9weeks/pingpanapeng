import asyncio
import re

import discord
from discord.ext import commands

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")

time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):

        args = argument.lower()

        matches = re.findall(time_regex, args)

        time = 0

        for v, k in matches:

            try:

                time += time_dict[k] * float(v)

            except KeyError:

                raise commands.BadArgument(
                    "{} is an invalid time-key! h/m/s/d are valid!".format(k)
                )

            except ValueError:

                raise commands.BadArgument("{} is not a number!".format(v))

        return time


class MuteCog(commands.Cog):
    def __init__(self, bot):

        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def tjail(self, ctx, member: discord.Member, *, time: TimeConverter = None):

        """Jails a member for the specified time- time in 2d 10h 3m 2s format ex:

        &mute @Someone 1d"""

        print(1)

        if time == None:

            embed = discord.Embed(
                title="Error", description="Please specify a time", color=0xFFC2FF
            )

            await ctx.send(embed=embed)

            print(2)

        if member == None:

            embed = discord.Embed(
                title="Error",
                description="Please specify a member to jail",
                color=0xFFC2FF,
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
                    title="Jail",
                    description=f"{member.mention} has been jail by {ctx.message.author.mention} for {time}s",
                    color=0xFFC2FF,
                )

                await ctx.send(embed=embed)

                print(4)

                embed = discord.Embed(
                    title="Jailed",
                    description=f"You have been jailed in {ctx.guiild.name} by {ctx.author.mention} for {time}",
                    color=0xFFC2FF,
                )

                await member.send(embed=embed)

                print(5)

            if time:

                await asyncio.sleep(time)

                await member.remove_roles(role)

                print(6)

    @tjail.error
    async def tjail_error(self, ctx, error):

        if isinstance(error, commands.MissingPermissions):

            embed = discord.Embed(
                title="Error",
                description="You do not have permissions to temp-jail members!",
                color=0xFFC2FF,
            )

            await ctx.send(embed=embed)


def setup(bot):

    bot.add_cog(MuteCog(bot))
