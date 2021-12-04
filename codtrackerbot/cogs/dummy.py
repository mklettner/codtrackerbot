import random
import discord
import logging


class Dummy(discord.ext.commands.Cog, name='Dummy module'):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @discord.ext.commands.command(name="hey")
    async def adhoc_play(self, ctx):
        self.logger.debug("hey command executed")
        await ctx.send(f'Hey {ctx.author.name}')

    @discord.ext.commands.command(name="99")
    async def brooklyn99_joke(self, ctx):
        self.logger.debug("99 command executed")
        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)

    @discord.ext.commands.command(name="roll_dice")
    async def roll_dice(self, ctx, number_of_dice: int, number_of_sides: int):
        self.logger.debug("roll_dice command executed")
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))