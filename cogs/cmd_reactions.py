import disnake
from disnake.ext import commands
from main import has_specific_role

class реакции(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="реакции",
        description='получение ID пользователей, которые оставили определенную реакцию на сообщение.',
    )
    @has_specific_role()
    async def реакции(self, ctx, сообщение: disnake.Message, реакция: str):
        reacted_users = set()
        for reaction in сообщение.reactions:
            if str(reaction.emoji) == реакция:
                async for user in reaction.users():
                    if user.id != self.bot.user.id:
                        reacted_users.add(str(user.id))

        with open('ID_реакции.txt', 'w') as file:
            file.write('\n'.join(reacted_users))

        await ctx.send(f"ID пользователей, оставивших реакцию {реакция} на сообщение {сообщение.jump_url}, были записаны в файл 'ID_реакции.txt'.", ephemeral=True)

@staticmethod
def setup(bot: commands.Bot):
    bot.add_cog(реакции(bot))