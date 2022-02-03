import asyncio
import discord
from src.extras.emojis import *
from discord.ext import commands
from src.extras.func import db_push_object, db_fetch_object


async def secondary_callback(
        ctx: commands.Context, bot: discord.Client, event: str,
        value: int, message: discord.Message, db_data: dict):

    if value == 1:

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(embed=discord.Embed(description='Type your custom message below:'))
        try:
            resp = await bot.wait_for('message', check=check, timeout=300)
            await ctx.send(embed=discord.Embed(title=f'{Emo.CHECK} Done!', description=f'> {resp.content}'))
            db_data[event] = resp.content
            await db_push_object(ctx.guild.id, db_data, 'text')
        except asyncio.TimeoutError:
            await ini.channel.send('Bye! you took too long to respond!')
    elif value == 2:
        db_data[event] = ''
        await db_push_object(ctx.guild.id, db_data, 'text')
        await ctx.send(embed=discord.Embed(
            title=f'{Emo.WARN} Done!',
            description=f'> Removed custom **{event}** message'))
    elif value == 3:
        await message.delete()


class BaseView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        super().__init__()
        self.value = None

    @discord.ui.button(label='Welcome', style=discord.ButtonStyle.green, emoji=f'{Emo.IMG}')
    async def welcome(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.ctx.author == interaction.user:
            self.value = 1
            self.stop()

    @discord.ui.button(label='Upload', style=discord.ButtonStyle.blurple, emoji=f'{Emo.YT}')
    async def upload(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.ctx.author == interaction.user:
            self.value = 2
            self.stop()

    @discord.ui.button(label='Live', style=discord.ButtonStyle.red, emoji=f'{Emo.LIVE}')
    async def live(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.ctx.author == interaction.user:
            self.value = 3
            self.stop()


class ActionView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        super().__init__()
        self.value = None

    @discord.ui.button(label='Edit', style=discord.ButtonStyle.green)
    async def edit(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.ctx.author == interaction.user:
            self.value = 1
            self.stop()

    @discord.ui.button(label='Remove', style=discord.ButtonStyle.blurple)
    async def remove(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.ctx.author == interaction.user:
            self.value = 2
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.ctx.author == interaction.user:
            self.value = 3
            self.stop()


async def sub_view_msg(bot: discord.Client, ctx: commands.Context, interaction: discord.Interaction):

    default_welcome = '................................................(default)'
    default_upload = '...................................................(default)'
    default_live = '................................................(default)'

    db_data = await db_fetch_object(guild_id=ctx.guild.id, key='text')
    if db_data:
        welcome_text = db_data.get('welcome') or default_welcome
        upload_text = db_data.get('upload') or default_upload
        live_text = db_data.get('live') or default_live
    else:
        db_data = {}
        welcome_text = default_welcome
        upload_text = default_upload
        live_text = default_live

    emd = discord.Embed(
        title=f'{Emo.CUSTOM} Custom Messages',
        description=f'**`Welcome`** {welcome_text}'
                    f'\n\n**`Upload`** {upload_text}'
                    f'\n\n**`Livestream`** {live_text}')
    await interaction.response.defer()
    await interaction.message.delete()
    initial_view = BaseView(ctx)
    root_message = await ctx.send(embed=emd, view=initial_view)

    await initial_view.wait()

    if initial_view.value == 1:
        welcome_actions = ActionView(ctx)
        emd = discord.Embed(
            title=f'{Emo.IMG} Welcome Message',
            description=f'**Formatting Scopes**'
                        f'\n> `[guild.name]` will be replaced with the server name'
                        f'\n> `[ping.member]` this will ping the member with the card'
                        f'\n> `[member.name]` will be replaced with the member name'
                        f'\n> `[member.mention]` will be replaced with the member mention'
                        f'\n\nTap **`Edit`** to create a custom welcome message')
        emd.set_footer(text='You can mention any text channel directly inside the custom message')
        new = await root_message.edit(embed=emd, view=welcome_actions)
        await welcome_actions.wait()
        await secondary_callback(ctx, bot, 'welcome', welcome_actions.value, new, db_data)

    elif initial_view.value == 2:
        upload_actions = ActionView(ctx)
        emd = discord.Embed(
            title=f'{Emo.YT} YT Upload Message',
            description=f'**Formatting Scopes**'
                        f'\n> `[ping]` will be replaced with the  role ping'
                        f'\n> `[url]` will be replaced with youtube video url'
                        f'\n> `[name]` will be replaced with youtube channel name'
                        f'\n\nTap **`Edit`** to create a custom youtube upload message')
        emd.set_footer(text='You can mention any text channel directly inside the custom message')
        new = await root_message.edit(embed=emd, view=upload_actions)
        await upload_actions.wait()
        await secondary_callback(ctx, bot, 'upload', upload_actions.value, new, db_data)

    elif initial_view.value == 3:
        live_actions = ActionView(ctx)
        emd = discord.Embed(
            title=f'{Emo.LIVE} YT Live Message',
            description=f'**Formatting Scopes**'
                        f'\n> `[ping]` will be replaced with the  role ping'
                        f'\n> `[url]` will be replaced with youtube video url'
                        f'\n> `[name]` will be replaced with youtube channel name'
                        f'\n\nTap **`Edit`** to create a custom youtube live message')
        emd.set_footer(text='You can mention any text channel directly inside the custom message')
        new = await root_message.edit(embed=emd, view=live_actions)
        await live_actions.wait()
        await secondary_callback(ctx, bot, 'live', live_actions.value, new, db_data)
