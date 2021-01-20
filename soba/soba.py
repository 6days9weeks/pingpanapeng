import asyncio

import discord
from discord.ext import commands, tasks


class StatusNezuko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=10)
    async def start_status(self):
        server = self.bot.get_guild(703455306272735313)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{server.member_count} Cuties <3",
            )
        )
        await asyncio.sleep(10)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.streaming,
                name=f"Type Donate To Donate",
                url="https://twitch.tv/kawaiii0001",
            )
        )
        await asyncio.sleep(10)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing, name=f"Buy Paid Promos"
            )
        )
        await asyncio.sleep(10)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"Soba is mine - ឵឵❥sasha"
            )
        )
        await asyncio.sleep(10)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"Nezuko Hideout | DM For Help | {server.member_count} Members",
            )
        )
        await asyncio.sleep(5)

    @commands.command(name="ss")
    async def start_start_cmd(self, ctx):
        self.start_status.start()
        await ctx.send("Done! Re-run this command if it stops working")


def setup(bot):
    bot.add_cog(StatusNezuko(bot))
