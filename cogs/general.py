import discord, aiohttp, os
from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="help",
        description="List all the commands the bot has loaded."
    )
    async def help(self, ctx: Context) -> None:
        prefix = os.getenv("PREFIX")
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0x9C84EF)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition('\n')[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(name=i.capitalize(),
                            value=f'```{help_text}```', inline=False)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="bitcoin",
        description="Gets the current USD Price of Bitcoin."
    )
    async def bitcoin(self, context: Context) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coindesk.com/v1/bpi/currentprice/BTC.json") as request:
                if request.status == 200:
                    data = await request.json(
                        content_type="application/javascript")
                    embed = discord.Embed(
                        title="₿ Bitcoin Price ₿",
                        description=f"The current price is ${data['bpi']['USD']['rate']} :dollar:",
                        color=0x8C84EF
                    )
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later.",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get information about the server."
    )
    async def serverinfo(self, context: Context) -> None:
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">> Displaying [50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{context.guild}",
            color=0x9C84EF
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(
                url=context.guild.icon.url
            )
        embed.add_field(
            name="Server ID",
            value=context.guild.id
        )
        embed.add_field(
            name="Member Count",
            value=context.guild.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {context.guild.created_at}"
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name='test',
        description="Tests"
    )
    async def test(self, ctx: Context) -> None:
        embed = discord.Embed()
        embed.add_field(
            name="",
            value="```ansi"
                  "\u001b[0;40m\u001b[1;32mThat's some cool formatted text right?```"
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
