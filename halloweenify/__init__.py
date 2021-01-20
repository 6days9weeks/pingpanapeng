from .halloweenify import Halloweenify


def setup(bot):
    bot.add_cog(Halloweenify(bot))
