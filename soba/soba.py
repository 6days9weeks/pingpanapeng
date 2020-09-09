import discord
from discord.ext import commands, tasks
import asyncio

class CustomStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       

    @tasks.loop(seconds=10)
    async def start_the_status(self):
        await self.bot.change_presence(activity=discord.Game(name=f"type donate to donate"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{bot.guild.member_count}  cuties <3"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Streaming(name=f"soba struggles in life", url="https://twitch.tv/kawaiii0001"))
        await asyncio.sleep(10)
        await self.bot.change_presence(activity=discord.Streaming(name=f"dm for help", url="https://twitch.tv/kawaiii0001"))
        await asyncio.sleep(10)

    @commands.command(name="start")
    async def statusy_start(self, ctx):
       
            self.start_the_status.start()
            await ctx.send("Done! If you experience any problems just run this command again!")



def setup(bot):
    bot.add_cog(CustomStatus(bot))
