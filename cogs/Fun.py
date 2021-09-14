from discord.ext import commands
from discord.ext.commands import Cog
from utils.economysys import open_account,update_bank
import random
from random import randint
from googleapiclient.discovery import build
import discord
from config.keys import api_key_giphy,api_instance
import aiohttp
from PIL import Image
from io import BytesIO
class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cancelled = False


    

    @commands.command(aliases=['show'], brief="search image what you want with google")
    async def image(self,ctx, *, search):
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey='AIzaSyDS-PsjhyUt-Sgypn8muoa8DC3giGQEE7A').cse()
        result = resource.list(
            q=f"{search}", cx="115ee45d46b90cbab", searchType="image").execute()
        url = result["items"][ran]["link"]
        embed1 = discord.Embed(title=f"Here Your Image ({search.title()})")
        embed1.set_image(url=url)
        await ctx.send(embed=embed1)

    @commands.command(helpinfo='Be an assassin')
    async def kill(self,ctx, *, user='You'):
        '''
        Kills the player, minecraft style
        '''
        await ctx.channel.send((user) + ' fell out of the world')

    @commands.command(brief="Meme command")
    async def meme(self,ctx):
        async with aiohttp.ClientSession()as cs:
            async with cs.get("https://www.reddit.com/r/dankmemes.json") as r:
                memes = await r.json()
                embed = discord.Embed(
                    color=discord.Colour.purple()
                )
                embed.set_image(url=memes["data"]["children"][random.randint(0, 25)]["data"]["url"])
                embed.set_footer(text=f"Powered by r/dankmemes! | Meme requestes by {ctx.author}")
                await ctx.send(embed=embed)

    @commands.command()
    async def wanted(self,ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author

        wanted = Image.open("data/wanted.png")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        profilepic = Image.open(data)

        profilepic = profilepic.resize((300, 300))

        wanted.paste(profilepic, (78, 219))
        wanted.save("data/wantedpic.png")

        await ctx.send(file=discord.File("data/wantedpic.png"))
    
    


    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Fun is ready')


def setup(bot):
    bot.add_cog(Fun(bot))
