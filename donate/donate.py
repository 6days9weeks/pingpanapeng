import discord
from discord.ext import commands
import asyncio
from datetime import datetime


class Donate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot              

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        else:
            if message.channel.id == 751768597239562260:
                if message.content.lower() == "donate":
                    await message.channel.send("hiii")

def setup(bot):
    bot.add_cog(Donate(bot))
