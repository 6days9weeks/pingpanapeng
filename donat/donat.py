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
           
                if message.content.lower() == "donate":
                   
   
                    embed = discord.Embed(
                    title="Here's the donation link for hope",
                    description=f"{message.author.mention} donate at PayPal.com",
                    color=0xffc2ff
                    )
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Donate(bot))
