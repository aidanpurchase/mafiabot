import discord
import random
from discord.ext import commands
from gamelist import GameList

role_order = ["Boss", "Inspector", "Doctor", "Drunk", "Disabler", "Bodyguard", "Stalker"]
town_roles = ["Inspector", "Doctor", "Drunk", "Bodyguard", "Villager"]
mafia_roles = ["Boss", "Disabler", "Stalker"]

class MafiaBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        GameList.instance = GameList()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mafia Bot ready")

    @commands.command(pass_context=True)
    async def create(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            games = GameList.instance.get_games()
            if game in games:
                await ctx.send("{} has already been created! Type '--join {}' to join the game.".format(game, game))
            else:
            `   GameList.instance.create_game(game, ctx.author)
                await ctx.send("{} has been created by {}! Type '--join {}' to join the game.".format(game, ctx.message.author, game))
        else:
            await ctx.send("Please join a server to use this command.")

    @commands.command(pass_context=True)
    async def join(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            open_games = GameList.instance.get_open_games()
            if game in open_games:
                GameList.instance.add_attendee(game, ctx.author)
            else:
                await ctx.send("{} is unable to join the game. Try again later.".format(ctx.message.author))
        else:
            await ctx.send("Please join a server to use this command.")

    @commands.command(pass_context=True)
    async def start(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            games = GameList.instance.get_games()
            open_games = GameList.instance.get_open_games()
            if game in open_games:
                await ctx.send("{} has already been started!".format(game))
            elif game in games:
                creatorID = GameList.instance.get_creator(game)
                creator = ctx.message.guild.get_member(creatorID)
                if ctx.message.author == creator:
                    GameList.instance.start_game(game)
                    await ctx.send("{} has been started!!".format(game))
                    await self.run(game, ctx)
                else:
                    await ctx.send("{} doesn't have permission to start {}!".format(ctx.message.author, game))
            else:
                await ctx.send("{} doesn't exist!".format(game))
        else:
            await ctx.send("Please join a server to use this command.")

    @commands.command(pass_context=True)
    async def delete(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            game = ctx.message.content.split(" ")[1]
            games = GameList.instance.get_games()
            if game in games:
                creatorID = GameList.instance.get_creator(game)
                creator = ctx.message.guild.get_member(creatorID)
                if ctx.message.author == creator:
                    GameList.instance.delete_game(game)
                    await ctx.send("{} was been deleted!".format(game))
                else:
                    await ctx.send("{} doesn't have permission to delete {}".format(ctx.message.author, game))
            else:
                await ctx.send("{} doesn't exist!".format(game))
        else:
            await ctx.send("Please join a server to use this command.")

    async def run(self, game_name, ctx):
        playerIDs = GameList.instance.get_all_IDs(game_name)
        shuffled_IDs = random.shuffle(playerIDs)

        for role_pair in set(zip(shuffled_IDs, role_order)):
            ID, role = role_pair
            member = ctx.message.guild.get_member(ID)
            await member.send("You are a {}! To find out more type --roles.".format(role))
            GameList.instance.assign_role(game_name, member, role)
        try:
            for ID in shuffled_IDs[len(role_order):]:
                member = ctx.message.guild.get_member(ID)
                await member.send("You are a Townie! To find out more type --roles.")
                GameList.instance.assign_role(game_name, member, "Townie")
        except:
            print("No more players")
        print("All players assigned a role")

        await ctx.send("The roles are assigned! Check your DMs for your secrete mission.")

        while True:
            # The gameloop goes here
            pass
    
    def who_won(self, game_name, ctx):
        alive_mafia = 0
        alive_villagers = 0
        roles = GameList.instance.get_alive_roles(game_name)
        
        for role in roles:
            if role in town_roles:
                alive_town += 1
            elif role in mafia_roles:
                alive_mafia += 1
            else:
                print("Error! Role doesn't exist.")

        if alive_mafia < 1:
            return "Town"
        elif alive_town < 1:
            return "Mafia"
        else:
            return None

    @commands.command(pass_context=True)
    async def kill(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            print("{} killed nothing".format(ctx.message.author))
        else:
            print("{} made a big whoopsie!".format(ctx.message.author))

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author

        embed = discord.Embed(
            colour = discord.Colour.red()
        )

        embed.set_author(name="Help")
        embed.add_field(name="Premise", value="""A town is terrorised by a new mafia! The mafia wish to exterminate them and clearly the town wishes the mafia were gone.
                                                \nEach night every player goes through their special ability to achieve their 'team' goal. During the day you all discuss who to kill.
                                                \nThe mafia are in kahoots so town folk beware you don't kill your own during the day as well! A game of pleas and lies, will you survive the night?""",
                                    ,inline=False)
        embed.add_field(name="--create [game_name]", value="Create the specified game", inline=False)
        embed.add_field(name="--join [game_name]", value="Join the specified game", inline=False)
        embed.add_field(name="--start [game_name]", value="Starts the specified game (only if you created it)", inline=False)
        embed.add_field(name="--delete [game_name]", value="Deletes the specified game (only if you created it)", inline=False)
        embed.add_filed(name="--roles", value="A help card explaining every role and their ability", inline=False)
        await author.send(embed=embed)

    @commands.command(pass_context=True)
    async def roles(self, ctx):
        author = ctx.message.author

        embed = discord.Embed(
                colour = discord.Colour.blue()
        )

        embed.set_author(name="Roles")
        embed.set_field(name="Town Folk", inline=False)
        embed.set_field(name="Townie", value"A innocent resident of the town you simply wish to survive the night (and the day). Don't look suspicious!", inline=False)
        embed.set_field(name="Inspector", value="You are the town inspector tasked with identifying and removing the Mafia.\nCommand: --inspect [player]", inline=False)
        embed.set_field(name="Doctor", value="You are the town doctor tasked with saving the town from the death.\nCommand: --save [player]", inline=False)
        embed.set_field(name="Drunk", value="You are a simple drunk person who always foils the Mafia's plan.\nCommand: --prevent [player]", inline=False)
        embed.set_field(name="Bodyguard", value="You were hired by the town to protect them by taking a bullet for them.\nCommand: --protect [player]", inline=False)
        embed.set_field(name="The Mafia", inline=False)
        embed.set_field(name="Boss", value="You are the mafia boss and thus you decide who takes the bullet every night\nCommand: --kill [player]", inline=False)
        embed.set_field(name="Disabler", value="You are mafia hitman sent out to disable the town folk for the night\nCommand: --disable [player]", inline=False)
        embed.set_field(name="Stalker", value="You are the town stalker sending information back to the boss about town folk\nCommand: --stalk [player]", inline=False)
        await author.send(embed=embed)

def setup(client):
    client.add_cog(MafiaBot(client))
