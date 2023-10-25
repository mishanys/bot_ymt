import disnake
import asyncio
from disnake.ext import commands
from main import has_specific_role


class лс(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="лс",
        description="написать в ЛС всем пользователям, ID которых сохранены в ID.txt",
    )
    @has_specific_role()
    async def лс(self, ctx, имя_файла: str, *, текст: str):  # Добавьте self как первый параметр метода
        await ctx.send("Обработка запроса начата. Это может занять некоторое время.", ephemeral=True)

        try:
            with open(имя_файла, 'r') as file:
                user_ids = file.read().splitlines()

            successful_sends = 0  # Счетчик успешно отправленных сообщений

            for user_id in user_ids:
                try:
                    user = await self.bot.fetch_user(int(user_id))  # Используйте self.bot
                    if user:
                        try:
                            await user.send(content=текст) # Используйте content= для отправки текста
                            successful_sends += 1
                            print(f"Сообщение успешно отправлено человеку с ID: {user_id}")
                        except disnake.errors.Forbidden as e:
                            print(f"Сообщение не отправлено человеку с ID {user_id} (Ошибка: {e})")
                        except disnake.errors.HTTPException as e:
                            print(f"Ошибка в отправке человеку с ID {user_id}: {e}")
                    else:
                        print(f"Человек с {user_id} не найден.")
                except disnake.errors.NotFound:
                    print(f"Человек с {user_id} не найден.")

                await asyncio.sleep(7)

            await ctx.send(f"Сообщения отправлены успешно. Успешно отправлено: {successful_sends}/{len(user_ids)}", ephemeral=True)

        except FileNotFoundError:
            await ctx.send("Файл не найден.", ephemeral=True)

@staticmethod
def setup(bot: commands.Bot):
    bot.add_cog(лс(bot))
