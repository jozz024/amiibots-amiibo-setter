import os
import requests
import discord
import keep_alive
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']
AMIIBOID = os.environ['AMIIBO-ID']
APIKEY = os.environ['AMIIBOTS-API-KEY']
USERID = os.environ['USERID']
USER = os.environ['USERNAME']
PINGCHANNEL = os.environ['PINGCHANNEL']

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        activity = discord.Game(
            name=f'Pinging {USER} when their amiibo finish their amiibots run!')
        await client.change_presence(status=discord.Status.idle,
                                     activity=activity)

    async def on_message(self, message):
        if USER in message.content:
            message_send_channel = client.get_channel(PINGCHANNEL)
            url = f'https://www.amiibots.com/api/amiibo/{AMIIBOID}'
            headers = {'Authorization': APIKEY}
            payload = {'is_active': False}
            response = requests.put(url, headers=headers, json=payload)
            response1 = requests.get(url, headers=headers)
            match_turn_off_numbers = [29, 40, 49, 99, 149]
            amiibo = response1.json()['data']
            if amiibo['total_matches'] in match_turn_off_numbers:
                print(message_send_channel)
                await message_send_channel.send(
                    f"<@{USERID}> Your amiibo, {amiibo['name']}, finished its run with {amiibo['total_matches'] + 1} matches!\n {response.json} "
                )


keep_alive.keep_alive()
client = MyClient()
client.run(TOKEN)
