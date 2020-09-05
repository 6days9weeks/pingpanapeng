from redbot.core import commands, checks
import discord


class Act(commands.Cog):
    """Description of the cog visible with [p]help Webhooks"""

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def sudo(self, ctx, member: discord.Member, *, msg):
        """
       Send webhooks which look like a user is saying something.
        """

        webhook = await ctx.channel.create_webhook(name="su")
        await webhook.send(content=msg, username=member.name, avatar_url=member.avatar_url)
        await webhook.delete()

        message = ctx.message
        message.author = member
        message.content = msg
        await ctx.message.delete()
