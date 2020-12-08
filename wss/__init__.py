from .socketstats import Wss
import json
def setup(bot):
    bot.add_cog(Wss(bot))
