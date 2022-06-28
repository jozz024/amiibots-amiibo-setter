import nextcord
from nextcord.ext import commands
import os
import requests
import json
import asyncio
from datetime import datetime

bot = commands.Bot(command_prefix="!", description="")

def parse_config():
    with open("./config.json") as config:
        real_config = json.load(config)
    return real_config

def get_headers_from_key(api_key):
    if api_key.__contains__("Bearer"):
        headers = {"Authorization": api_key}
    else:
        headers = {"Authorization": f"Bearer {api_key}"}
    return headers

def get_amiibo_data(amiibo_id, headers):
    url = "https://www.amiibots.com/api/amiibo/" + amiibo_id
    data = requests.get(url, headers = headers).json()["data"]
    return data

def get_all_user_amiibo(user_id, headers):
    return requests.get(url=f'https://www.amiibots.com/api/amiibo/by_user_id/{user_id}', headers=headers).json()["data"]

def get_last_match(user_id, headers):
    datedict = {}
    amiibo = get_all_user_amiibo(user_id, headers)

    for amiibos in amiibo:
        if type(amiibos["last_match_time"]) != str:
            continue
        datedict[datetime.fromisoformat(amiibos["last_match_time"])] = amiibos["id"]
    current_date = datetime.now()
    cloz_dict = {
        abs(current_date.timestamp() - date.timestamp()) : date
        for date in datedict.keys()}

    res = cloz_dict[min(cloz_dict.keys())]

    return datedict[res]

def set_amiibo_data(amiibo_id, headers, payload):
    url = "https://www.amiibots.com/api/amiibo/" + amiibo_id
    requests.put(url, headers = headers, json = payload)

@bot.event
async def on_ready():
    config = parse_config()

    headers = get_headers_from_key(config["api_key"])

    amiibo_data = get_amiibo_data(config["to_watch"], headers)

    print(f"Logged on as {bot.user} and monitoring {amiibo_data['name']}'s matches!")

    await bot.change_presence(
        status=nextcord.Status.idle,
        activity=nextcord.Activity(
            name=f"Pinging {config['twitch_username']} when their amiibo finish their amiibots run!",
            type=nextcord.ActivityType.playing,
        ),
    )

@bot.listen("on_message")
async def on_message(message: nextcord.message.Message):
    config = parse_config()

    if message.channel.id != config["shoutbox_id"]:
        return

    if message.author == bot.user:
        return

    def check(m):
        return m.channel == message.channel

    dm = await bot.fetch_user(int(config["discord_id"]))

    if message.content.__contains__(config["twitch_username"]):
        if config["notify_matches"] == True:
                await dm.send(f"Your amiibo just got a match! \n{message.content}", embeds=[message.embeds[0], message.embeds[1]])

        headers = get_headers_from_key(config["api_key"])


        await bot.wait_for("message", check=check)

        amiibo_data = get_amiibo_data(config["to_watch"], headers)

        if config["notify_matches"] == True:
            id = get_last_match(config["amiibots_user_id"], headers)

            last_match_data = get_amiibo_data(id, headers)
            await dm.send(f"Your amiibo's rating after the match is {round(last_match_data['rating'], 2)}")

        if message.content.__contains__(amiibo_data["name"]):

            if config["type"] == "rating_cap":
                if amiibo_data["rating"] >= float(config["max_rating"]):
                    payload = {"match_selection_status": "INACTIVE"}
                    set_amiibo_data(config["to_watch"], headers, payload)
                    await dm.send(f"Your amiibo, {amiibo_data['name']} has reached the rating goal and has been set to inactive. \nUse `!setamiibo <id>` to set a new amiibo!")

            if config["type"] == "match_cap":
                if amiibo_data["total_matches"] >= config["max_matches"]:
                    payload = {"match_selection_status": "STANDBY"}
                    set_amiibo_data(config["to_watch"], headers, payload)
                    await dm.send(f"Your amiibo, {amiibo_data['name']} has reached the required match amount and has been set to standby. \nUse `!setamiibo <id>` to set a new amiibo!")


