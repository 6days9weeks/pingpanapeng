import discord
from discord.ext import commands

class Test1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def howto(self, ctx):
        embed = discord.Embed(
            title="***How To Use Nezubabey***\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            description="**The commands are explained as followed -**\n**To reply normally:** `nezur` or <@742315489765621763> r\n**To reply anonymously:** `nezuar` or <@742315489765621763> ar\n**To close a thread:** to close without any name or who did it just type `nezuclose silenty ~~reason~~` to close after sometime do `nezuclose in 5m etc`\n**To block a certain person from dming the bot:** `nezublock userid or usermention`\n**To get the loglink of this thread:** `nezuloglink`\n**To check logs of user:** `nezulogs user`\n**To make the bot say something:** `nezusay` only for owner\n**To delete a message:** `nezudelete messageid`\n**To open a thread with a person without them dming the bot:**`nezucontact userid or mention`\n**To get pinged if user replies in thread:** `nezusubscribe`\n**To add an tag:** `nezutags add "tag name" value`\nAny questions? Just Dm or ask me my tag is `chizuru#0001` <@682849186227552266>",
            color=0xffcff2,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text="nezubabey", icon_url="https://cdn.discordapp.com/avatars/742315489765621763/9a5506e8b058381eac96a2bcc327158f.png?size=128")
        await ctx.send(embed=embed)
        
        
def setup(bot):
    bot.add_cog(Test1(bot))
