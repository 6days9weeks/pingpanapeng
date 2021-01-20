import asyncio

import discord
from discord.ext import commands, tasks


class CustomStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.first = None
        self.second = None
        self.third = None
        self.fourth = None

    @tasks.loop(seconds=10)
    async def start_the_status(self):
        await self.bot.change_presence(activity=discord.Game(name=f"{self.first}"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Game(name=f"{self.second}"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Game(name=f"{self.third}"))
        await asyncio.sleep(10)
        await self.bot.change_presence(
            activity=discord.Streaming(
                name=f"{self.fourth}", url="https://twitch.tv/kawaiii0001"
            )
        )
        await asyncio.sleep(10)

    @commands.group(name="statusy", invoke_without_command=True)
    async def status_group(self, ctx):
        embed = discord.Embed(
            title="Change the Bot's Status!",
            description=f"Change the Bot's Status to make it change every 10 Seconds!\n\nAvailable Commands:\n`{self.bot.prefix}statusy start`: Start the Status Changing Process\n`{self.bot.prefix}statusy one`: Set the first status of the bot!\n`{self.bot.prefix}statusy two`: Set the second status of the bot!\n`{self.bot.prefix}statusy three`: Set third first status of the bot!",
            color=self.bot.main_color,
        )
        await ctx.send(embed=embed)

    @status_group.command(name="start")
    async def statusy_start(self, ctx):
        if (
            self.first == None
            or self.second == None
            or self.third == None
            or self.fourth == None
        ):
            await ctx.send("Please set the 4 Status's first!")
        else:
            self.start_the_status.start()
            await ctx.send(
                "Done! If you experience any problems just run this command again!"
            )

    @status_group.command(name="one")
    async def first_set(self, ctx, *, first):
        if first == None:
            await ctx.send("Please choose something to set!")
        else:
            self.first = first
            await ctx.send(f"Set `{first}` as the first status!")

    @status_group.command(name="two")
    async def second_set(self, ctx, *, two):
        if two == None:
            await ctx.send("Please choose something to set!")
        else:
            self.second = two
            await ctx.send(f"Set `{two}` as the second status!")

    @status_group.command(name="three")
    async def third_set(self, ctx, *, three):
        if three == None:
            await ctx.send("Please choose something to set!")
        else:
            self.third = three
            await ctx.send(f"Set `{three}` as the third status!")

    @status_group.command(name="four")
    async def fourth_set(self, ctx, *, four):
        if four == None:
            await ctx.send("Please choose something to set!")
        else:
            self.fourth = four
            await ctx.send(f"Set `{four}` as the fourth status!")


def setup(bot):
    bot.add_cog(CustomStatus(bot))
