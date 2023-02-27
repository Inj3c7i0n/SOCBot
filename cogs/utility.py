import requests
import json
import os
import discord
import base64
import datetime
import platform
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Utility(commands.Cog, name='utility'):
	def __init__(self, bot):
		self.bot = bot


	@commands.hybrid_command(
		name='urlscan', 
		description='Scans a url with urlscan.io API'
		)
	@app_commands.describe(url="The url to scan")
	async def urlscan(self, ctx: Context, url: str) -> None:
		try:
			api = os.getenv('URLSCAN_API_KEY')
			headers = {'API-Key':f'{api}','Content-Type':'application/json'}
			data = {"url": "{url}", "visibility": "public"}
			response = requests.post('https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
			embed = discord.Embed()
		except Exception:
			embed = discord.Embed(
				description="An error occured while scanning the URL",
				color=0x9C84EF
			)
			await ctx.send(embed=embed)

	@commands.hybrid_command(
		name='virustotal',
		description='Scan a url with VirusTotal API'
		)
	async def virustotal(self, ctx: Context, url: str) -> None:
		try:
			api = str(os.getenv('VIRUSTOTAL_API_KEY'))
			url_id = base64.urlsafe_b64encode(f"{url}".encode()).decode().strip("=")
			url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
			headers = {
				"accept": "application/json",
				"x-apikey": f"{api}",
			}
			response = requests.get(url, headers=headers)
			data = json.loads(response.text)
			last_scan_date = data['data']['attributes']['last_analysis_date']
			date = datetime.datetime.fromtimestamp(last_scan_date)
			id = data['data']['id']
			submits = data['data']['attributes']['times_submitted']
			mal_scans = data['data']['attributes']['last_analysis_stats']['malicious']
			target = F"https://www.virustotal.com/gui/url/{id}/details"
			embed = discord.Embed(
				title="Virustotal URL Scanner",
				description=f"""
** Full Analysis Link **
{target}""",
				url=f'https://icons.iconarchive.com/icons/hopstarter/malware/256/Search-icon.png',
				color=discord.Color.darker_grey()
			)
			embed.set_thumbnail(
				url='https://icons.iconarchive.com/icons/hopstarter/malware/256/Search-icon.png'
			)
			embed.add_field(
				name="",
				value=f"""```diff
+ Analysis Submissions: {submits}
- Malicious: {mal_scans}
```""",
				inline=False
			)
			embed.add_field(
				name="",
				value=f"""```py
Analysis URL: {url}
```""",
				inline=False
			)
			embed.add_field(
				name="",
				value=f"""```py
Analysis ID: {id}
```""",
				inline=False
			)
			embed.add_field(
				name="",
				value=f"""```css
Last Analysis Date: {date}
```""",
				inline=False
			)
			embed.set_footer(
				icon_url=ctx.author.avatar.url,
				text=f"Analysis requested by {ctx.author.name}"
			)
		except Exception as e:
			embed = discord.Embed(
				description=f"""An API error occurred while scanning the URL
Exception: {e}""",
				color=0x9C84EF
			)
		await ctx.send(embed=embed)


async def setup(bot):
	await bot.add_cog(Utility(bot))
