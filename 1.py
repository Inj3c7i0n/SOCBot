import discord
import os
import sys
import asyncio

from discord.ext import commands

TOKEN = "your-bot-token-here"

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def background_task():
    while True:
        for extension in list(bot.extensions):
            try:
                mod_time = os.path.getmtime(f"{extension}.py")
                if mod_time > bot.mod_times[extension]:
                    await bot.reload_extension(extension)
                    print(f"Reloaded {extension}")
                    bot.mod_times[extension] = mod_time
            except KeyError:
                pass
        await asyncio.sleep(5)

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    print(f"Loaded {extension}")

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    print(f"Unloaded {extension}")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    print(f"Reloaded {extension}")

if __name__ == "__main__":
    bot.mod_times = {}
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename[:-3]}")
            bot.mod_times[filename[:-3]] = os.path.getmtime(f"./cogs/{filename}")

    bot.loop.create_task(background_task())
    bot.run(TOKEN)
