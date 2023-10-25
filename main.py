import disnake
import logging
import os
import sys
import keep_alive
from disnake.ext import commands
from datetime import timedelta

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all())

# Create admin role


def has_specific_role():

  async def predicate(ctx):
    required_role = disnake.utils.get(ctx.guild.roles,
                                      name="bot_mngr")  # Name of role
    if required_role in ctx.author.roles:
      return True
    else:
      await ctx.send("You don't have permission to run this command.",
                     ephemeral=True)
      return False

  return commands.check(predicate)


# Configure the logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load cogs
bot.load_extension("cogs.cmd_ping")
bot.load_extension("cogs.help_command")
bot.load_extension("cogs.cmd_yamato")
bot.load_extension("cogs.cmd_ls-teg")
bot.load_extension("cogs.cmd_role_ID")
bot.load_extension("cogs.cmd_voice_list")
bot.load_extension("cogs.cmd_online")
bot.load_extension("cogs.cmd_reactions")
bot.load_extension("cogs.cmd_list")

# Start


@bot.event
async def on_ready():
  print(f"{bot.user} online and working!")

  game = disnake.Game("/помощь and Eating cookies 🍪")
  await bot.change_presence(status=disnake.Status.online, activity=game)


keep_alive.keep_alive()

token = os.environ['token_p']

bot.run(token)
