# bot.py
from ast import parse
import os
import helpers
import discord
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json 



client = discord.Client()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#BOT ON READY 
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    rawData = helpers.getRaw()
    parseData = helpers.getData(rawData)
    # print(json.dumps(jsonArray, indent=2))
    parseData = helpers.removeDuplicates(parseData)
    await helpers.postToChannels(client, parseData)

    print("Light Light shutting down.")               
    await client.close()

#BOT MEMBER JOIN
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Yoooooo {member.name}, free games for you!'
    )

#MESSAGE EVENTS (unused atm)
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'raise-exception':
        raise discord.DiscordException

client.run(TOKEN)