import discord
from discord import app_commands
from discord.ext import commands


class CogManagement(commands.Cog, name="cog_management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="load",
        description="Load a Cog",
        hidden=True
    )
    @app_commands.describe(cog="The name of the cog to load")
    @commands.is_owner()
    async def load_cog(self, ctx, cog: str):
        try:
            self.bot.load_extension(cog)
            embed = discord.Embed(
                title="Cog Loaded",
                description=f"The {cog} cog was loaded successfully!",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)
        except commands.ExtensionNotFound:
            embed = discord.Embed(
                title="Cog Load Failed",
                description=f"Could not find the {cog} cog.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        except commands.ExtensionAlreadyLoaded:
            embed = discord.Embed(
                title="Cog Load Failed",
                description=f"The {cog} cog is already loaded.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="unload",
        description="Unload a Cog",
        hidden=True
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @commands.is_owner()
    async def unload_cog(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            embed = discord.Embed(
                title="Cog Unloaded",
                description=f"The {cog} cog was unloaded successfully!",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)
        except commands.ExtensionNotFound:
            embed = discord.Embed(
                title="Cog Unload Failed",
                description=f"Could not find the {cog} cog.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        except commands.ExtensionNotLoaded:
            embed = discord.Embed(
                title="Cog Unload Failed",
                description=f"The {cog} cog is not loaded.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

    @commands.command(
        name="reload",
        description="Reload a Cog",
        hidden=True
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            embed = discord.Embed(
                title="Cog Reloaded",
                description=f"The {cog} cog was reloaded successfully!",
                color=0x00FF00,
            )
            await ctx.send(embed=embed)
        except commands.ExtensionNotFound:
            embed = discord.Embed(
                title="Cog Reload Failed",
                description=f"Could not find the {cog} cog.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)
        except commands.ExtensionNotLoaded:
            embed = discord.Embed(
                title="Cog Reload Failed",
                description=f"The {cog} cog is not loaded.",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CogManagement(bot))
