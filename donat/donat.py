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
                    title="donations~!",
                    description=f"<a:NezukoRun3NH:709587712084017273>  thank you for choosing to donate to nezuko hideout~! <a:NezukoYayNH:709593706432430231>\n\n<a:NezukoRun3NH:709587712084017273>  all your donations will fully be used for the server only unless you specify!\n\n<a:NezukoRun3NH:709587712084017273> donations will currently go to:\n         <a:NH_NezukoBored:709585865705259079> buying mimu premium (goal not met)\n         <a:NH_NezukoBored:709585865705259079> paying affiliate managers\n         <a:NH_NezukoBored:709585865705259079> bot hosting for modmail\n\n<a:NezukoRun3NH:709587712084017273> donate via paypal to nezuko hideout by clicking [here](https://paypal.me/NezukoHideout)~\n\n<:NHonly_z_N:752130256143646730>  please specify which tier you're paying for in paypal~ \n<:NHonly_y_E:752130280105574470>  $5 = <@&752324984340480111>\n<:NHonly_x_Z:752130306881880114> $10 = <@&752323907050274896>\n<:NHonly_w_U:752130334098980864> $20 = <@&752327555175940227>\n<:NHonly_v_K:752130449811177512> $30 = <@&752352437846802482>\n<:NHonly_u_O:752130470120128592> + add on donations\n\nmore details in <#752318300482043974> ! \n\n***all your donations are greatly appreciated, thankq so much!***  \n\n\nyou can see the current list of donors in <#752329148793487490> <:NH_NezukoHeart:728468706178367549>",
                    color=0xffc2ff
                    )
                    embed.set_thumbnail(url=message.author.avatar_url)
                    await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Donate(bot))
