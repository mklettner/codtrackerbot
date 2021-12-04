import aiohttp
import discord
import logging
from tabulate import tabulate
from codtrackerbot.models import codtrackermodel
from sqlite3 import Error
import aiosqlite

sql_create_table = '''CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name TEXT type UNIQUE NOT NULL, platform TEXT NOT NULL);'''


class CodTracker(discord.ext.commands.Cog, name='Warzone'):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @discord.ext.commands.command(name="add_user")
    async def add_user(self, ctx, user: str, platform: str):
        db = await aiosqlite.connect("sqlite.db")
        cursor = await db.cursor()
        sql = ' INSERT INTO users(name,platform) VALUES(?,?) '
        try:
            await cursor.execute(sql, (user, platform))
            await db.commit()
        except Error as e:
            self.logger.error(e)
        finally:
            await cursor.close()
            await db.close()
        await ctx.send(f'User {user} added to DB')

    @discord.ext.commands.command(name="get_user")
    async def get_user(self, ctx):
        db = await aiosqlite.connect("sqlite.db")
        cursor = await db.cursor()
        sql = ' SELECT * FROM users'
        try:
            await cursor.execute(sql)
            rows = await cursor.fetchall()
        except Error as e:
            self.logger.error(e)
        finally:
            await cursor.close()
            await db.close()
        await ctx.send(f'Users: {rows}')

    @discord.ext.commands.command(name="wzstats")
    async def adhoc_play(self, ctx, username: str):
        self.logger.debug("wzstats command executed")

        h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Accept": "application/json"
        }

        async with aiohttp.ClientSession() as client:
            async with client.get(
                    f"https://api.tracker.gg/api/v2/warzone/standard/matches/battlenet/{username}?type=wz",
                    headers=h) as resp:
                data = await resp.json()

        resp.raise_for_status()
        raw_matches = data["data"]["matches"]
        matches = [codtrackermodel.Match(**m) for m in raw_matches if "Plunder" not in m["metadata"]["modeName"]]
        table_data = []
        for match in matches:
            table_data.append(
                [match.segments[0].stats.teamPlacement.displayValue, match.metadata.modeName, match.attributes.avgKd.kd,
                 match.segments[0].stats.kills.displayValue, match.segments[0].stats.kdRatio.displayValue])
        await ctx.send(tabulate(table_data, headers=["Placement", "Mode", "Lobby KD", "Kills", "KD Ratio"]))
