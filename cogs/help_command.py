import disnake
from disnake.ext import commands


class помощь(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.slash_command(
      name="помощь",  # или "help", как вам удобнее
      description="показать список доступных команд и их примеры использования",
  )
  async def help_command(ctx):
    help_embed = disnake.Embed(
        title="Помощь",
        description="Вот список доступных команд и примеры их использования:",
        color=disnake.Color.green())

    help_embed.add_field(name="/пинг",
                         value="Узнать пинг бота.\nПример: `/пинг`",
                         inline=False)

    help_embed.add_field(
        name="/айди",
        value=
        "Получение ID пользователей, имеющих указанную роль.\nПример: `/айди имя_роли:DS manager`",
        inline=False)

    help_embed.add_field(
        name="/лс_1/2/3",
        value=
        "Отправка сообщения в ЛС пользователям с указанными ID из файла.\nПример: `/лс_1/2/3 имя_файла:ID.txt текст:капт`",
        inline=False)

    help_embed.add_field(
        name="/реакции",
        value=
        "Получение ID пользователей, которые оставили определенную реакциию на сообщение.\nПример: `/реакции сообщение:ID_сообщения реакция:🍪`",
        inline=False)

    help_embed.add_field(
        name="/список_войс",
        value=
        "Получение ID пользователей, которые находятся в голосовом канале.\nПример: `/список_войс канал: #🐺〡Волчья нора #1`",
        inline=False)

    help_embed.add_field(
        name="/список",
        value=
        "Создание списка для МП.\nПример: `/список list_id:1 type:FW main:20 reserve:5 start_time:20 color:Green`",
        inline=False)

    help_embed.add_field(
        name="/списки",
        value="Отобразить id всех списка для МП.\nПример: `/списки`",
        inline=False)

    help_embed.add_field(
        name="/доб",
        value=
        "Добавление человека в список для МП.\nПример: `/доб list_id:1 list_name:main/main def/reserve user:@mishanya`",
        inline=False)

    help_embed.add_field(
        name="/дел",
        value=
        "Удаление человека из списка для МП.\nПример: `/дел list_id:1 user:@mishanya`",
        inline=False)
    await ctx.send(
        embed=help_embed, ephemeral=True
    )  # ephemeral=True делает сообщение видимым только для пользователя


@staticmethod
def setup(bot: commands.Bot):
  bot.add_cog(помощь(bot))
