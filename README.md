### pingmii
![logo](https://cdn.discordapp.com/attachments/881840554340679720/886729364329336832/pingmii_icon_png.png)

pingmii is a Discord Bot for detecting when an amiibots amiibo is at a specified amount of games and disabling it.

## How to use
Make sure you have [python3](https://www.python.org) and pip installed

Replace the sample values in the `sampleenv.env` with the proper values (Note: ENABLE-AMIIBO-ID is not required)

What the values in the `sampleenv.env` mean:

`BOT-TOKEN`: The token for the Discord bot you will be using

`DISABLE-AMIIBO-ID`: The ID of the amiibo you want to disable at the specified amount of games

`ENABLE-AMIIBO-ID`: The ID of the amiibo you want to enable one the disable amiibo finishes

`AMIIBOTS-API-KEY`: Your API key for amiibots, Contact untitled1991#9405 on Discord to get one

`USER-ID`: Your 18 digit Discord userid

`TWITCH-USER`: Your Twitch username

`PING-CHANNEL-ID`: The channel id of the channel you want to use to get pinged when your amiibo finish

`SHOUTBOX-ID`: The channel id of the shoutbox used to detect games

Ping `jozz#1961` in the disord for help on getting the amiibo's id

Once you fill out all of those values, rename the file to `.env` with nothing before the file ending

At this point you should have pip installed, so open up a command prompt in the folder and type in `pip install -r requirements.txt`

When the requirements finish installing, type `py main.py` in the command prompt

## Discord
Join the [amiibots Discord](https://discord.gg/2v6pcw3zzg/) for support/requests.

## Credits
untitled1991 for doing code review & helping fix bugs, etc.

Orchid for being an early tester to help verify it's working state, and for the logo.