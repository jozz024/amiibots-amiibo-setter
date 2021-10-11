import requests
import asyncio
from config import *

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user} and monitoring {amiiboname}'s matches, with {amiiboname_2} coming up next!")
    await bot.change_presence(
        status=nextcord.Status.idle,
        activity=nextcord.Activity(name=f"Pinging {USER} when their amiibo finish their amiibots run!", type=nextcord.ActivityType.playing),
    )

@bot.listen("on_message")
async def pingmii(message):
        message_send_channel = bot.get_channel(PINGCHANNEL)
        if message.author == bot.user:
            return
        if (
            (USERID in message.content or USER in message.content)
            and amiiboname in message.content
            and message.channel.id == SHOUTBOXID
            and (RATING_OR_MATCHES == "Matches" or None)
        ):
            amiibo = requests.get(OLD_AMIIBO_URL, headers=HEADERS).json()["data"]
            if amiibo["total_matches"] + 1 in MATCH_TURN_OFF_NUMBERS:
                disablepayload = {"is_active": False}
                disabled_amiibo = requests.put(
                    OLD_AMIIBO_URL, headers=HEADERS, json=disablepayload
                )
                await message_send_channel.send(
                    f"<@{USERID}> Your amiibo, {amiibo['name']}, finished its run with {amiibo['total_matches'] + 1} matches!"
                )
                if ENABLEAMIIBOID is not None:
                    enablepayload = {"is_active": True}
                    enableamiibo = requests.put(
                        NEW_AMIIBO_URL, headers=HEADERS, json=enablepayload
                    )
            if ENABLEAMIIBOID is not None and RATING_OR_MATCHES == "Rating":
                newamiibo = requests.get(NEW_AMIIBO_URL, headers=HEADERS).json()["data"]
                oldamiibo = requests.get(OLD_AMIIBO_URL, headers=HEADERS).json()["data"]
                if (
                    oldamiibo["rating"]
                    <= newamiibo["rating"]
                ):
                    disablepayload = {"is_active": False}
                    enablepayload = {"is_active": True}
                    disableoldamiibo = requests.put(
                        OLD_AMIIBO_URL, headers=HEADERS, json=disablepayload
                    )
                    enablenewamiibo = requests.put(
                        NEW_AMIIBO_URL, headers=HEADERS, json=enablepayload
                    )
                    await message_send_channel.send(
                        f"<@{USERID}> your amiibo have swithed due to rating changes"
                    )
                if (
                    newamiibo["rating"]
                    <= oldamiibo["rating"]
                ):
                    disablepayload = {"is_active": False}
                    enablepayload = {"is_active": True}
                    disablenewamiibo = requests.put(
                        NEW_AMIIBO_URL, headers=HEADERS, json=disablepayload
                    )
                    enableoldamiibo = requests.put(
                        OLD_AMIIBO_URL, headers=HEADERS, json=enablepayload
                    )
                    await message_send_channel.send(
                        f"<@{USERID}> your amiibo have swithed due to rating changes"
                    )
                    
@bot.command(name='currentamiibostats')
async def getcurrentamiibostats(ctx):
    amiibo = requests.get(OLD_AMIIBO_URL, headers=HEADERS).json()["data"]
    amiibo_win_percent = float(amiibo["win_percentage"]) * 100
    id_to_char = {value : key for (key, value) in CHARACTER_NAME_TO_ID_MAPPING.items()}
    await ctx.send(f'Name: {amiibo["name"]} \nCharacter: {str(id_to_char[amiibo["playable_character_id"]]).title()}\nRating: {round(amiibo["rating"], 2)} \nWin Rate: {amiibo_win_percent}% \nWins: {amiibo["wins"]} \nLosses: {amiibo["losses"]} \nTotal Matches: {amiibo["total_matches"]}')

loop = asyncio.get_event_loop()
loop.run_until_complete(
    bot.start(TOKEN)
)