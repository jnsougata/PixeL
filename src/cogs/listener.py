import discord
import discord.errors
from discord.ext import commands
from src.extras.emojis import Emo


class Listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        invite = 'https://top.gg/bot/848304171814879273/invite'
        support = 'https://discord.gg/G9fk5HHkZ5'
        emd = discord.Embed(
            description=f'{Emo.MIC} Sup folks! I\'m **{guild.me.display_name}**'
                        f'\n\nTo get started, send `.help` | `@{guild.me.display_name} help` '
                        f'\n\nUse any one commands for everything:'
                        f'\n`/setup` | `.setup`'
                        f'\n\n**Important Links**'
                        f'\n[Invite]({invite}) - Add the bot to another server'
                        f'\n[Support Server]({support}) - Get some bot support here!',
            color=0xf2163b,
        )

        async def valid_intro_channel(_guild: discord.Guild):
            for channel in _guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    return channel

        intro = await valid_intro_channel(guild)

        if intro:
            try:
                await intro.send(embed=emd)
            except discord.errors.Forbidden:
                pass

        logger = self.bot.get_channel(899864601057976330)
        await logger.send(
            embed=discord.Embed(
                title=f'{Emo.MIC} {guild.name}',
                description=f'```\nOwner: {guild.owner}'
                            f'\n\nMembers: {guild.member_count}'
                            f'\n\nID: {guild.id}\n```',
                colour=discord.Colour.blurple()
            )
        )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        registry = self.bot.get_channel(899864601057976330)
        await registry.send(
            embed=discord.Embed(
                title=f'{Emo.MIC} {guild.name}',
                description=f'```\nInspect for suspicious activity\nGuild ID: {guild.id}\n```',
                colour=discord.Colour.red()
            )
        )


def setup(bot):
    bot.add_cog(Listeners(bot))
