from .webhooks import Webhooks


def setup(bot):
    bot.add_cog(Webhooks())
