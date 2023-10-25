import disnake
from disnake.ext import commands
from main import has_specific_role

class список_войс(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="список_войс",
        description="получение ID пользователей, которые находятся в голосовом канале.",
    )
    @has_specific_role()
    async def список_войс(ctx, канал: disnake.VoiceChannel):
        # Создаем список для хранения ID пользователей
        user_ids = []

        # Перебираем участников в указанном голосовом канале
        for member in канал.members:
            user_ids.append(str(member.id))  # Преобразуем ID в строку и добавляем в список

        # Создаем или перезаписываем файл для хранения ID
        with open("ID_войс.txt", "w") as file:
            file.write("\n".join(user_ids))

        await ctx.send(f"ID пользователей из голосового канала {канал.name} были записаны в файл 'ID_войс.txt'.")

@staticmethod
def setup(bot: commands.Bot):
    bot.add_cog(список_войс(bot))