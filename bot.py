import os
import json
import disnake
from disnake.ext import commands
import datetime
from datetime import date
from typing import Optional
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') # Путь до файла с переменными окружения
if os.path.exists(dotenv_path):
    load_dotenv("C:\Users\matve\AppData\Local\Programs\Python\Python311\.env.txt")


settings = {
    "token" : BOT_TOKEN,
    "badwords" : BOT_BADLIST,
    "prefix": BOT_PREFIX
}
badlist = settings[badwords].split()
bot = commands.Bot(command_prefix=settings[prefix], help_command=None, intents=disnake.Intents.all(), test_guilds=[1100747106135855176])

@bot.event
async def on_ready():
    print(f"Bot{bot.user} is ready to work")


@bot.event
async def on_member_join(member):
    role = disnake.utils.get(member.guild.roles, id=1115580756228575264)
    channel = member.guild.system_channel
    embed = disnake.Embed(
        title="Приветики!",
        description=f"{member.name}#{member.discriminator} добрался до горы Мьёбоку",
        color=999950
    )
    embed.set_image(url='https://i.ytimg.com/vi/sY_duhW4tH4/maxresdefault.jpg')
    await member.add_roles(role)
    await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    print(error)

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author}, тебе не хватает ненависти, попроси Орочимару(Георгия) дать тебе силы')
    elif isinstance(error, commands.UserInputError):
        await ctx.send(embed=disnake.Embed(
            description=f'Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.brief}\nExample: {ctx.prefix}{ctx.command.usage}'
        ))


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    mes = message.content.split()
    for content in mes:
        for badword in badlist:
            if content.lower() == badword:
                await message.delete()
                await message.channel.send(f'{message.author.mention} это что за безобразие? Слово "{content}" порядочные люди не используют!')


@bot.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member:disnake.Member, *, reason='Нарушение правил.'):
    await ctx.send(f'Этот властный и грозный человек {ctx.author.mention} исключил негодяя (пользователя) {member.mention} из нашего теплого, сугубо круглого кружка')
    await member.kick(reason=reason)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member:disnake.Member, *, reason = 'Нарушение правил.'):
    await ctx.send(f'Этот властный и грозный человек {ctx.author.mention} забанил негодяя (пользователя) {member.mention}')
    await member.ban(reason=reason)
    await ctx.message.delete()


@bot.command()
@commands.has_permissions()
async def todo(ctx, role=1111239786720661596):
    with open('todo.txt', encoding="utf-8") as f:
        string = f.read().split('\n')
    for i in string:
       info = i.split(';')


       embed = disnake.Embed(
       title=info[0].upper(),
       description=str(info[-1]),
       color=999950,
       )

       if role==int(info[1]):
            await ctx.send(embed=embed, delete_after=10)
       else:
           await ctx.send('err')


@bot.slash_command()
async def add(inter, deadline: str, description: str):
    deadline = datetime.datetime.strptime(deadline, '%d.%m.%y').date()

    with open('todo.txt', 'a', encoding="utf-8") as file:
        file.write(deadline.strftime('%y.%d.%m') + ';' + description + '\n')
    await inter.send('Успешно добавлено')

class Menu(disnake.ui.View):
    def __int__(self):
        super().__init__(timeout=10.0)
        self.value = Optional[bool]
        self.span=''
        self.stop()


    @disnake.ui.button(label = 'Day', style=disnake.ButtonStyle.green, emoji='🐣')
    async def Day(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.span = 'd'
        self.stop()


    @disnake.ui.button(label='Month', style=disnake.ButtonStyle.red, emoji='👌')
    async def Month(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.span = 'm'
        self.stop()

    @disnake.ui.button(label='Year', style=disnake.ButtonStyle.grey, emoji='🌈')
    async def Year(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        self.span = 'y'
        self.stop()

    def nes_events(self):
        nes_dates = []
        today = date.today().strftime('%y.%d.%m').split('.')
        date_list = []
        with open('todo.txt', 'r', encoding="utf-8") as f:

            list_of_lines = f.read().split('\n')
            for i in range(0, len(list_of_lines), 1):
                a = list_of_lines[i].split(';')
                date_list.extend(a)

        for i in range(0, len(date_list), 2):
            if self.span == 'd' and date_list[i] == date.today().strftime('%y.%d.%m'):
                nes_dates.append(date_list[i] + '\t' + date_list[i + 1])

            elif self.span == 'm' and date_list[i].split('.')[0] == today[0] and date_list[i].split('.')[2] == today[2]:
                nes_dates.append(date_list[i] + '\t' + date_list[i + 1])

            elif self.span == 'y' and date_list[i].split('.')[0] == today[0]:
                nes_dates.append(date_list[i] + '\t' + date_list[i + 1])

        return nes_dates

#--------------------------------------------------------------------------------------------------------------
@bot.command()
async def menu(ctx):
    view = Menu()
    await ctx.send('Выберите список задач по дате', view=view)
    await view.wait()

    listik = Menu.nes_events(view)
    res = ''
    for i in listik:
        res += i + '\n'

    embed = disnake.Embed(
        title=res,
        description='Задачи',
        color=999950,
    )

    if view.span == 'd':
        await ctx.send('Задачи на сегодня:')
        await ctx.send(embed=embed)

    elif view.span == 'm':
        await ctx.send('Задачи на текущий месяц:')
        await ctx.send(embed=embed)

    elif view.span == 'y':
        await ctx.send('Задачи на текущий год:')
        await ctx.send(embed=embed)

    else:
        await ctx.send('Время ожидания истекло!')


bot.run(settings[token])
