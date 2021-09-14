import discord
from discord.ext.commands import Cog
from discord.ext import commands
class Info(Cog):
    def __init__(self,bot):
        self.bot = bot
        self.cancelled = True

    @commands.command(brief="Search avatar member")
    async def avatar(self,ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(title="This command is used like this: ```+avatar [member]```", colour=0xff0000,
                                  timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)
            return

        else:
            embed2 = discord.Embed(title=f"{member}'s Avatar!", colour=0x0000ff, timestamp=ctx.message.created_at)
            embed2.add_field(name="Animated?", value=member.is_avatar_animated())
            embed2.set_image(url=member.avatar_url)
            await ctx.send(embed=embed2)

    @commands.command(brief="Check your pings delay")
    async def ping(self,ctx):
      ping = round(self.bot.latency * 1000)
      embed = discord.Embed (
        title = "**PING**",
        description = f"The Ping is {ping}ms",
        colour = discord.Colour.green()
      )
      await ctx.send(embed=embed)

    @commands.command(aliases=["m"])
    async def members(self,ctx):
        a = ctx.guild.member_count
        b = discord.Embed(title=f"Member", description=f'There is {a} members in {ctx.guild.name}', color=(0xffff00))
        await ctx.send(embed=b)

    @commands.command(aliases=['serverinfo', 'sinfo', 'si'], pass_context=True)
    async def server(self,ctx):
        server = ctx.guild
        owner = str(ctx.guild.owner)
        role_count = len(ctx.guild.roles)
        em = discord.Embed(color=0xea7938)
        em.add_field(name='Name', value=f'{ctx.guild.name}')
        em.add_field(name='Owner', value=owner)
        em.add_field(name='Members', value=server.member_count)
        em.add_field(name='Region', value=server.region)
        em.add_field(name='Verification Level', value=str(server.verification_level))
        em.add_field(name='Highest role', value=ctx.guild.roles[-2])
        em.add_field(name='Number of roles', value=str(role_count))
        em.add_field(name='Created At', value=server.created_at.__format__('%A, %d. %B %Y  %H:%M:%S'))
        em.set_thumbnail(url=server.icon_url)
        em.set_author(name='**Server Info**')
        em.set_footer(text='Server ID: %s' % server.id)
        await ctx.send(embed=em)

    @Cog.listener()
    async def on_ready(self):
        print('Bot Info is ready')

def setup(bot):
    bot.add_cog(Info(bot))
