import disnake
from disnake.ext import commands

class пинг(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name='пинг',
        description='узнать задержку бота.',
    )
    async def пинг(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f"Понг! {round(self.bot.latency * 1000)}мс", ephemeral=True)

@staticmethod
def setup(bot: commands.Bot):
    bot.add_cog(пинг(bot))