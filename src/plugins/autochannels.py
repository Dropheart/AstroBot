from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from discord.ext import commands

from .. import Embed


if TYPE_CHECKING:
    from .. import AstroBot


log = logging.getLogger(__name__)


class Autochannels(commands.Cog):
    def __init__(self, bot: AstroBot):
        self.bot = bot

    game_reviews_embed = (
        Embed(
            title='**Review Format**',
            description='Use the following template to post.\n```Game Name\n**Rating:** x/10\n**Playtime:** x hours\n**Review:** A few words about your thoughts on the game and why you gave it that rating```',
        )
        .set_thumbnail(url='https://cdn.discordapp.com/attachments/674660518371524609/828343777668235295/games.png')
        .add_field(
            name='<:pswarn:785145298720129024> **Follow the above template.**',
            value='Your message will be removed if it doesn\'t match the format.',
            inline=False,
        )
    )
    psn_friends_embed = (
        Embed(
            title='**LFG Post Format**',
            description='Use the following template to post.\n```\nYourPSNUsername\n\n**Games:** Game 1, Game 2, ...\n**Bio:**  A few words about yourself,\n          and who you\'re looking for\n**Timezone:** UTC+X/PST/etc```',
        )
        .set_thumbnail(url='https://cdn.discordapp.com/attachments/674660518371524609/828350579516112916/lfg.png')
        .add_field(
            name='<:pswarn:785145298720129024> **Follow the above template.**',
            value='Your messages will be removed if it doesn\'t match the format. You are allowed **one** post every **72 hours.**',
            inline=False,
        )
    )
    psn_friends_cooldown = {}

    def cooldown(self, id):
        if id not in self.psn_friends_cooldown:
            return False
        return self.psn_friends_cooldown[id] + 3600 * 72 > time.time()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 867753068003328000 and message.author.id != self.bot.application_id:
            if not (all(x in message.content.lower() for x in ['rating', 'playtime', 'review'])):
                await message.delete()
            else:
                async for msg in message.channel.history(limit=3):
                    if msg.author.id == self.bot.application_id:
                        await msg.delete()
                await message.channel.send(embed=self.game_reviews_embed)
        elif message.channel.id == 867800438715449384 and message.author.id != self.bot.application_id:
            if (not (all(x in message.content.lower() for x in ['games', 'bio', 'timezone']))) or self.cooldown(
                message.author.id
            ):
                await message.delete()
            else:
                async for msg in message.channel.history(limit=3):
                    if msg.author.id == self.bot.application_id:
                        await msg.delete()
                await message.channel.send(embed=self.psn_friends_embed)
                self.psn_friends_cooldown[message.author.id] = time.time()


def setup(bot: AstroBot):
    bot.add_cog(Autochannels(bot))
