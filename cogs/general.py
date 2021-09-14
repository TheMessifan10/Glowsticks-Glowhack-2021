import discord
from discord.ext import commands
from discord.ext.commands import Cog
from aiohttp import request
import requests
import aiohttp
import random
from config import keys
from config.keys import base_url,api_key_weather
import datetime
import wikipedia
import asyncio
import requests

class General(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cancelled = False

    @Cog.listener()
    async def on_ready(self):
        print('Bot General is ready')

    @commands.command(name="animal")
    async def animal_fact(self,ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala", "raccoon", "kangaroo", "whale"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = discord.Embed(title=f"{animal.title()} fact",
                                          description=data["fact"],
                                          colour=ctx.author.colour)
   
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send("No facts are available for that animal.")

  

    @commands.command(brief="Remind command")
    async def remind(self,ctx, time, *, task):
        def convert(time):
            pos = ['s', 'm', 'h', 'd']
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
            unit = time[-1]
            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2
            return val * time_dict[unit]

        converted_time = convert(time)

        if converted_time == -1:
            await ctx.send("You didn't answer the time correctly")
            return
        elif converted_time == -2:
            await ctx.send("The time must be integer")
            return

        await ctx.send(f"Started reminder for **{task}** and will last **{time}**.")

        await asyncio.sleep(converted_time)
        await ctx.send(f"{ctx.author.mention} your reminder for **{task}** has finished!!")

    @commands.command(brief="Show status of server")
    @commands.is_owner()
    async def status(self,ctx, *args):
        guild = ctx.guild

        no_voice_channels = len(guild.voice_channels)
        no_text_channels = len(guild.text_channels)

        embed = discord.Embed(description="Server Status",
                              colour=discord.Colour.dark_purple())

        emoji_string = ""
        for e in guild.emojis:
            if e.is_usable():
                emoji_string += str(e)
        embed.add_field(name="Custom Emojies",
                        value=emoji_string or "No emojis available", inline=False)

        embed.add_field(name="Server Name", value=guild.name, inline=False)

        embed.add_field(name="# Voice Channels", value=no_voice_channels)

        embed.add_field(name="# Text Channels", value=no_text_channels)

        embed.add_field(name="AFK Channel:", value=guild.afk_channel)
        embed.set_author(name=self.bot.user.name)
        embed.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=embed)

    @commands.command(brief="Search member info")
    async def whois(self,ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
            roles = [role for role in ctx.author.roles]

        else:
            roles = [role for role in member.roles]

        embed = discord.Embed(title=f"{member}", colour=member.colour, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_author(name="User Info: ")
        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="User Name:", value=member.display_name, inline=False)
        embed.add_field(name="Discriminator:", value=member.discriminator, inline=False)
        embed.add_field(name="Current Status:", value=str(member.status).title(), inline=False)
        embed.add_field(name="Current Activity:",
                        value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None",
                        inline=False)
        embed.add_field(name="Created At:", value=member.created_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"),
                        inline=False)
        embed.add_field(name="Joined At:", value=member.joined_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"),
                        inline=False)
        embed.add_field(name=f"Roles [{len(roles)}]", value=" **|** ".join([role.mention for role in roles]),
                        inline=False)
        embed.add_field(name="Top Role:", value=member.top_role, inline=False)
        embed.add_field(name="Bot?:", value=member.bot, inline=False)
        await ctx.send(embed=embed)
        return



    @commands.command(helpinfo='Wikipedia summary', aliases=['wiki'])
    async def define(self,ctx, *, query: str):
        '''
        Uses Wikipedia APIs to summarise search
        '''
        sea = requests.get(
            ('https://en.wikipedia.org//w/api.php?action=query'
             '&format=json&list=search&utf8=1&srsearch={}&srlimit=5&srprop='
             ).format(query)).json()['query']

        if sea['searchinfo']['totalhits'] == 0:
            await ctx.send('Sorry, your search could not be found.')
        else:
            for x in range(len(sea['search'])):
                article = sea['search'][x]['title']
                req = requests.get('https://en.wikipedia.org//w/api.php?action=query'
                                   '&utf8=1&redirects&format=json&prop=info|images'
                                   '&inprop=url&titles={}'.format(article)).json()['query']['pages']
                if str(list(req)[0]) != "-1":
                    break
            else:
                await ctx.send('Sorry, your search could not be found.')
                return
            article = req[list(req)[0]]['title']
            arturl = req[list(req)[0]]['fullurl']
            artdesc = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/' + article).json()['extract']
            lastedited = datetime.datetime.strptime(req[list(req)[0]]['touched'], "%Y-%m-%dT%H:%M:%SZ")
            embed = discord.Embed(title='**' + article + '**', url=arturl, description=artdesc, color=0x3FCAFF)
            embed.set_footer(text='Wiki entry last modified',
                             icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
            embed.set_author(name='Wikipedia', url='https://en.wikipedia.org/',
                             icon_url='https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png')
            embed.timestamp = lastedited
            await ctx.send('**Search result for:** ***"{}"***:'.format(query), embed=embed)

    @commands.command()
    async def quote(self,ctx):
        results = requests.get('https://type.fit/api/quotes').json()
        num = random.randint(1, 1500)
        content = results[num]['text']
        em = discord.Embed(title="Quote", description=content, color=0xfffb00)
        await ctx.send(embed=em)

    @commands.command(brief="Your emoji")
    async def emoji(self,ctx, *, text):
        emojis = []
        for s in text.lower():
            if s.isdecimal():
                num2emo = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
                           '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
                emojis.append(f':{num2emo.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)
        await ctx.send(' '.join(emojis))
        await ctx.message.delete()

    @commands.command()
    async def say(self, ctx, message, *, question):
      await ctx.message.delete()
      embed = discord.Embed (
        colour = discord.Colour.red()
      )
      embed.add_field(name= f"{message}" .format(message), value = f"{question}" .format(question))
      await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(General(bot))
