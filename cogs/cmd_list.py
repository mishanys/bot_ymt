import disnake
from disnake.ext import commands
from disnake.ui.button import Button
from datetime import datetime
import json
import os
import asyncio

ADMIN_ROLES = ["DS Moder",
               "DS Manager"]  # Роли которые смогут удалять списки и т.п


class список(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.data = self.load_data()  # Загрузка данных из файла
    self.message_sent = False
    self.message_id = None

  def load_data(self):
    # Создаем абсолютный путь к файлу list_data.json
    file_path = os.path.join(os.path.dirname(__file__), "list_data.json")
    try:
      with open(file_path, "r") as file:
        data = json.load(file)
    except FileNotFoundError:
      data = {}
      with open(file_path, "w") as file:
        json.dump(data, file)
    return data

  def save_data(self):
    # Создаем абсолютный путь к файлу list_data.json
    file_path = os.path.join(os.path.dirname(__file__), "list_data.json")
    with open(file_path, "w") as file:
      json.dump(self.data, file)

  def is_admin_or_has_role(self, member):
    return any(
        role.name in ADMIN_ROLES
        for role in member.roles) or member.guild_permissions.administrator

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author == self.bot.user and self.message_sent and self.message_id:
      self.data[self.message_id]["message_id"] = message.id
      self.data[self.message_id][
          "link"] = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
      self.save_data()
      self.message_sent = False
      self.message_id = None

  @commands.slash_command(name="удалить_список",
                          description="Удалить список пользователей.",
                          options=[
                              disnake.Option("list_id",
                                             "Идентификатор списка",
                                             type=disnake.OptionType.string,
                                             required=True)
                          ])
  async def удалить_список(self, ctx, list_id: str):
    if self.is_admin_or_has_role(ctx.author):
      if list_id in self.data:
        del self.data[list_id]  # Удаляем список из данных
        self.save_data()  # Сохраняем обновленные данные
        await ctx.send(f"Список с идентификатором '{list_id}' удален.",
                       ephemeral=True)
      else:
        await ctx.send(f"Список с идентификатором '{list_id}' не найден.",
                       ephemeral=True)
    else:
      await ctx.send("Нет у Вас прав на это", ephemeral=True)

  @commands.slash_command(name="списки",
                          description="Показать список всех доступных списков."
                          )
  async def списки(self, ctx):
    if self.is_admin_or_has_role(ctx.author):
      if not self.data:
        await ctx.send("Списков не найдено.", ephemeral=True)
      else:
        list_info = []
        for list_id, list_data in self.data.items():
          list_link = list_data.get("link", "Ссылка не найдена")
          list_info.append(f"Название: `{list_id}` | Ссылка: {list_link}\n")
        lists_info_str = "\n".join(list_info)
        await ctx.send(f"Доступные списки:\n{lists_info_str}", ephemeral=True)
    else:
      await ctx.send("Нет у Вас прав на это", ephemeral=True)

  @commands.slash_command(name="список",
                          description="Создание списка пользователей.",
                          options=[
                              disnake.Option("list_id",
                                             "Идентификатор списка",
                                             type=disnake.OptionType.string,
                                             required=True),
                              disnake.Option("type",
                                             "Тип мероприятия",
                                             type=disnake.OptionType.string,
                                             required=True),
                              disnake.Option("main",
                                             "Кол-во людей в основном списке",
                                             type=disnake.OptionType.integer,
                                             required=True),
                              disnake.Option("reserve",
                                             "Кол-во людей в резевном списке",
                                             type=disnake.OptionType.integer,
                                             required=True),
                              disnake.Option("start_time",
                                             "Время начала",
                                             type=disnake.OptionType.integer,
                                             required=True),
                              disnake.Option("color",
                                             "Цвет",
                                             type=disnake.OptionType.string,
                                             required=True)
                          ])
  async def список(self, ctx, list_id: str, type: str, main: str, reserve: str,
                   start_time: str, color: str):
    if self.is_admin_or_has_role(ctx.author):
      # Проверяем, существует ли list_id уже в данных
      if list_id in self.data:
        await ctx.send(f"Список с идентификатором '{list_id}' уже существует.",
                       ephemeral=True)
        return

      voice_time = start_time - 1

      # Создаем встроенное сообщение
      embed = disnake.Embed(
          title=
          f"**[{type}] Время начала {start_time}:00 / Voice {voice_time}:00**",
          description=f"Цвет - **{color}**",
          color=0x8B0000  # Цвет сообщения (в формате RGB)
      )

      if list_id not in self.data:
        self.data[list_id] = {
            "message_id": "",
            "link": "",
            "toggle": True,
            "main": main,
            "reserve": reserve,
            "start_time": f"{start_time}:00",
            "main_list": [],
            "reserve_list": []
        }

      main_list_str = ""
      for i in range(1, main + 1):  # Создаем строки с номерами от 1 до 20
        if i <= len(self.data[list_id]["main_list"]):
          main_list_str += f"``{i}.`` {self.data[list_id]['main_list'][i - 1]}\n"
        else:
          main_list_str += f"``{i}.``\n"

      reserve_list_str = ""
      for i in range(1, reserve +
                     1):  # Создаем строки с номерами от 1 до reserve + 1
        if i <= len(self.data[list_id]["reserve_list"]):
          reserve_list_str += f"``{i}.`` {self.data[list_id]['reserve_list'][i - 1]}\n"
        else:
          reserve_list_str += f"``{i}.``\n"
      self.save_data()

      embed.add_field(name="**MAIN**", value=main_list_str, inline=False)
      embed.add_field(name="**RESERVE**", value=reserve_list_str, inline=False)
      embed.set_footer(
          text=f"[{type}] Время начала {start_time}:00 / Voice {voice_time}:00"
      )

      self.message_sent = True
      self.message_id = list_id

      # Создаем кнопки
      await ctx.send(embed=embed,
                     components=[
                         Button(style=disnake.ButtonStyle.grey,
                                custom_id=f"{list_id}_add_button",
                                label="ADD",
                                emoji="➕"),
                         Button(style=disnake.ButtonStyle.green,
                                custom_id=f"{list_id}_def_button",
                                label="DEF",
                                emoji="🚑"),
                         Button(style=disnake.ButtonStyle.blurple,
                                custom_id=f"{list_id}_reserve_button",
                                label="RESERVE",
                                emoji="🔁"),
                         Button(style=disnake.ButtonStyle.red,
                                custom_id=f"{list_id}_cancel_button",
                                label="CANCEL",
                                emoji="❌"),
                         Button(style=disnake.ButtonStyle.red,
                                custom_id=f"{list_id}_delete_list_button",
                                label="УДАЛИТЬ",
                                emoji="🗑️"),
                         Button(style=disnake.ButtonStyle.blurple,
                                custom_id=f"{list_id}_toggle_buttons",
                                label="ЗАКРЫТЬ",
                                emoji="🔄")
                     ])
    else:
      await ctx.send("Нет у Вас прав на это", ephemeral=True)

  async def update_embed_and_buttons(self, list_id):
    if list_id:
      server_id, channel_id, message_id = map(
          int, self.data[list_id]["link"].split("/")[4:7])
      # Получаем объект сервера
      server = disnake.utils.get(self.bot.guilds, id=server_id)

      # Получаем объект канала
      channel = disnake.utils.get(server.channels, id=channel_id)
      # Получаем объект сообщения
      try:
        message = await channel.fetch_message(message_id)
        current_embed = message.embeds[0]
        main_list_str = ""
        reserve_list_str = ""

        for i in range(1, self.data[list_id]["main"] + 1):
          if i <= len(self.data[list_id]["main_list"]):
            main_list_str += f"``{i}.`` {self.data[list_id]['main_list'][i - 1]}\n"
          else:
            main_list_str += f"``{i}.``\n"

        for i in range(1, self.data[list_id]["reserve"] + 1):
          if i <= len(self.data[list_id]["reserve_list"]):
            reserve_list_str += f"``{i}.`` {self.data[list_id]['reserve_list'][i - 1]}\n"
          else:
            reserve_list_str += f"``{i}.``\n"

        current_embed.set_field_at(0,
                                   name="**MAIN**",
                                   value=main_list_str,
                                   inline=False)
        current_embed.set_field_at(1,
                                   name="**RESERVE**",
                                   value=reserve_list_str,
                                   inline=False)

        # Создайте списки для кнопок в каждой строке
        components_row1 = [
            disnake.ui.Button.from_component(row)
            for row in message.components[0].children
        ]
        components_row2 = [
            disnake.ui.Button.from_component(row)
            for row in message.components[1].children
        ]

        # Создайте строки ActionRow
        action_row1 = disnake.ui.ActionRow(*components_row1)
        action_row2 = disnake.ui.ActionRow(*components_row2)

        await message.edit(embed=current_embed,
                           components=[action_row1, action_row2])
      except disnake.errors.NotFound:
        print("Сообщение не найдено.")
      except disnake.errors.Forbidden:
        print("У бота нет прав для просмотра сообщения.")
      except disnake.errors.HTTPException:
        print("Произошла ошибка при выполнении HTTP-запроса.")

  @commands.slash_command(name="дел",
                          description="Удалить пользователя из списка.",
                          options=[
                              disnake.Option("list_id",
                                             "Идентификатор списка",
                                             type=disnake.OptionType.string,
                                             required=True),
                              disnake.Option("user",
                                             "Пользователь для удаления",
                                             type=disnake.OptionType.user,
                                             required=True)
                          ])
  async def удалить_пользователя(self, ctx, list_id: str,
                                 user: disnake.Member):
    if self.is_admin_or_has_role(ctx.author):
      if list_id in self.data:
        if user.mention in self.data[list_id]["main_list"]:
          self.data[list_id]["main_list"].remove(user.mention)
          self.save_data()
          # Отправить сообщение в личные сообщения пользователю
          await user.send(
              f"Вы были удалены из списка [{list_id}] {self.data[list_id]['link']} by {ctx.author.mention}."
          )
          await ctx.send(f"{user.mention} был удален из списка '{list_id}'.",
                         ephemeral=True)
          await self.update_embed_and_buttons(list_id)
        elif user.mention + " / def" in self.data[list_id]["main_list"]:
          self.data[list_id]["main_list"].remove(user.mention + " / def")
          self.save_data()
          # Отправить сообщение в личные сообщения пользователю
          await user.send(
              f"Вы были удалены из списка [{list_id}] {self.data[list_id]['link']} by {ctx.author.mention}."
          )
          await ctx.send(f"{user.mention} был удален из списка '{list_id}'.",
                         ephemeral=True)
          await self.update_embed_and_buttons(list_id)
        elif user.mention in self.data[list_id]["reserve_list"]:
          self.data[list_id]["reserve_list"].remove(user.mention)
          self.save_data()
          # Отправить сообщение в личные сообщения пользователю
          await user.send(
              f"Вы были удалены из списка [{list_id}] {self.data[list_id]['link']} by {ctx.author.mention}."
          )
          await ctx.send(f"{user.mention} был удален из списка '{list_id}'.",
                         ephemeral=True)
          await self.update_embed_and_buttons(list_id)
        else:
          await ctx.send(f"{user.mention} не найден в списке '{list_id}'.",
                         ephemeral=True)
      else:
        await ctx.send(f"Список с идентификатором '{list_id}' не найден.",
                       ephemeral=True)
    else:
      await ctx.send("Нет у Вас прав на это", ephemeral=True)

  @commands.slash_command(name="доб",
                          description="Добавить пользователя в список.",
                          options=[
                              disnake.Option("list_id",
                                             "Идентификатор списка",
                                             type=disnake.OptionType.string,
                                             required=True),
                              disnake.Option(
                                  "list_name",
                                  "Название позиции",
                                  type=disnake.OptionType.string,
                                  choices=["main", "main def", "reserve"],
                                  required=True),
                              disnake.Option("user",
                                             "Пользователь для добавления",
                                             type=disnake.OptionType.user,
                                             required=True)
                          ])
  async def добавить_пользователя(self, ctx, list_id: str, list_name: str,
                                  user: disnake.Member):
    if self.is_admin_or_has_role(ctx.author):
      if list_id in self.data:
        start_time = datetime.strptime(self.data[list_id]["start_time"],
                                       "%H:%M").time()
        current_time = datetime.now().time()
        if len(self.data[list_id]["main_list"]
               ) < self.data[list_id]["main"] and list_name == "main":
          if user.mention not in self.data[list_id][
              "main_list"] and user.mention not in self.data[list_id][
                  "reserve_list"] and user.mention + " / def" not in self.data[
                      list_id]["main_list"]:
            self.data[list_id]["main_list"].append(user.mention)
            self.save_data()
            await user.send(
                f"Вы были добавлены в список [{list_id}] {self.data[list_id]['link']} by {ctx.author.mention}."
            )
            await ctx.send(
                f"{user.mention} был добавлен в список '{list_id}'.",
                ephemeral=True)
            await self.update_embed_and_buttons(list_id)
          else:
            await ctx.send(f"{user.mention} уже в списке.", ephemeral=True)
        elif len(self.data[list_id]["main_list"]
                 ) < self.data[list_id]["main"] and list_name == "main def":
          if user.mention not in self.data[list_id][
              "main_list"] and user.mention not in self.data[list_id][
                  "reserve_list"] and user.mention + " / def" not in self.data[
                      list_id]["main_list"]:
            self.data[list_id]["main_list"].append(f"{user.mention} / def")
            self.save_data()
            await user.send(
                f"Вы были добавлены в список [{list_id}] {self.data[list_id]['link']} by {ctx.author.mention}."
            )
            await ctx.send(
                f"{user.mention} был добавлен в список '{list_id}'.",
                ephemeral=True)
            await self.update_embed_and_buttons(list_id)
          else:
            await ctx.send(f"{user.mention} уже в списке.", ephemeral=True)

        elif len(self.data[list_id]["reserve_list"]
                 ) < self.data[list_id]["reserve"] and list_name == "reserve":
          if user.mention not in self.data[list_id][
              "main_list"] and user.mention not in self.data[list_id][
                  "reserve_list"] and user.mention + " / def" not in self.data[
                      list_id]["main_list"]:
            self.data[list_id]["reserve_list"].append(user.mention)
            self.save_data()
            await user.send(
                f"Вы были добавлены в список [{list_id}] {self.data[list_id]['link']} by {ctx.author.mention}."
            )
            await ctx.send(
                f"{user.mention} был добавлен в список '{list_id}'.",
                ephemeral=True)
            await self.update_embed_and_buttons(list_id)
          else:
            await ctx.send(f"{user.mention} уже в списке.", ephemeral=True)
        else:
          await ctx.send(
              f"Нет свободных мест в списке и в списке '{list_id}'.",
              ephemeral=True)
      else:
        await ctx.send(f"Список с идентификатором '{list_id}' не найден.",
                       ephemeral=True)
    else:
      await ctx.send("Нет у Вас прав на это", ephemeral=True)

  @commands.Cog.listener()
  async def on_button_click(self, inter):
    success = False
    list_id = inter.data["custom_id"].split("_")[0]

    if list_id is None:
      return

    if inter.response.is_done():
      return

    current_time = datetime.now().time()
    if inter.component.custom_id.endswith("_add_button"):
      start_time = datetime.strptime(self.data[list_id]["start_time"],
                                     "%H:%M").time()
      if len(self.data[list_id]["main_list"]) < self.data[list_id]["main"]:
        success = True
        if inter.author.mention not in self.data[list_id][
            "main_list"] and inter.author.mention not in self.data[list_id][
                "reserve_list"] and inter.author.mention + " / def" not in self.data[
                    list_id]["main_list"]:
          self.data[list_id]["main_list"].append(inter.author.mention)
        else:
          await inter.send("Вы уже в списке!", ephemeral=True)
      else:
        await inter.send("Мест в основном списке больше нет.", ephemeral=True)
    elif inter.component.custom_id.endswith("_def_button"):
      start_time = datetime.strptime(self.data[list_id]["start_time"],
                                     "%H:%M").time()
      if len(self.data[list_id]["main_list"]) < self.data[list_id]["main"]:
        success = True
        if inter.author.mention not in self.data[list_id][
            "main_list"] and inter.author.mention not in self.data[list_id][
                "reserve_list"] and inter.author.mention + " / def" not in self.data[
                    list_id]["main_list"]:
          self.data[list_id]["main_list"].append(
              f"{inter.author.mention} / def")
        else:
          await inter.send("Вы уже в списке!", ephemeral=True)
      else:
        await inter.send("Мест в деф. списке больше нет.", ephemeral=True)
    elif inter.component.custom_id.endswith("_reserve_button"):
      start_time = datetime.strptime(self.data[list_id]["start_time"],
                                     "%H:%M").time()
      if len(
          self.data[list_id]["reserve_list"]) < self.data[list_id]["reserve"]:
        success = True
        if inter.author.mention not in self.data[list_id][
            "main_list"] and inter.author.mention not in self.data[list_id][
                "reserve_list"] and inter.author.mention + " / def" not in self.data[
                    list_id]["main_list"]:
          self.data[list_id]["reserve_list"].append(inter.author.mention)
        else:
          await inter.send("Вы уже в списке!", ephemeral=True)
      else:
        await inter.send("Мест в списке резервов больше нет.", ephemeral=True)
    elif inter.component.custom_id.endswith("_cancel_button"):
      start_time = datetime.strptime(self.data[list_id]["start_time"],
                                     "%H:%M").time()
      if inter.author.mention in self.data[list_id]["reserve_list"]:
        self.data[list_id]["reserve_list"].remove(inter.author.mention)
        success = True
      elif inter.author.mention + " / def" in self.data[list_id]["main_list"]:
        self.data[list_id]["main_list"].remove(f"{inter.author.mention} / def")
        success = True
      elif inter.author.mention in self.data[list_id]["main_list"]:
        self.data[list_id]["main_list"].remove(inter.author.mention)
        success = True
      else:
        await inter.send("Вас нет в списках!", ephemeral=True)
    elif inter.component.custom_id.endswith("_delete_list_button"):
      if self.is_admin_or_has_role(inter.author):
        if list_id in self.data:
          del self.data[list_id]  # Удаляем список из данных
          self.save_data()  # Сохраняем обновленные данные
          await inter.message.delete()  # Удаляем сообщение с кнопками
          await inter.send(f"Список с идентификатором '{list_id}' удален.",
                           ephemeral=True)
        else:
          await inter.send(f"Список с идентификатором '{list_id}' не найден.",
                           ephemeral=True)
      else:
        await inter.send("У вас нет прав на удаление списка.", ephemeral=True)
    elif inter.component.custom_id.endswith("_toggle_buttons"):
      if self.is_admin_or_has_role(inter.author):
        if self.data[list_id]["toggle"]:
          for button in inter.message.components[0].children:
            if button.custom_id.startswith(f"{list_id}_"):
              if button.custom_id == f"{list_id}_add_button" or button.custom_id == f"{list_id}_def_button" or button.custom_id == f"{list_id}_reserve_button" or button.custom_id == f"{list_id}_cancel_button":
                button.disabled = True

          for button in inter.message.components[1].children:
            if button.custom_id.startswith(f"{list_id}_"):
              if button.custom_id == f"{list_id}_toggle_buttons":
                button.label = "ОТКРЫТЬ"

          # Создайте списки для кнопок в каждой строке
          components_row1 = [
              disnake.ui.Button.from_component(row)
              for row in inter.message.components[0].children
          ]
          components_row2 = [
              disnake.ui.Button.from_component(row)
              for row in inter.message.components[1].children
          ]

          # Создайте строки ActionRow
          action_row1 = disnake.ui.ActionRow(*components_row1)
          action_row2 = disnake.ui.ActionRow(*components_row2)

          # Обновите сообщение с новыми состояниями кнопок
          self.data[list_id]["toggle"] = False
          self.save_data()  # Сохраняем обновленные данные
          await inter.message.edit(components=[action_row1, action_row2])
          await inter.send("Список закрыт", ephemeral=True)
        else:
          for button in inter.message.components[0].children:
            if button.custom_id.startswith(f"{list_id}_"):
              if button.custom_id == f"{list_id}_add_button" or button.custom_id == f"{list_id}_def_button" or button.custom_id == f"{list_id}_reserve_button" or button.custom_id == f"{list_id}_cancel_button":
                button.disabled = False

          for button in inter.message.components[1].children:
            if button.custom_id.startswith(f"{list_id}_"):
              if button.custom_id == f"{list_id}_toggle_buttons":
                button.label = "ЗАКРЫТЬ"

          # Создайте списки для кнопок в каждой строке
          components_row1 = [
              disnake.ui.Button.from_component(row)
              for row in inter.message.components[0].children
          ]
          components_row2 = [
              disnake.ui.Button.from_component(row)
              for row in inter.message.components[1].children
          ]

          # Создайте строки ActionRow
          action_row1 = disnake.ui.ActionRow(*components_row1)
          action_row2 = disnake.ui.ActionRow(*components_row2)

          # Обновите сообщение с новыми состояниями кнопок
          self.data[list_id]["toggle"] = True
          self.save_data()  # Сохраняем обновленные данные
          await inter.message.edit(components=[action_row1, action_row2])
          await inter.send("Список открыт", ephemeral=True)
      else:
        await inter.send("У вас нет прав на отключение кнопок.",
                         ephemeral=True)

    if success:
      self.save_data()
      if inter.message:
        current_embed = inter.message.embeds[0]
        main_list_str = ""
        reserve_list_str = ""

        for i in range(1, self.data[list_id]["main"] + 1):
          if i <= len(self.data[list_id]["main_list"]):
            main_list_str += f"``{i}.`` {self.data[list_id]['main_list'][i - 1]}\n"
          else:
            main_list_str += f"``{i}.``\n"

        for i in range(1, self.data[list_id]["reserve"] + 1):
          if i <= len(self.data[list_id]["reserve_list"]):
            reserve_list_str += f"``{i}.`` {self.data[list_id]['reserve_list'][i - 1]}\n"
          else:
            reserve_list_str += f"``{i}.``\n"

        current_embed.set_field_at(0,
                                   name="**MAIN**",
                                   value=main_list_str,
                                   inline=False)
        current_embed.set_field_at(1,
                                   name="**RESERVE**",
                                   value=reserve_list_str,
                                   inline=False)
        # Создайте списки для кнопок в каждой строке
        components_row1 = [
            disnake.ui.Button.from_component(row)
            for row in inter.message.components[0].children
        ]
        components_row2 = [
            disnake.ui.Button.from_component(row)
            for row in inter.message.components[1].children
        ]

        # Создайте строки ActionRow
        action_row1 = disnake.ui.ActionRow(*components_row1)
        action_row2 = disnake.ui.ActionRow(*components_row2)

        if inter.response.is_done():
          return

        await inter.response.edit_message(
            embed=current_embed, components=[action_row1, action_row2])


def setup(bot: commands.Bot):
  bot.add_cog(список(bot))
