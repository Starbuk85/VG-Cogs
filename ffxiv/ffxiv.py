import discord
from discord.ext import commands
try: # check if BeautifulSoup4 is installed
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False
import aiohttp
import asyncio

def setup(bot):
    if soupAvailable:
        bot.add_cog(Mycog(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")


class FFXIV:
    """FFXIV

    Misc Utilities for Final Fantasy XIV"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lodestone(self, server_name: str, char_fname: str, char_lname: str):
        """Returns lodestone link for selected character"""

        url = "http://na.finalfantasyxiv.com/lodestone/character/"
        search_url = url + "q=" + char_fname + "+" + char_lname + "&worldname=" + server_name
        char_name = char_fname + " " + char_lname

        async with aiohttp.get(search_url) as response:
            searchObject = BeautifulSoup(await response.text(), "html.parser")
        try:
            charid = searchObject.find(class_='player_name_gold').find('a').get_text()
			data = "```**" + char_name + "**\n"
			data += "\n"
			data += "```"
			await self.bot.say(data)
        except:
            await self.bot.say("Character could not be found in lodestone. Please check server and name spelling.")


def check_folder():
    if not os.path.exists("data/ffxiv"):
        print("Creating data/ffxiv folder...")
        os.makedirs("data/ffxiv")


def check_file():
    enabled = {}

    f = "data/ffxiv/enabled.json"
    if not fileIO(f, "check"):
        print("Creating default ffxiv's enabled.json...")
        fileIO(f, "save", enabled)


def setup(bot):
    check_folder()
    check_file()
    n = FFXIV(bot)
    bot.add_cog(n)