import disnake
from disnake.ext import commands
from main import has_specific_role

class айди(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="айди",
        description="получение ID пользователей, который имеют {роль} ( Пример указания роли: DS manager | )",
    )
    @has_specific_role()
    async def get_role_members_id(ctx, имя_роли: str):    
        role = disnake.utils.get(ctx.guild.roles, name=имя_роли)
        if role:
            members_with_role = role.members
            member_ids = [str(member.id) for member in members_with_role]

            # Сохранение идентификаторов в файл
            with open("member_ids.txt", "w") as file:
                file.write("\n".join(member_ids))

            await ctx.send("Идентификаторы пользователей были сохранены в файле member_ids.txt.", ephemeral=True)
        else:
            await ctx.send(f"Роль {имя_роли} не найдена.", ephemeral=True)

@staticmethod
def setup(bot: commands.Bot):
    bot.add_cog(айди(bot))