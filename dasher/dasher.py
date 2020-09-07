import discord
from discord.ext import commands
import asyncio
from datetime import datetime


class Dasher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot              

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        else:
            if message.channel.id == 751768597239562260:
                    await message.add_reaction("\U00002705")
                    await message.add_reaction("\U0000274C")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        else:
            if message.channel.id == 752535585662435329:
                    await message.add_reaction("\U00002705")
                    await message.add_reaction("\U0000274C")

def setup(bot):
    bot.add_cog(Dasher(bot))
