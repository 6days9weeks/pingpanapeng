import discord
from discord.ext import commands

class Prune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(aliases = ["clear"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def purge(self, ctx, amount = 10):
        max_purge = 2000
        if amount >= 1 and amount <= max_purge:
            await ctx.channel.purge(limit = amount + 1)
            embed = discord.Embed(
                title = "Purge",
                description = f"Purged {amount} message(s)!",
                color = self.blurple
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
            if modlog == None:
                return
            if modlog != None:
                embed = discord.Embed(
                    title = "Purge",
                    description = f"{amount} message(s) have been purged by {ctx.author.mention} in {ctx.message.channel.mention}",
                    color = self.blurple
                )
                await modlog.send(embed = embed)
        if amount < 1:
            embed = discord.Embed(
                title = "Purge Error",
                description = f"You must purge more then {amount} message(s)!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()
        if amount > max_purge:
            embed = discord.Embed(
                title = "Purge Error",
                description = f"You must purge less then {amount} messages!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()
def setup(bot):
    bot.add_cog(Prune(bot))
