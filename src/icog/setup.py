import discord
from typing import Any
from src.extras.emojis import *
from discord.ext import commands
from src.views.subARole import sub_view_arole
from src.views.subPrefix import sub_view_prefix
from src.views.subYouTube import sub_view_youtube
from src.views.subReceiver import sub_view_receiver
from src.views.subReception import sub_view_reception
from src.views.subJoincard import sub_view_welcomecard
from extslash import *
from extslash.commands import SlashCog, ApplicationContext, Client


class BaseView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = 180
        self.value = None
        self.message = None

    async def on_timeout(self):
        try:
            await self.message.delete()
        except Exception:
            return


class CommandMenu(discord.ui.Select):

    def __init__(self, ctx: Any, bot: discord.Client):

        self.bot = bot
        self.ctx = ctx

        options = [
            discord.SelectOption(label='\u200b', value='100', emoji=Emo.CROSS),
            discord.SelectOption(label='Prefix', value='0', emoji=Emo.TAG),
            discord.SelectOption(label='YouTube', value='2', emoji=Emo.YT),
            discord.SelectOption(label='Receiver', value='1', emoji=Emo.PING),
            discord.SelectOption(label='Reception', value='3', emoji=Emo.DEAL),
            discord.SelectOption(label='Alert Role', value='5', emoji=Emo.BELL),
            discord.SelectOption(label='Welcome Card', value='4', emoji=Emo.IMG),
        ]

        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
            placeholder='select a command'
        )

    async def callback(self, interaction: discord.Interaction):

        if interaction.user == self.ctx.author:

            if int(self.values[0]) == 0:
                await sub_view_prefix(ctx=self.ctx, interaction=interaction, bot=self.bot)

            elif int(self.values[0]) == 1:
                await sub_view_receiver(ctx=self.ctx, interaction=interaction, bot=self.bot)

            elif int(self.values[0]) == 2:
                await sub_view_youtube(ctx=self.ctx, interaction=interaction, bot=self.bot)

            elif int(self.values[0]) == 3:
                await sub_view_reception(ctx=self.ctx, interaction=interaction, bot=self.bot)

            elif int(self.values[0]) == 4:
                await sub_view_welcomecard(ctx=self.ctx, interaction=interaction, bot=self.bot)

            elif int(self.values[0]) == 5:
                await sub_view_arole(ctx=self.ctx, interaction=interaction, bot=self.bot)

            elif int(self.values[0]) == 6:
                await sub_view_streamer(ctx=self.ctx, interaction=interaction, bot=self.bot)

            elif int(self.values[0]) == 100:
                try:
                    await interaction.message.delete()
                except discord.errors.NotFound:
                    pass
            else:
                pass
        else:
            await interaction.response.send_message(
                'You are not allowed to control this message!', ephemeral=True
            )


class Setup(SlashCog):
    def __init__(self, bot: Client):
        self.bot = bot

    def register(self):
        return SlashCommand(name='setup', description='Setup PixeL for your Server')

    async def command(self, appctx: ApplicationContext):
        if appctx.author.guild_permissions.administrator:
            emd = discord.Embed(title=f'{Emo.SETUP} use menu below to setup', colour=0x005aef)
            emd.set_footer(text=f'⏱️ this menu will disappear after 3 minutes')
            view = BaseView()
            view.add_item(CommandMenu(appctx, self.bot))
            await appctx.respond(embed=emd)
            view.message = await appctx.send(content='\u200b', view=view)
        else:
            await appctx.respond(
                embed=discord.Embed(title=f'{Emo.WARN} You are not an **ADMIN** {Emo.WARN}'), ephemeral=True)


def setup(bot: Client):
    bot.add_slash_cog(Setup(bot))