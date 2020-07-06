import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix = "--")
bot.remove_command("help")
extensions = ["mafiabot", "mafiacommands"]

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Mafia"))
    print("Bot is ready")

@bot.command()
async def load(ctx):
    extension = ctx.message.content.split(" ")[1]
    try:
        bot.load_extension(extension)
        print("Loaded {}".format(extension))
    except Exception as error:
        print("{} cannot be loaded. [{}]".format(extension, error))

@bot.command()
async def unload(ctx):
    extenstion = ctx.message.content.split(" ")[1]
    try:
        bot.unload_extension(extension)
        print("Unloaded {}".format(extension))
    except Exception as error:
        print("{} cannot be unloaded. [{}]".format(extension, error))

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print("Loaded {}".format(extension))
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))
    bot.run(TOKEN)
