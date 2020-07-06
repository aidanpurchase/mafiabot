import discord
import random
from discord.ext import commands
from gamelist import GameList

class MafiaCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.Listener()
    async def on_ready(self):
        print("Mafia Commands ready")

    @commands.command(pass_context=True)
    async def kill(self, ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if ctx.author.id is in GameList.instance.get_playing_IDs():
                game_name = GameList.instance.get_game(ctx.author)
                if GameList.instance.get_role(game_name, ctx.author) == "Boss":
                    try:
                        target = ctx.message.mentions.users.first()
                    except:
                        await ctx.send("Target does not exist! Type --kill @[user_name] (not nickname)")
                    
                    if target.id is in GameList.instance.get_alive_IDs(game_name):
                        GameList.instance.kill_player(game_name, target)
                        await ctx.send("You successfully targetted {}.".format(target.name))
                    else:
                        await ctx.send("Target is either already dead or not playing! Type --kill @[username] (not nickname).")
                else:
                    await ctx.send("You must be a Boss to use this command! Type --roles to find your role!")
            else:
                await ctx.send("you must be in an active game to use this command.")
        else:
            await ctx.send("You must be in a DM with me to use this command!")

def setup(client):
    client.add_cog(MafiaBot(client))
