import disnake
from disnake.ext import commands
from main import has_specific_role

class онлайн(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="онлайн",
        description="упомянуть всех пользователей с ролью @Yamato Majestic, находящихся в сети",
    )
    @has_specific_role()
    async def онлайн(ctx):
        # Получаем объекты роли @Yamato Majestic
        role_names = ["Yamato Majestic"]
        roles = [disnake.utils.get(ctx.guild.roles, name=role_name) for role_name in role_names]

        # Создаем список пользователей с этими ролями и статусом "онлайн"
        online_users = [member for member in ctx.guild.members if member.status == disnake.Status.online and any(role in member.roles for role in roles)]

        # Тегаем пользователей
        tagged_users = [member.mention for member in online_users]

        if tagged_users:
            await ctx.send(f"Пользователи с ролью {role_names}, находящиеся в сети: {' '.join(tagged_users)}")
        else:
            await ctx.send("Нет пользователей с ролью {role_names}, находящихся в сети.")

@staticmethod
def setup(bot: commands.Bot):
    bot.add_cog(онлайн(bot))