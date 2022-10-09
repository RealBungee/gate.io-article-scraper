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

async def send_message(message):
    channel = client.get_channel(1008802973553537134)
    await channel.send(message)

def run_bot(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever(client.run(TOKEN))
    
