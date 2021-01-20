import json

from .socketstats import Wss


def setup(bot):
    bot.add_cog(Wss(bot))
