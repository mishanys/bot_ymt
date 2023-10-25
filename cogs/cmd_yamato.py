import disnake
from disnake.ext import commands

class ямато(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="ямато",
        description="Кто такие Yamato?",
        )
    async def ямато( ctx ):
        author_mention = ctx.author.mention
        await ctx.send(f"{author_mention} Загляни в лс!", ephemeral=True)
        await ctx.author.send("Привет! Ты что, не знаешь кто такие Yamato? Yamato - 100")

@staticmethod
def setup(bot: commands.Bot):
    bot.add_cog(ямато(bot))