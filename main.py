import sys
import asyncio
import discord
import os
import logging
import platform
import re, time, datetime
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

import exceptions

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
prefix = os.getenv('PREFIX')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents, help_command=None, owner_id=315995352010588160)


class LoggingFormatter(logging.Formatter):
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


logger = logging.getLogger("TestingBot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(
    filename="testingbot.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] [{name}]: [{message}]", "%Y-%m-%d %H:%M:%S", style="{")
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
bot.logger = logger


@bot.event
async def on_ready() -> None:
    bot.logger.info("-" * 45)
    bot.logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id}")
    bot.logger.info(f"discord.py API Version: {discord.__version__}")
    bot.logger.info(f"Python Version: {platform.python_version()}")
    bot.logger.info(f"Running on {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info("-" * 45)


async def on_message(message: discord.Message) -> None:
    # don't respond to ourselves
    if message.author == bot.user or message.author.bot:
        return


@bot.event
async def on_command_completion(context: Context) -> None:
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
    else:
        bot.logger.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id} in DM's")


@bot.event
async def on_command_error(ctx: Context, error) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await ctx.send(embed=embed)
    elif isinstance(error, exceptions.UserNotOwner):
        embed = discord.Embed(
            description="You are not the owner of the bot!",
            color=0xE02B2B
        )
        await ctx.send(embed=embed)
        bot.logger.warning(
            f"{ctx.author} (ID: {ctx.author.id}) tried to execute an owner only command in the guild {ctx.guild.name} (ID: {ctx.guild.id}), but the user is not owner of the bot.")
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            description="I am missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to fully perform this command!",
            color=0xE02B2B
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await ctx.send(embed=embed)
    else:
        raise error


async def load_cogs() -> None:
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                bot.logger.info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                bot.logger.error(
                    f"Failed to  load extension {extension}\n{exception}")


asyncio.run(load_cogs())
bot.run(os.getenv('TOKEN'))
