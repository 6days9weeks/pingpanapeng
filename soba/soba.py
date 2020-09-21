import discord
from discord.ext import commands,tasks
import asyncio

class StatusNezuko(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=10)
    async def start_status(self):
        server = self.bot.get_guild(699158208027164723)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{server.member_count} cuties <3"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=f"type donate to donate", url="https://twitch.tv/kawaiii0001"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"buy paid promos"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"ash is mine ~ itsuki"))

    @commands.command(name="status_start")
    async def start_start_cmd(self, ctx):
        self.start_status.start()
        await ctx.send("Done! Re-run this command if it stops working")

def setup(bot):
    bot.add_cog(StatusNezuko(bot))