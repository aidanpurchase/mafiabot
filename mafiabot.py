import discord
from discord.ext import commands

class MafiaBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mafia Bot ready")
        
    @commands.command()
    async def marco(self, ctx):
        await ctx.message.channel.send("Pollo!")

    @commands.command(pass_context=True)
    async def kill(self, ctx):
        await ctx.message.delete()

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author

        embed = discord.Embed(
            colour = discord.Colour.orange()
        )

        embed.set_author(name="Help")
        embed.add_field(name="--command_name", value="It does a thing", inline=False)                                       
        await author.send(embed=embed)                                                                                      
    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=100):
        async for message in ctx.history(limit=int(amount)):
            await message.delete()

def setup(client):
    client.add_cog(MafiaBot(client))
