import logging

import discord
import sys
import traceback
from discord.ext import commands


class CommandErrHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send('I do not know that command?!')
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Missing arguments')
        else:
            self.logger.exception(f'Ignoring exception in command {ctx.command}:')
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)