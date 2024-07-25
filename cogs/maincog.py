# https://www.docker.com/blog/how-to-dockerize-your-python-applications/

from discord.ext import tasks, commands
import datetime
import discord
from lxml import html, etree
import requests
import re
import os

utc = datetime.timezone.utc
time = datetime.time(hour=5, minute=7, tzinfo=utc)
class maincog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.my_task.start()

    def cog_unload(self):
        self.my_task.cancel()

    @tasks.loop(time=time)
    async def my_task(self):
        channel = self.bot.get_channel(int(1234567890)) #put the channel ID here for the daily posting
        date = datetime.now()
        date_str = date.strftime("%Y/%m/%d")
        url = f"https://www.gocomics.com/heathcliff/{date_str}"
        page = requests.get(url)
        tree = html.fromstring(page.content)
        image = etree.tostring((tree.xpath('/html/body/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/div/a/picture/img'))[0])
        link = re.findall(r"http[s]*\S+", image.decode('utf-8'))
        message = link[1].strip("\"")
        os.chdir("./images")
        response = requests.get(url)
        file_name = f"{date.strftime("%Y-%m-%d")}.gif"
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
        os.chdir("..")
        await channel.send(message)

    @commands.command()
    async def sendmessage(self, ctx, *, message: str):
        channel = self.bot.get_channel(int(1234567890)) #put channel ID that you want to be able to send messages to here
        await channel.send(message)

    @commands.command() #need to run $sync on first run so slash commands are activated
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"synced {len(fmt)} commands to current guild")
        return

    @discord.app_commands.command(name="getcomic", description="given a date in the format of YYYY-MM-DD the comic from that date will be displayed")
    async def slash_command(self, interaction: discord.Interaction, date: str):
        channel = self.bot.get_channel(int(1234567890)) #put channel you want the comics to be sent to after a slash command here
        try:
            await channel.send(file=discord.File(f"./images/{date}.gif"))
            await interaction.response.send_message(f"comic for {date}")
        except Exception:
            await interaction.response.send_message(f"no comic exists for {date}")

async def setup(bot):
    await bot.add_cog(maincog(bot), guilds=[discord.Object(id=1234567890)]) #put the server ID that you want the / commands synced to here