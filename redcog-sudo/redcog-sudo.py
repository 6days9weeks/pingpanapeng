from redbot.core import commands, checks
import discord


class redcog-sudo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

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
        await self.bot.process_commands(message)
        await ctx.message.delete()
