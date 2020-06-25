import discord
from discord.ext import commands
from game import Game
from gamelist import GameList

class MafiaBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        GameList.instance = GameList()
        self.games = {}
        self.open_games = set([])

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mafia Bot ready")

    @commands.command(pass_context=True)
    async def create(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            if game in self.games:
                await ctx.send("{} has already been created! Type '--join {}' to join the game.".format(game, game))
            else:
                self.games[game] = [ctx.message.author]
                self.open_games.add(game)
                await ctx.send("{} has been created by {}! Type '--join {}' to join the game.".format(game, ctx.message.author, game))
        else:
            await ctx.send("Please join a server to use this command.")

    @commands.command(pass_context=True)
    async def join(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            if game in self.games and self.open_games:
                self.games[game].append(self.message.author)
            else:
                await ctx.send("{} is unable to join the game. Try again later.".format(ctx.message.author))
        else:
            await ctx.send("Please join a server to use this command.")

    @commands.command(pass_context=True)
    async def start(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel) and ctx.message.author.voice:
            game = ctx.message.content.split(" ")[1]
            if game not in self.open_games:
                await ctx.send("{} has already been started!".format(game))
            elif game in self.games:
                #TODO Make sure dead games (ie, creator hasn't ended it) are removed
                if ctx.message.author == self.games[game][0]:
                    self.open_games.remove(game)
                    channel = ctx.message.author.voice.channel
                    await channel.connect()
                    await ctx.send("{} has been started!!".format(game))
                    #TODO get the game actually started
                else:
                    await ctx.send("{} doesn't have permission to start {}!".format(ctx.message.author, game))
            else:
                await ctx.send("{} doesn't exist!".format(game))
        else:
            await ctx.send("Please join a server voice chat to use this command.")

    @commands.command(pass_context=True)
    async def delete(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            if game in self.games:
                if ctx.message.author == self.games[game][0]:
                    self.games.pop(game, None)
                    try:
                        self.open_games.remove(game) # A game can be ended whether it is open or not
                    except:
                        pass 
                    await ctx.send("{} was been deleted!".format(game))
                else:
                    await ctx.send("{} doesn't have permission to delete {}".format(ctx.message.author, game))
            else:
                await ctx.send("{} doesn't exist!".format(game))
        else:
            await ctx.send("Please join a server to use this command.")


    async def run(self, game):
        players = len(self.games[game])

    @commands.command(pass_context=True)
    async def kill(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            print("{} killed nothing".format(ctx.message.author))
        else:
            print("{} made a big whoopsie!".format(ctx.message.author))

#TODO remove these once you've sorted out vc aspect of bot
#    @commands.command(pass_context=True)
#    async def leave(self, ctx):
#        await ctx.voice_client.disconnect()

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author

        embed = discord.Embed(
            colour = discord.Colour.orange()
        )

        embed.set_author(name="Help")
        embed.add_field(name="--create [game_name]", value="Create the specified game", inline=False)
        embed.add_field(name="--join [game_name]", value="Join the specified game", inline=False)
        embed.add_field(name="--start [game_name]", value="Starts the specified game (only if you created it)", inline=False)
        embed.add_field(name="--delete [game_name]", value="Deletes the specified game (only if you created it)", inline=False)
        await author.send(embed=embed)

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=100):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            async for message in ctx.history(limit=int(amount)):
                await message.delete()

def setup(client):
    client.add_cog(MafiaBot(client))
