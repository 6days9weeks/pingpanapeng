from .pickup import PickupLine


def setup(bot):
    bot.add_cog(PickupLine(bot))
