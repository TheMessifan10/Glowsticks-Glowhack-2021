import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
import random
class eightball(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cancelled = False
    @Cog.listener()
    async def on_ready(self):
        print('Bot Eightball is ready')
    @command(aliases=['8ball', '8b'], brief="eightball Q&A")
    async def eightball(self,ctx, *, question):
        responses = [
          "It is certain.",
          "It is decidedly so.",
          "Without a doubt.",
          "Yes - definitely.",
          "You may rely on it.",
          "As I see it, yes.",
          "Most likely.",
          "Outlook good.",
          "Yes.",
          "Signs point to yes.",
          "Reply hazy, try again.",
          "Ask again later.",
          "Better not tell you now.",
          "Cannot predict now.",
          "Concentrate and ask again.",
          "Don't count on it.",
          "My reply is no.",
          "My sources say no.",
          "Outlook not so good.",
          "Very doubtful."]
            
        embed = discord.Embed (
          title = f"8ball",
          description = f'**Answer:** {random.choice(responses)} \n \n **Question:** {question}',
          colour = discord.Colour.blue()
        )
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(eightball(bot))
