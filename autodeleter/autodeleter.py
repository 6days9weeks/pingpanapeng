import discord
from discord.ext import commands
import asyncio
from datetime import datetime


class autodeleter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
       

    @commands.Cog.listener()
    async def on_message(self, message):
            if message.channel.id == 757144854265331792:
               
                    await message.delete()


def setup(bot):
    bot.add_cog(autodeleter(bot))

