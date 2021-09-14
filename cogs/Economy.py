import discord
import random
from discord.ext import commands
from utils.economysys import open_account,get_bank_data,update_bank
from discord.ext.commands import Cog
import json

import random
from discord_buttons_plugin import *
class Economy(Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      print('Bot Economy is ready')


    @commands.command(aliases=['bal'], brief="Check your balance money")
    async def balance(self,ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        await open_account(member)

        users = await get_bank_data()
        user = member
        wallet_amount = users[str(user.id)]["wallet"]
        bank_amount = users[str(user.id)]["bank"]
        embed = discord.Embed(title=f"{member.name}'s Balance", color=discord.Color.green())
        embed.add_field(name="Wallet", value=wallet_amount)
        embed.add_field(name="Bank", value=bank_amount)
        await ctx.send(embed=embed)

    @commands.command(brief="Get money for saying command daily")
    @commands.cooldown(1, 86400, commands.cooldowns.BucketType.user)
    async def daily(self,ctx):
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(500)

        embed = discord.Embed(
          title = "Daily",
          description = f"You Got ${earnings} for today"
        )
        await ctx.send(embed=embed)
        
        users[str(user.id)]["wallet"] += earnings
        with open("data/bank.json", "w") as f:
          json.dump(users, f, indent=4)


    @commands.command(aliases=['with'], brief="Withdraw your money")
    async def withdraw(self,ctx, amount=None):
        await open_account(ctx.author)
        if amount == None:
            embed = discord.Embed(
              title="Withdraw Error",
              description = "Please Enter An Amount You Would Like To Withdraw",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[1]
        elif amount == "max":
            amount = bal[1]

        amount = int(amount)
        if amount < 0:
            embed = discord.Embed(
              title="Withdraw Error",
              description = "Amount must be larger than 0",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed = embed)
        if amount > bal[1]:
            embed = discord.Embed(
              title="Withdraw Error",
              description = "You Do Not Have Enough Money",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed = embed)

        await update_bank(ctx.author, amount, "wallet")
        await update_bank(ctx.author, -1 * amount, "bank")

        embed = discord.Embed(
          title = "Withdraw",
          description = f"You Withdrew ${amount}",
          colour = discord.Colour.green()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['dep'], brief="Deposit your money")
    async def deposit(self,ctx, amount=None):
        await open_account(ctx.author)
        if amount == None:
            embed = discord.Embed(
              title="Deposit Error",
              description = "Please Enter An Amount You Would Like To Deposit",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[0]
        elif amount == "max":
            amount = bal[0]

        amount = int(amount)
        if amount < 0:
            embed = discord.Embed(
              title="Deposit Error",
              description = "Amount must be larger than 0",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        if amount > bal[0]:
            embed = discord.Embed(
              title="Deposit Error",
              description = "You do not have enough money",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)

        await update_bank(ctx.author, -1 * amount, "wallet")
        await update_bank(ctx.author, amount, "bank")

        embed = discord.Embed(
          title="Deposit",
          description = f"You Deposited {amount}",
          colour = discord.Colour.green()
        )

    @commands.command(aliases=['send'], brief="Give your money to your @mention")
    async def give(self,ctx, member: discord.Member, amount=None):
        await open_account(ctx.author)
        if amount == None:
            embed = discord.Embed(
              title="Guive Error",
              description = "Please Enter An Amount You Would Like To Give",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        bal = await update_bank(ctx.author)
        if amount == "all":
            amount = bal[0]
        elif amount == "max":
            amount = bal[0]
        amount = int(amount)
        if amount < 0:
            embed = discord.Embed(
              title="Give Error",
              description = "Amount must be larger than 0",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)
        if amount > bal[0]:
            embed = discord.Embed(
              title="Give Error",
              description = "You Do Not Have Enough Money",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)

        await update_bank(ctx.author, -1 * amount, "wallet")
        await update_bank(member, amount, "wallet")

        embed = discord.Embed(
          title="Give",
          description = f"{ctx.author} gave {member} ${amount}",
          colour = discord.Colour.red()
        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def rob(self, ctx, member: discord.Member=None):
      if member == None:
        embed = discord.Embed(
          title="Rob Error",
          description = "Please Enter Who You Would Like To Rob",
          colour = discord.Colour.red()
        )
      return await ctx.send(embed=embed)
      await open_account(ctx.author)
      await open_account(member)

      bal = await update_bank(member)
      robberBal = await update_bank(ctx.author)
      if robberBal[0] < 150:
            embed = discord.Embed(
              title="Rob Error",
              description = "You Do Not even have $150",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)
      else:
        if bal[0]<150:
            embed = discord.Embed(
              title="Rob Error",
              description = "They Do Not even have $150",
              colour = discord.Colour.red()
            )
            return await ctx.send(embed=embed)

      stolen = random.randrange(-1*(robberBal[0]), bal[0])

      await update_bank(ctx.author, stolen)
      await update_bank(member,-1* stolen)

      if stolen > 0:
        embed = discord.Embed(
          title=f"{member} Got Robbed",
          description=f"{ctx.author} stole ${stolen} from {member}",
          colour = discord.Colour.green()
        )
        await ctx.send(embed=embed)
      elif stolen < 0:
        stolen = stolen*-1
        embed = discord.Embed(
          title = f"Attempted Robbery",
          description = f"{ctx.author} tried to rob {member} but got caught and had to pay ${stolen}",
          colour = discord.Colour.red()
        )
        return await ctx.send(embed=embed)
        

    @commands.command(brief="Begging for money")
    @commands.cooldown(1, 3600, commands.cooldowns.BucketType.user)
    async def beg(self,ctx):
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        earnings = random.randint(10, 100)
        hi = random.randint(0, 2)

        name = [
          '**Bill Nye**',
          '**Donald Trump**',
          '**kim ja un**',
          "**Jeff Beazos**"]

        responses = [
          'stop begging you look like a fool',
          'get a job you hippy',
          'honestly just stop asking for free money']


        if hi == 0:
          embed = discord.Embed(
            color = discord.Color.orange()
          )
          embed.add_field(name=f"{random.choice(name)}", value=f"\n {random.choice(responses)}")
          embed.set_footer(text="imagine begging lol")
          await ctx.send(embed=embed)
          

        if hi == 1:
          embed = discord.Embed(
            color = discord.Color.green()
          )
          embed.add_field(name=f"{random.choice(name)}", value=f"\n oh you poor begger take ${earnings}")
          embed.set_footer(text="Bot Made By TheMessifan10 & WTBudgie")
          await ctx.send(embed=embed)

          users[str(user.id)]["wallet"] += earnings
          with open("data/bank.json", "w") as f:
            json.dump(users, f, indent=4)

        if hi == 2:
          embed = discord.Embed(
            color = discord.Color.red()
          )
          embed.add_field(name=f"{random.choice(name)}", value=f"\n took your donation basket you lost ${earnings}")
          await ctx.send(embed=embed)

          users[str(user.id)]["wallet"] -= earnings
          with open("data/bank.json", "w") as f:
            json.dump(users, f, indent=4)


    @commands.command(aliases = ['gold-dig'])
    @commands.cooldown(1, 86400, commands.cooldowns.BucketType.user)
    async def golddig(self,ctx):
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        earnings = random.randint(1, 10000)
        hi = random.randint(0, 5)

        name = [
          "**Bernard Arnault**",
          "**Jeff Bezos**",
          "**Elon Musk**",
          "**Bill Gates**",
          "**Mark Zuckerberg**",
          "**Warren Buffett**",
          "**Larry Ellison**",
          "**Larry Page**",
          "**Sergey Brin**",
          "**Mukesh Ambani**"]

        gain = [
          f"You gold digged the judge let you keep ${earnings}",
          f"You succeded the gold dig and got ${earnings}",
          f"Your gold dig didn't seem to work out but you secretly pitpocketed ${earnings}"]

        lose = [
          f"Found out you that you gold digged you lost ${earnings}",
          f"Didn't have clue but when you got all of his money, but then he mugged you for all of the money back you lost ${earnings}",
          f"You failed the gold dig and lost ${earnings}"]

        none = [
          "Found out and dumped you immediatly you got/lost nothing",
          "You succeded the gold dig but then right before you won in court he started shooting everyone and you never got your money",
          "You failed the gold dig but then he felt bad and gave you your money back you lost/got nothing"]

        if hi == 0:
          embed = discord.Embed(colour = discord.Colour.green())
          embed.add_field(name = f"{random.choice(name)}", value = f"{random.choice(gain)}")
          await ctx.send(embed = embed)
          
          users[str(user.id)]["wallet"] += earnings
          with open("data/bank.json", "w") as f:
            json.dump(users, f, indent=4)
        
        if hi == 1:
          embed = discord.Embed(colour = discord.Colour.red())
          embed.add_field(name = f"{random.choice(name)}", value = f"{random.choice(lose)}")
          await ctx.send(embed = embed)

          users[str(user.id)]["wallet"] -= earnings
          with open("data/bank.json", "w") as f:
            json.dump(users, f, indent=4)

        if hi == 2:
          embed = discord.Embed(colour = discord.Colour.red())
          embed.add_field(name = f"{random.choice(name)}", value = f"{random.choice(lose)}")
          await ctx.send(embed = embed)

          users[str(user.id)]["wallet"] -= earnings
          with open("data/bank.json", "w") as f:
            json.dump(users, f, indent=4)

        if hi == 3:
          embed = discord.Embed(colour = discord.Colour.red())
          embed.add_field(name = f"{random.choice(name)}", value = f"{random.choice(lose)}")
          await ctx.send(embed = embed)

          users[str(user.id)]["wallet"] -= earnings
          with open("data/bank.json", "w") as f:
            json.dump(users, f, indent=4)

        if hi == 4:
          embed = discord.Embed(colour = discord.Colour.orange())
          embed.add_field(name = f"{random.choice(name)}", value = f"{random.choice(none)}")
          await ctx.send(embed = embed)

        if hi == 5:
          embed = discord.Embed(colour = discord.Colour.orange())
          embed.add_field(name = f"{random.choice(name)}", value = f"{random.choice(none)}")
          await ctx.send(embed = embed)
          

    @commands.command(brief="Play slots to earn money")
    async def slots(self,ctx, amount=None):
        if amount == None:
            embed = discord.Embed(
              title = "Slots Error",
              descripton = "Please Enter An"
            )
            return await ctx.send('Please enter an amount you would like to bet!')

        await open_account(ctx.author)
        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount < 100:
            return await ctx.send('You must bet at least 100 coins')
        else:
            if amount > bal[0]:
                return await ctx.send('You do not have this much money!')
            if amount < 0:
                return await ctx.send('Amount must be positive!')
        final = []
        for i in range(3):
            a = random.choice([':laughing:',':thumbsup:', ':white_check_mark:'])
            final.append(a)
        em = discord.Embed(title=f"{ctx.author.name}'s Slots Game", color=discord.Color.green())
        em.add_field(name="Your slots game", value=str(final))
        await ctx.send(embed=em)

        if final[0] == final[1] == final[2]:
            await update_bank(ctx.author, 3 * amount)
            await ctx.send('You won all 3 slots you double you money!!!')
        elif final[0] == final[1] or final[1] == final[2] or final[2] == final[0]:
            await ctx.send('You won all 2 slots your money stays the same!!!')
        else:
            await update_bank(ctx.author, -1 * amount)
            await ctx.send('Sorry,You lost all slots !!!')
    
    @commands.command()
    async def coinflip(self, ctx, message, amount=None):
      if amount == None:
        return await ctx.send('Please enter an amount you would like to bet')
      await open_account(ctx.author)
      bal = await update_bank(ctx.author)

      amount = int(amount)
      if amount < 100:
        return await ctx.send('dont be shy put some more')
      else:
        if amount > bal[0]:
          return await ctx.send('You dont have enough money you broke boy')
        if amount < 0:
          return await ctx.send('Amount must be positive!')
        answer = message.lower()
        choices = ["heads", "tails"]
        aianswer = random.choice(choices)  
        if answer not in choices:
          await ctx.send('That is not a valid! please put heads or tails')
        else:
          if aianswer == answer:
            await update_bank(ctx.author, 2 * amount)
            em = discord.Embed(
              title = "Coinflip",
              description = f"You won and guessed {answer}",
              colour = discord.Colour.green(),
            )
            await ctx.send(embed = em)
          elif aianswer != answer:
            await update_bank(ctx.author, -1 * amount)
            em = discord.Embed(
              title = "Coinflip",
              description = f"You lost the correct answer was {aianswer}",
              colour = discord.Colour.red(),
            )
            await ctx.send(embed = em)

    @commands.command()
    async def dice(self, ctx, amount=None):
      if amount == None:
        return await ctx.send('Please enter an amount you would like to bet')
      await open_account(ctx.author)
      bal = await update_bank(ctx.author)

      amount = int(amount)
      if amount < 100:
        return await ctx.send('dont be shy put some more')
      else:
        if amount > bal[0]:
          return await ctx.send('You dont have enough money you broke boy')
        if amount < 0:
          return await ctx.send('Amount must be positive!')
        choices = ["1", "2", "3", "4", "5", "6"] 
        aianswer = random.choice(choices)
        answer = random.choice(choices)
        if amount < -100:
          await ctx.send('hi')
        else:
          if aianswer > answer:
            await update_bank(ctx.author, -1 * amount)
            em = discord.Embed(
              title = "You lost",
              description = f"you lost ${1 *amount}",
              colour = discord.Colour.red(),
            )
            em.add_field(name=f"{ctx.author}", value=f"Rolled `{answer}`", inline=False)
            em.add_field(name=f"{self.bot.user.name}", value=f"Rolled `{aianswer}`", inline=False)
            await ctx.send(embed = em)
          elif aianswer < answer:
            await update_bank(ctx.author, 3 * amount)
            em = discord.Embed(
              title = "You won",
              description = f"you won ${3 *amount}",
              colour = discord.Colour.green(),
            )
            em.add_field(name=f"{ctx.author}", value=f"Rolled `{answer}`", inline=False)
            em.add_field(name=f"{self.bot.user.name}", value=f"Rolled `{aianswer}`", inline=False)
            await ctx.send(embed = em)
          elif aianswer == answer:
            em = discord.Embed(
              title = "You tied",
              description = f"you won $0",
              colour = discord.Colour.orange(),
            )
            em.add_field(name=f"{ctx.author}", value=f"Rolled `{answer}`", inline=False)
            em.add_field(name=f"{self.bot.user.name}", value=f"Rolled `{aianswer}`", inline=False)
            await ctx.send(embed = em)

    @commands.command()
    async def number(self, ctx, amount=None):
      if amount == None:
        return await ctx.send('Please enter an amount you would like to bet')
      await open_account(ctx.author)
      bal = await update_bank(ctx.author)

      amount = int(amount)
      if amount < 100:
        return await ctx.send('dont be shy put some more')
      else:
        if amount > bal[0]:
          return await ctx.send('You dont have enough money you broke boy')
        if amount < 0:
          return await ctx.send('Amount must be positive!')
        choices = ["1", "2", "3", "4", "5", "6"] 
        aianswer = random.choice(choices)
        answer = random.choice(choices)
        if amount < -100:
          await ctx.send('hi')
        else:
          if aianswer > answer:
            await update_bank(ctx.author, -1 * amount)
            em = discord.Embed(
              title = "You lost",
              description = f"you lost ${1 *amount}",
              colour = discord.Colour.red(),
            )
            em.add_field(name=f"{ctx.author}", value=f"Rolled `{answer}`", inline=False)
            em.add_field(name=f"{self.bot.user.name}", value=f"Rolled `{aianswer}`", inline=False)
            await ctx.send(embed = em)
          elif aianswer < answer:
            await update_bank(ctx.author, 3 * amount)
            em = discord.Embed(
              title = "You won",
              description = f"you won ${3 *amount}",
              colour = discord.Colour.green(),
            )
            em.add_field(name=f"{ctx.author}", value=f"Rolled `{answer}`", inline=False)
            em.add_field(name=f"{self.bot.user.name}", value=f"Rolled `{aianswer}`", inline=False)
            await ctx.send(embed = em)
          elif aianswer == answer:
            em = discord.Embed(
              title = "You tied",
              description = f"you won $0",
              colour = discord.Colour.orange(),
            )
            em.add_field(name=f"{ctx.author}", value=f"Rolled `{answer}`", inline=False)
            em.add_field(name=f"{self.bot.user.name}", value=f"Rolled `{aianswer}`", inline=False)
            await ctx.send(embed = em)


      
          


    @commands.command(aliases=['rockpaperscissors'], brief="Play rock paper scissors")
    async def rps(self,ctx, message, amount=None):
        if amount == None:
            return await ctx.send('Please enter an amount you would like to bet!')
        await open_account(ctx.author)
        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount < 100:
            return await ctx.send('You must bet at least 100 coins')
        else:
            if amount > bal[0]:
                return await ctx.send('You do not havve this much money!')
            if amount < 0:
                return await ctx.send('Amount must be positive!')
            answer = message.lower()
            choices = ["rock", "paper", "scissors"]
            computer_answer = random.choice(choices)
            if answer not in choices:
                await ctx.send("That is not a valid option! Please use one of these options : rock,paper,scissors")
            else:
                if computer_answer == answer:
                    await update_bank(ctx.author, 0 * amount)
                    await ctx.send(f"Tie! We both picked {answer}! and You earned {0 * amount}")
                elif computer_answer == "rock":
                    if answer == "paper":
                        await update_bank(ctx.author, 3 * amount)
                        await ctx.send(
                            f"You win! I picked {computer_answer} ,You earned {2 * amount} and you picked {answer}!")
                    elif answer == "scissors":
                        await update_bank(ctx.author, -1 * amount)
                        await ctx.send(
                            f"You lost! I picked {computer_answer} ,You lost {-1 * amount} and you picked {answer}!")
                elif computer_answer == "paper":
                    if answer == "scissors":
                        await update_bank(ctx.author, 3 * amount)
                        await ctx.send(
                            f"You win! I picked {computer_answer} ,You earned {3 * amount} and you picked {answer}!")
                    elif answer == "rock":
                        await update_bank(ctx.author, -1 * amount)
                        await ctx.send(
                            f"You lost! I picked {computer_answer} ,You lost {-1 * amount} and you picked {answer}!")
                elif computer_answer == "scissors":
                    if answer == "rock":
                        await update_bank(ctx.author, 3 * amount)
                        await ctx.send(
                            f"You win! I picked {computer_answer} ,You earned {3 * amount} and you picked {answer}!")
                    elif answer == "paper":
                        await update_bank(ctx.author, -1 * amount)
                        await ctx.send(
                            f"You lost! I picked {computer_answer} ,You lost {-1 * amount} and you picked {answer}!")

    

    @beg.error
    async def error(self,ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="**BEG ERROR**", description =f"Sorry There is a cooldown on this command please wait {round(error.retry_after)} seconds", colour = discord.Colour.red())
        await ctx.send(embed=embed)

    @golddig.error
    async def golddig_error(self,ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="**Gold-Dig Error**", description =f"Sorry There is a cooldown on this command please wait {round(error.retry_after)} seconds ", colour = discord.Colour.red())
        await ctx.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="**DAILY ERROR**", description= f"Sorry There is a cooldown on this command please wait {round(error.retry_after)} seconds", colour = discord.Colour.red())
        await ctx.send(embed=embed)
  

  

  
def setup(bot):
    bot.add_cog(Economy(bot))
