# bot.py
import asyncio
import discord

TOKEN = 'MTAwMTgyNjYzMDEwNjM2MTk2Ng.GeTYoY.aYSub_OpCIk3Hg3BtVAZU9rz00o6noYUtdf7KA'
GUILD = '994952384642043974'

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

async def send_message():
    channel = client.get_channel(1006153987629789216)
    await channel.send("msg")

async def run_bot():
    try:
        await client.start(TOKEN)
    except Exception as e:
        await client.close()

def start_discord_bot():
    asyncio.run(run_bot())
