import discord
from discord.ext import commands
import asyncio
from datetime import datetime


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.maincolor = 0x06c9ff
        self.errorcolor = 0xFF0000
        self.log_channel = 708197652545667072  # ID of the log channel
        self.defaultRole = 705764532303167568  # ID of the Discord Member role
       

    @commands.command(name="send-verify")
    @commands.has_permissions(administrator=True)
    async def sendverifymsg(self, ctx):
        embed = discord.Embed(
            title="**Verification**",
            description="To gain access to Chiasa Discord Server, you will have to verify.\n\nVerifying means that you have agreed to our Rules and Guidelines\n\nOur Rules and Guidelines can be found in <#711667049465905302> and check for info on our server <#711667131820933210>!\n\nTo verify, please type `verify` in this channel!",
            color=self.maincolor
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        else:
            if message.channel.id == 705764310109913138:
                if message.content.lower() == "verify":
                    guild = message.guild
                    role = guild.get_role(self.defaultRole)
                   
                   
                    await message.author.add_roles(role)
                    log_channel = guild.get_channel(self.log_channel)
                    await message.add_reaction("\U00002705")
                    embed = discord.Embed(
                        title="Someone just verified!",
                        description=f"{message.author.mention} just verified!\n\nTheir ID is {message.author.id}\n\nAccount created at **{message.author.created_at}**.",
                        color=self.maincolor
                    )
                    await log_channel.send(embed=embed)
                    await asyncio.sleep(2)
                    await message.delete()
                    try:
                        embed = discord.Embed(
                            title="Verification",
                            description="You are now verified in Chiasa Discord Server! Get some roles from <#711673102534181005>",
                            color=self.maincolor
                        )
                        await message.author.send(embed=embed)
                    except:
                        print(f"Couldn't send {message.author.name} his verification acceptation")

                else:
                    await message.delete()
                    return


def setup(bot):
    bot.add_cog(Verify(bot))
