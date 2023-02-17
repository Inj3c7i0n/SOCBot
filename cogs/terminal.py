import os
import whois
import discord
import socket
import requests
from discord.ext import commands
from discord.ext.commands import Context


class Terminal(commands.Cog, name="terminal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='ping',
        description="Ping(send ICMP ECHO_REQUEST) to network hosts(IP or URL)."
    )
    async def ping(self, ctx: Context, target):
        try:
            ip = socket.gethostbyname(target)
            result = os.popen(f"ping -c 3 {target}").read()
            lines = result.split('\n')
            latencies = [line.split("time=")[1].split(" ms")[0] for line in lines if "time=" in line]
            packets_tx = [line.split(",")[1].split(" ")[-2] for line in lines if "transmitted" in line]
            packets_rx = [line.split(",")[1].split(" ")[-2] for line in lines if "received" in line]
            response = requests.get(f"http://{target}")
            status_code = response.status_code
            embed = discord.Embed(
                title="Ping results",
                color=discord.Color.gold()
            )
            embed.add_field(
                name="",
                value=f"""```py
from, {target}                    {latencies[0]} ms
from, {target}                    {latencies[1]} ms
from, {target}                    {latencies[2]} ms```""",
                inline=False
            )
            embed.add_field(
                name="",
                value=f"""```py
--- {target} ping statistics ---
{packets_tx[0]} packets transmitted, {packets_rx[0]} packets received
IP Address: {ip}
Status Code: {status_code}```""",
                inline=False
            )
            await ctx.send(embed=embed)
            return
        except Exception as e:
            embed = discord.Embed(
                description=f"An error occurred while pinging {target}: {e}",
                color=0x9C84EF
            )
        await ctx.send(embed=embed)

    class Whois(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

    @commands.hybrid_command(
        name="whois",
        description="Used to query databases for registered users of an Internet resource."
    )
    async def whois(self, ctx: Context, domain):
        try:
            result = whois.whois(domain)
            embed = discord.Embed(
                title=f"**Information for domain** {domain}:",
                color=discord.Color.gold()
            )
            embed.add_field(
                name="Registrar:",
                value=result.registrar
            )
            embed.add_field(
                name="Creation date:",
                value=result.creation_date
            )
            embed.add_field(
                name="Expiration date:",
                value=result.expiration_date
            )
            embed.add_field(
                name="Name servers:",
                value=f"""```{result.name_servers}```""",
                inline=False
            )
            await ctx.send(embed=embed)
            return
        except Exception as e:
            embed = discord.Embed(
                description=f"An error occurred while retrieving whois information for {domain}: {e}",
                color=0x9C84EF
            )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Terminal(bot))
