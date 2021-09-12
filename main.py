import os
import requests
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['BOT-TOKEN']
AMIIBOID = os.environ['AMIIBO-ID']
APIKEY = os.environ['AMIIBOTS-API-KEY']
USERID = os.environ['USERID']
USER = os.environ['USERNAME']
PINGCHANNEL = int(os.environ['PINGCHANNEL'])
SHOUTBOXID = int(os.environ['SHOUTBOXID'])

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        activity = discord.Game(
            name=f'Pinging {USER} when their amiibo finish their amiibots run!')
        await client.change_presence(status=discord.Status.idle, activity=activity)
    url = f'https://www.amiibots.com/api/amiibo/{AMIIBOID}'
    headers = {'Authorization': APIKEY}
    amiibodata = requests.get(url, headers=headers)
    match_turn_off_numbers = [29, 49, 99, 149]
    amiibo = amiibodata.json()['data']
    async def on_message(self, message):
        if message.author == client.user:
            return
        if USERID in message.content and message.channel.id == SHOUTBOXID:
            if MyClient.amiibo['total_matches'] in MyClient.match_turn_off_numbers:
                url = f'https://www.amiibots.com/api/amiibo/{AMIIBOID}'
                headers = {'Authorization': APIKEY}
                payload = {'is_active': False}
                response = requests.put(url, headers=headers, json = payload)
                message_send_channel = client.get_channel(PINGCHANNEL)
                await message_send_channel.send(
                    f"<@{USERID}> Your amiibo, {MyClient.amiibo['name']}, finished its run with {MyClient.amiibo['total_matches'] + 1} matches!"
                )

client = MyClient()
client.run(TOKEN)
