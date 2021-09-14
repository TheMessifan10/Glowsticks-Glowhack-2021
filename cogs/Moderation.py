import discord
from discord.ext import commands
from discord.ext.commands import Cog
import datetime
import asyncio
class Moderation(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cancelled = False

    class DurationConverter(commands.Converter):
        async def convert(self, ctx, argument):
            amount = argument[:-1]
            unit = argument[-1]

            if amount.isdigit() and unit in ['s', 'm', 'h','d']:
                return (int(amount), unit)

            raise commands.BadArgument(message='Not a valid duration')

    @commands.command()
    async def ban(self, ctx, member : discord.Member=None, *, reason=None):
      if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You Need The Permission `ban members` to do this command')
        return
      await member.ban(reason=reason)
      embed2 = discord.Embed(title="**BANNED**", colour=0xff6600)
      embed2.add_field(name="**User**", value=f"{member.mention} has been banned", inline=False)
      embed2.add_field(name="**Reason**", value=f"Reason: {reason}", inline=False)
      embed2.add_field(name="**Banned By**", value=f"{ctx.author}", inline=False)
      await ctx.send(embed=embed2)
      return
      
    
    @commands.command()
    async def unban(self, ctx, *, member):
      if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You Need The Permission `ban members` to do this command')
        return
      banned_user = await ctx.guild.bans()
      member_name, member_discriminator = member.split("#")
      for ban_entry in banned_user:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
          await ctx.guild.unban(user)
          embed = discord.Embed(title="**UNBANNED**!", description=f" {user.mention} has been unbanned by {ctx.author}!", color=0xff6600)
          await ctx.send(embed=embed)
          return

    @commands.command(brief="Tempban member")
    async def tempban(self,ctx, member: commands.MemberConverter, duration:DurationConverter, reason=None):
      if (not ctx.author.guild_permissions.ban_members):
        await ctx.send('You Need The Permission `ban members` to do this command')
        return
      multiplier = {'s': 1, 'm': 60, 'h' : 3600, 'd': 86400}
      amount, unit = duration

      await ctx.guild.ban(member, reason=reason)
      embed2 = discord.Embed(title="**TEMPBANNED**", colour=0xff6600)
      embed2.add_field(name="USER", value=f"{member.mention} has been banned", inline=False)
      embed2.add_field(name="Reason", value=f"Reason: {reason}", inline=False)
      embed2.add_field(name="TEMPBANNED By", value=f"{ctx.author}", inline=False)
      embed2.add_field(name="TEMPBANNED Time", value=f"{amount}{unit}", inline=False)
      await ctx.send(embed=embed2)
      await asyncio.sleep(amount * multiplier[unit])
      await ctx.guild.unban(member)
      embed3 = discord.Embed(title=f"Tempban Has Finished", colour=0xff6600)
      embed3.add_field(name="**USER**", value=f"{member.mention} has been banned", inline=False)
      embed3.add_field(name="**REASON**", value=f"Reason: {reason}", inline=False)
      embed3.add_field(name="**TEMPBANNED By**", value=f"{ctx.author}", inline=False)
      embed3.add_field(name="**TEMPBANNED TIME**", value=f"{amount}{unit}", inline=False)
      await ctx.send(embed=embed3)

    @commands.command(brief="Kick member")
    async def kick(self,ctx, member: discord.Member, *, reason=None):
      if (not ctx.author.guild_permissions.kick_members):
        await ctx.send('You Need The Permission `kick members` to do this command')
        return
      await member.kick(reason=reason)
      embed2 = discord.Embed(title="**KICKED**", colour=0xff6600)
      embed2.add_field(name="**User**", value=f"{member.mention} has been kicked", inline=False)
      embed2.add_field(name="**Reason**", value=f"Reason: {reason}", inline=False)
      embed2.add_field(name="**Kicked By**", value=f"{ctx.author}", inline=False)
      await ctx.send(embed=embed2)
      return

    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, reason=None):
      if(not ctx.author.guild_permissions.manage_roles):
        await ctx.send('You need the permission `manage roles` to do this command sorry')
        return
      guild = ctx.guild
      mutedRole = discord.utils.get(guild.roles, name="Muted")

      if not mutedRole:
        mutedRole = await guild.create_role(name = "Muted")

        for channel in guild.channels:
          await ctx.send('No muted role was found let me create one really quickly... ')
          await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
      
      await member.add_roles(mutedRole, reason=reason)
      embed2 = discord.Embed(title="**MUTED**", colour=0xff6600)
      embed2.add_field(name="**User**", value=f"{member.mention} has been muted", inline=False)
      embed2.add_field(name="**Reason**", value=f"Reason: {reason}", inline=False)
      embed2.add_field(name="**MUTED BY**", value=f"{ctx.author}", inline=False)
      await ctx.send(embed=embed2)
      return
      await member.send(f'You have been muted from **{guild.name}** | Reason: **{reason}**')

    @commands.command()
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
      if(not ctx.author.guild_permissions.manage_roles):
        await ctx.send('You need the permission `manage roles` to do this command sorry')
        return
      guild = ctx.guild
      mutedRole = discord.utils.get(guild.roles, name="Muted")

      if not mutedRole:
        await ctx.send('no muted role was found lol, just do !mute and it will automatically create one for you')
        return

      await member.remove_roles(mutedRole, reason=reason)
      embed2 = discord.Embed(title="**UNMUTED**", colour=0xff6600)
      embed2.add_field(name="**User**", value=f"{member.mention} has been unmuted", inline=False)
      embed2.add_field(name="**Reason**", value=f"Reason: {reason}", inline=False)
      embed2.add_field(name="**UNMUTED BY**", value=f"{ctx.author}", inline=False)
      await ctx.send(embed=embed2)
      return
      await member.send(f'You have been unmuted from **{guild.name}** | Reason: **{reason}**')

    @commands.command(aliases = ['clear', 'p', 'c'])
    async def purge(self, ctx, amount=6):
      if (not ctx.author.guild_permissions.administrator):
        await ctx.send('You Need `Admin` to do this command')
        return
      await ctx.channel.purge(limit=amount + 1)
      embed = discord.Embed(title="Purge Successful", description = f"{amount -1} messages was cleared/purged")
      return await ctx.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot Moderation is ready")

  
def setup(bot):
    bot.add_cog(Moderation(bot))
