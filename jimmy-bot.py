import discord
from discord.ext import commands

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    prefix = "$"

    client = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True, self_bot=True)
    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        await client.load_extension("cogs.maincog")
    client.run('BOT-TOKEN-HERE')

if __name__ == "__main__":
    run()