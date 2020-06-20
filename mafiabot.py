import discord
from discord.ext import commands

class MafiaBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.games = {}
        self.open_games = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mafia Bot ready")

    @commands.command(pass_context=True)
    async def play(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            #TODO make a create command so I can avoid this error
            if game in self.games and self.open_games[ctx.guild]:
                self.games[game].append(self.message.author)
            elif self.open_games[ctx.guild]:
                self.games[game] = [ctx.message.author]
            else:
                await ctx.send("{} is unable to join the game".format(ctx.message.author))
        else:
            await ctx.send("Please join a server to use this command")

    @commands.command(pass_context=True)
    async def start(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            if game in self.games:
                if ctx.message.author == self.games[game][ctx.message.author]:
                    self.open_games[game] = False
                    #TODO get the game actually started
                else:
                    await ctx.send("{} doesn't have permission to start {}".format(ctx.message.author, game))
            else:
                await ctx.send("{} doesn't exist".format(game))
        else:
            await ctx.send("Please join a server to use this command")

    @commands.command(pass_context=True)
    async def kill(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            print("{} killed nothing".format(ctx.message.author))
        else:
            print("{} made a big whoopsie".format(ctx.message.author))

    @commands.command(pass_context=True)
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        except Exception as error:
            print("mafiabot couldn't join vc. [{}]".format(error))

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
        embed.add_field(name="--play [game_name]", value="Instantiate or join the specified game", inline=False)
        embed.add_field(name="--start [game_name]", value="Starts the specified game (only if you instantiated it", inline=False)
        await author.send(embed=embed)

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=100):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            async for message in ctx.history(limit=int(amount)):
                await message.delete()

def setup(client):
    client.add_cog(MafiaBot(client))
