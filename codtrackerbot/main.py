import logging
import aiohttp
import aiosqlite
from discord.ext import commands

from codtrackerbot.settings import settings
from codtrackerbot.cogs.dummy import Dummy
from codtrackerbot.cogs.command_err_handler import CommandErrHandler
from codtrackerbot.cogs.wzstats import CodTracker

logger = logging.getLogger('discord')
logger.setLevel(settings.log_level.upper())
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class MyBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix=command_prefix, **options)
        self.session = aiohttp.ClientSession(loop=self.loop)

    async def db_init(self):
        async with aiosqlite.connect("sqlite.db") as db:
            sql_create_table = 'CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name TEXT type UNIQUE NOT NULL, platform TEXT NOT NULL);'
            await db.execute(sql_create_table)
            await db.commit()

    async def on_ready(self):
        await self.db_init()
        guilds = [guild.name for guild in self.guilds]
        logger.info(f'{self.user.name} has connected to Discord guilds: {guilds}')


def main():
    bot = MyBot(command_prefix="!")

    bot.add_cog(Dummy(bot))
    bot.add_cog(CommandErrHandler(bot))
    bot.add_cog(CodTracker(bot))

    bot.run(settings.discord_bot_token)


if __name__ == "__main__":
    main()
