import discord
from discord.ext import commands
from discord.ext.commands import Cog
class Helping(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cancelled = False

    @Cog.listener()
    async def on_ready(self):
        print('Bot Help is ready')
    
    @commands.group()
    async def help(self,ctx):
        em = discord.Embed(title=".:. 📌 🧩  `Welcome to My Help Menu`  🧩📌 .:.",
                           description="Use `!help` followed by a command name to get more additional information on a command. For example: `!help covid`.",
                           color=0x9b05ff)
        em.add_field(name="⚙️ : Moderation(7)",
                     value="`ban`,`unban`,`kick`,`mute`, \n `unmute`, `tempban`, `snipe`")
        em.add_field(name="😄 : Fun(3)",
                     value="`meme`,  `image`, `kill`")
        em.add_field(name=":scroll: : General(13)",
                     value=" `animal`, `remind`, `whois`, `define`, `quote`, `emoji`, `covid`, `avatar`, `ping`, `members`, `server`, `calculator`")
        em.add_field(name="📈 : Economy(13)", value="`balance`,`beg`,`deposit`,`give`,`rob`,\n `withdraw`, `slots`, `rps`, `daily`, `dice`, `coinflip`, `number`, `gold-dig`") 
        await ctx.send(embed=em)


   

    @help.command()
    async def ban(self,ctx):
        em = discord.Embed(title="Ban", description="Ban a member from the guild", color=0xff6600)
        em.add_field(name="**Example**", value="!ban @TheMessifan10 being mean")
        await ctx.send(embed=em)

    @help.command()
    async def mute(self,ctx):
        em = discord.Embed(title="Mute", description="mutes a member from the guild", color=0xff6600)
        em.add_field(name="**Example**", value="!mute @TheMessifan10 being mean")
        await ctx.send(embed=em)

    @help.command()
    async def unmute(self,ctx):
        em = discord.Embed(title="Unmute", description="unmutes a member from the guild", color=0xff6600)
        em.add_field(name="**Example**", value="!unmute @TheMessifan10 being mean")
        await ctx.send(embed=em)

    @help.command()
    async def kick(self,ctx):
        em = discord.Embed(title="Kick", description="Kick a member from the guild", color=0xff6600)
        em.add_field(name="**Example**", value="!kick @TheMessifan10 being mean")
        await ctx.send(embed=em)

    @help.command()
    async def tempban(self,ctx):
        em = discord.Embed(title="tempban", description="temporarily ban a member from the guild", color=0xff6600)
        em.add_field(name="**Example**", value="!tempban @TheMessifan10 10s Being Mean")
        await ctx.send(embed=em)

    @help.command()
    async def unban(self,ctx):
        em = discord.Embed(title="unban", description="unbans member", color=0xff6600)
        em.add_field(name="**Example**", value="!unban TheMessifan10#1192")
        await ctx.send(embed=em)

    @help.command()
    async def meme(self,ctx):
        em = discord.Embed(title="meme", description="says a meme", color=discord.Color.purple())
        em.add_field(name="**Example**", value="!meme")
        await ctx.send(embed=em)

    @help.command()
    async def image(self,ctx):
        em = discord.Embed(title="image", description="shows an image from google", color=discord.Color.purple())
        em.add_field(name="**Example**", value="!image dolphin")
        await ctx.send(embed=em)

    @help.command()
    async def animal(self,ctx):
        em = discord.Embed(title="animal_fact", description="tells facts about animals", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!animal_fact cat")
        await ctx.send(embed=em)

    @help.command()
    async def wanted(self,ctx):
        em = discord.Embed(title="wanted", description="puts your pfp on wanted sign", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!wanted @TheMessifan10")
        await ctx.send(embed=em)

    @help.command()
    async def remind(self,ctx):
        em = discord.Embed(title="remind", description="you can set reminders", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!remind 10s idk")
        await ctx.send(embed=em)
    
    @help.command()
    async def whois(self,ctx):
        em = discord.Embed(title="who is", description="tells you some stuff about you and others", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!whois @TheMessifan10")
        await ctx.send(embed=em)

    @help.command()
    async def define(self,ctx):
        em = discord.Embed(title="Define", description="tells you what any word means", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!define bee")
        await ctx.send(embed=em)

    @help.command()
    async def quote(self,ctx):
        em = discord.Embed(title=" quote", description="tells you any quote", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!quote")
        await ctx.send(embed=em)

    @help.command()
    async def emoji(self,ctx):
        em = discord.Embed(title="Emoji", description="the bot says anything you want it in emojis!", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!emoji hi")
        await ctx.send(embed=em)

    @help.command()
    async def covid(self,ctx):
        em = discord.Embed(title="Define", description="tells you how covid is in countries", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!covid USA")
        await ctx.send(embed=em)

    @help.command()
    async def avatar(self,ctx):
        em = discord.Embed(title="Avatar", description="tells you, your/someone elses pfp", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!avatar @TheMessifan10")
        await ctx.send(embed=em)

    @help.command()
    async def ping(self,ctx):
        em = discord.Embed(title="Ping", description="tells you the ping between you running that command and it responding", color=discord.Color.blue())
        em.add_field(name="**Example**", value="!ping")
        await ctx.send(embed=em)

    @help.command()
    async def balance(self,ctx):
        em = discord.Embed(title="Balance", description="tells you your wallet/bank", color=discord.Color.green())
        em.add_field(name="**Example**", value="!balance @TheMessifan10 or !balance")
        await ctx.send(embed=em)

    @help.command()
    async def withdraw(self,ctx):
        em = discord.Embed(title="Withdraw", description="withdraws the amount you want to withdraw", color=discord.Color.green())
        em.add_field(name="**Example**", value="!withdraw 100")
        await ctx.send(embed=em)

    @help.command()
    async def deposit(self,ctx):
        em = discord.Embed(title="Deposit", description="Deposits the amount you want to deposit", color=discord.Color.green())
        em.add_field(name="**Example**", value="!deposit 100")
        await ctx.send(embed=em)

    @help.command()
    async def give(self,ctx):
        em = discord.Embed(title="Give", description="Gives a member the amount you want", color=discord.Color.green())
        em.add_field(name="**Example**", value="!give @TheMessifan10 100")
        await ctx.send(embed=em)

    @help.command()
    async def rob(self,ctx):
        em = discord.Embed(title="Rob", description="Robs someone of your choice", color=discord.Color.green())
        em.add_field(name="**Example**", value="!rob @TheMessifan10")
        await ctx.send(embed=em)

    @help.command()
    async def slots(self,ctx):
        em = discord.Embed(title="slots", description="you can bet the amount of money to have a chance to double it in a slots machine", color=discord.Color.green())
        em.add_field(name="**Example**", value="!slots 100")
        await ctx.send(embed=em)
    
    @help.command()
    async def rps(self, ctx):
      em = discord.Embed(title="rps", description="you can bet the amount of money to have a chance to triple it in a rock paper scissors game", color=discord.Color.green())
      em.add_field(name="**Example**", value="!rps rock 100")
      await ctx.send(embed=em)

    @help.command()
    async def daily(self, ctx):
      em = discord.Embed(title = "daily", description = "you can get a guranteed money from 1-500", color = discord.Color.green())
      await ctx.send(embed = em)
    
    @help.command()
    async def dice(self, ctx):
      em = discord.Embed(title="dice", description = "you can have a chance to triple the amount you wanna bet with a dice", color = discord.Color.green())
      em.add_field(name="**Example**", value="!dice 100")
      await ctx.send(embed=em)

    @help.command()
    async def coinflip(self, ctx):
      em = discord.Embed(title="coinflip", description = "you can have a chance to double the amount you wanna bet with a coinflip", color = discord.Color.green())
      em.add_field(name="**Example**", value="bb!coinflip heads/tails 100")
      await ctx.send(embed=em)

    @help.command()
    async def number(self, ctx):
      em = discord.Embed(title="number", description = "I am thinking of a number between 1-10 if you guess it right you get 5 * the amount you bet", color = discord.Color.green())
      em.add_field(name="**Example**", value="bb!number 8 100")
      await ctx.send(embed=em)

    @help.command(aliases = ['gold-dig'])
    async def daosdifo(self, ctx):
      em = discord.Embed(title="gold-dig", description = "You can gold-dig the richest people in the world and get $1-10,000", color = discord.Color.green())
      em.add_field(name="**Example**", value="bb!gold-dig")
      await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Helping(bot))
