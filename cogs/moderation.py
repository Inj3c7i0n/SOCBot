import datetime
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context


class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="purge",
        description="Purge old messages from the channel."
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: Context, amount: int):
        await ctx.channel.purge(limit=amount)
        embed = Embed(timestamp=datetime.datetime.now())
        embed.add_field(name="", value=f"{amount} messages were purged from #{ctx.channel.name}.")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
