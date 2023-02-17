import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="sync",
        description="Symchronizea the slash commands."
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @checks.is_owner()
    async def sync(self, ctx: Context, scope: str) -> None:
        if scope == "global":
            await ctx.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally synchronized.",
                color=0x9C84EF
            )
            await ctx.send(embed=embed)
            return
        elif scope == "guild":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            embed = discord.Embed(
                description="Slash commands have been synchronized in this guild.",
                color=0x9C84EF
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.",
            color=0xE02B2B
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="unsync",
        description="Unsymchronizea the slash commands."
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @checks.is_owner()
    async def unsync(self, ctx: Context, scope: str) -> None:
        if scope == "global":
            cmds = await ctx.bot.tree.sync()
            embed = discord.Embed(
                description=f"{len(cmds)} Slash commands have been globally unsynchronized.",
                color=0x9C84EF
            )
            await ctx.send(embed=embed)
            return
        elif scope == "guild":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            embed = discord.Embed(
                description="Slash commands have been unsynchronized in this guild.",
                color=0x9C84EF
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.",
            color=0xE02B2B
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Load a Cog"
    )
    @app_commands.describe(cog="The name of the Cog to load")
    @checks.is_owner()
    async def load(self, ctx: Context, cog: str) -> None:
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not load the `{cog}` Cog.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully loaded the `{cog}` Cog.",
            color=0x9C84EF
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a Cog"
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @checks.is_owner()
    async def unload(self, ctx: Context, cog: str) -> None:
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not unload the `{cog}` Cog.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully unloaded the `{cog}` Cog.",
            color=0x9C84EF
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a Cog."
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @checks.is_owner()
    async def reload(self, ctx: Context, cog: str) -> None:
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not reload the `{cog}` Cog.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully reloaded the `{cog}` Cog.",
            color=0x9C84EF
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown."
    )
    @checks.is_owner()
    async def shutdown(self, ctx: Context) -> None:
        embed = discord.Embed(
            description="Shutting down. Bye! :wave:",
            color=0x9C84EF
        )
        await ctx.send(embed=embed)
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Owner(bot))
