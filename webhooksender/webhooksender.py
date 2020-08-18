from discord.ext import commands as commands
from core import checks
import discord
from core.models import PermissionLevel


class WebhookSender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @commands.command()
    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
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
def setup(bot):
    bot.add_cog(WebhookSender(bot))