@bot.command(name = "getamiiboid")
async def getamiiboid(ctx: commands.Context, *, name: str):
    rulesets = {
      "44748ebb-e2f3-4157-90ec-029e26087ad0": "vanilla",
      "328d8932-456f-4219-9fa4-c4bafdb55776": "spirits: big 5 ban",
      "af1df0cd-3251-4b44-ba04-d48de5b73f8b": "spirits: anything goes"
    }

    config = parse_config()

    headers = get_headers_from_key(config["api_key"])

    amiibo = get_all_user_amiibo(config["amiibots_user_id"], headers)

    output = ""
    for amiibo in amiibo:
        if amiibo['name'] == name:
            output += f"{amiibo['name']} | {amiibo['id']} | {rulesets[amiibo['ruleset_id']]}\n"
    await ctx.send(output)

@bot.command(name="currentamiibostats")
async def getcurrentamiibostats(ctx: commands.Context):
    config = parse_config()

    headers = get_headers_from_key(config["api_key"])

    amiibo = get_amiibo_data(config["to_watch"], headers)

    amiibo_win_percent = float(amiibo["win_percentage"]) * 100

    await ctx.send(
        f'Name: {amiibo["name"]} \nRating: {round(amiibo["rating"], 2)} \nWin Rate: {amiibo_win_percent}% \nWins: {int(amiibo["wins"])} \nLosses: {int(amiibo["losses"])} \nTotal Matches: {int(amiibo["total_matches"])}'
    )

@bot.command(name="setamiibo")
async def set_amiibo(ctx: commands.Context, id: str):
    config = parse_config()

    headers = get_headers_from_key(config["api_key"])

    try:
        get_amiibo_data(id, headers)
    except:
        ctx.send("Invalid ID!")

    config["to_watch"] = id

    payload = {"match_selection_status": "ACTIVE"}

    set_amiibo_data(id, headers, payload)

    with open("./config.json", "w+") as cfg:
        json.dump(config, cfg, indent=2)

@bot.command(name="settype")
async def set_type(ctx: commands.Context, type: str):
    config = parse_config()

    def check(m):
            return m.channel == ctx.channel and m.author != bot.user

    if type == "rating_cap":
        await ctx.send("What would you like the rating cap to be?")

        rating: nextcord.Message = await bot.wait_for("message", check=check)

        config["type"] = type

        config["max_rating"] = float(rating.content)

    if type == "match_cap":
        await ctx.send("What would you like the maximum amount of matches to be?")

        matches: nextcord.Message = await bot.wait_for("message", check=check)

        config["type"] = type

        config["max_matches"] = int(matches.content)

    with open("./config.json", "w+") as cfg:
        json.dump(config, cfg, indent=2)


async def start_bot():
    if not os.path.isfile("./config.json"):
        config = {}

        config["discord_id"] = int(input("Please put in your Discord ID.\n"))

        config["amiibots_user_id"] = input("Please input your amiibots user ID.\n")

        config["twitch_username"] = input("Please put in your Twitch username.\n")

        config["shoutbox_id"] = int(input("Please input the ID of the channel to watch for matches. \n"))

        config["api_key"] = input("Please input your amiibots api key.\n")

        config["type"] = input("Please input how you want to set the amiibo.\n")

        if config["type"] == "rating_cap":
            config["max_rating"] = float(input("Please input the rating you would like your amiibo to turn off at.\n"))

        elif config["type"] == "match_cap":
            config["max_matches"] = int(input("Please input the amount of matches you would like your amiibo to be turned off at.\n"))

        config["to_watch"] = input("Please input the ID of the amiibo to watch.\n")

        config["notify_matches"] = bool(input("Would you like to be notified for your amiibo's games?\nSend `True` if so, or `False` otherwise.\n"))

        config["bot_token"] = input("Please input the bot's token.\n")

        with open("./config.json", "w+") as cfg:
            json.dump(config, cfg, indent=2)

    config = parse_config()
    await bot.start(config["bot_token"])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
