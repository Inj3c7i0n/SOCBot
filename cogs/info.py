import discord
from discord.ext import commands
import datetime
import psutil
import platform
import os
import time


class Info(commands.Cog, name='info'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """Displays information about the bot"""
        embed = discord.Embed(title="Bot Information", color=discord.Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.add_field(name="Bot Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
        embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="System", value=f"{platform.system()} {platform.release()}", inline=True)
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%", inline=True)
        embed.add_field(name="Memory Usage", value=f"{psutil.virtual_memory().percent}%", inline=True)
        embed.add_field(name="Uptime", value=f"{self.get_bot_uptime()}", inline=True)
        await ctx.send(embed=embed)

    def get_bot_uptime(self):
        uptime = int(round(time.time() - psutil.Process(os.getpid()).create_time(), 0))
        uptime_str = str(datetime.timedelta(seconds=uptime))
        return uptime_str


async def setup(bot):
    await bot.add_cog(Info(bot))
