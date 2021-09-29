from datetime import datetime

from discord.ext import tasks
from discord import Client, Embed

from lib.scoreboard import ECSC_Stats


CHANNEL_ID = "<The channel ID where you want the bot to send messages>"
BOT_TOKEN = "<Bot token>"
EACH_X_MINUTES = 15

FLAGS = {
    "France": ":flag_fr:",
    "Poland": ":flag_pl:",
    "Italy": ":flag_it:",
    "Romania": ":flag_ro:",
    "Denmark": ":flag_dk:",
    "Switzerland": ":flag_ch:",
    "Cyprus": ":flag_cy:",
    "Netherlands": ":flag_nl:",
    "Austria": ":flag_at:",
    "Belgium": ":flag_be:",
    "Portugal": ":flag_pt:",
    "Spain": ":flag_es:",
    "Greece": ":flag_gr:",
    "Slovenia": ":flag_si:",
    "Ireland": ":flag_ie:",
    "Slovakia": ":flag_sk:",
    "Malta": ":flag_mt:",
    "Germany": ":flag_de:"
}

class MyClient(Client):
    async def on_ready(self):
        self.channel = await self.fetch_channel(CHANNEL_ID)
        self.ecsc_stats = ECSC_Stats()
        
        # Start loops
        self.refresh_and_show_deltas.start()

        await self.channel.send("Bonjour :french_bread:")

        print(f'Logged on as {self.user}!')

    @tasks.loop(minutes=EACH_X_MINUTES)
    async def refresh_and_show_deltas(self):
        await self.ecsc_stats.refresh()
        if self.ecsc_stats.old_scoreboard == self.ecsc_stats.scoreboard:
            print(f"{datetime.now().strftime('[%d/%m/%Y %H:%M:%S]')} Stats are the same, not showing leaderboard..")
            return

        deltas = self.ecsc_stats.get_deltas()

        text = ""
        for country in deltas:
            emoji = ":black_small_square:"
            if country.delta == 1:
                emoji = ":small_red_triangle:"
            elif country.delta == 2:
                emoji = ":small_red_triangle_down:"
            text += f"{emoji} {country.index}. {FLAGS[country.name]} {country.name} {':heart:' if country.name == 'France' else ''}, {country.points} points\n"

        embed = Embed(title=":crossed_swords: Leaderboard :flag_eu:", description=text)
        embed.set_footer(text="Allez la France")
        await self.channel.send(embed=embed)

client = MyClient()
client.run(BOT_TOKEN)
