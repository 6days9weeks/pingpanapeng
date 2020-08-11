import discord
from discord.ext import commands

class Test1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def how_to(self, ctx):
        embed = discord.Embed(
            title="***How To Use ModMail***",
            description="test",
            color=0xffcff2,
            timestamp=ctx.message.created_at
        )
       await ctx.send(embed=embed)
        
        
def setup(bot):
    bot.add_cog(Test1(bot))
