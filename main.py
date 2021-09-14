import discord
import random
from discord.ext import commands
import discord.utils 
import asyncio
import os
import json
from config import keys
import keep_alive
import random
import datetime

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

@client.event 
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Glows Videos"))

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

keep_alive.keep_alive()
client.run('token')
