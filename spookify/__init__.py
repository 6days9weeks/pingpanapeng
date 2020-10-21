from .spookify import SpookyAvatar


def setup(bot):
    bot.add_cog(SpookyAvatar(bot))