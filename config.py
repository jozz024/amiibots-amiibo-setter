import os
import requests
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["BOT-TOKEN"]
DISABLEAMIIBOID = os.environ["DISABLE-AMIIBO-ID"]
ENABLEAMIIBOID = os.environ.get("ENABLE-AMIIBO-ID", None)
APIKEY = os.environ["AMIIBOTS-API-KEY"]
USERID = os.environ["USER-ID"]
USER = os.environ["TWITCH-USERNAME"]
PINGCHANNEL = int(os.environ["PING-CHANNEL-ID"])
SHOUTBOXID = int(os.environ["SHOUTBOX-ID"])
RATING_OR_MATCHES = os.environ.get("RATING-OR-MATCHES", None)
BASE_URL = "https://www.amiibots.com/api/amiibo/"
OLD_AMIIBO_URL = BASE_URL + DISABLEAMIIBOID
NEW_AMIIBO_URL = BASE_URL + ENABLEAMIIBOID
if "Bearer" in APIKEY:
    HEADERS = {"Authorization": APIKEY}
else:
    HEADERS = {"Authorization": f"Bearer {APIKEY}"}
MATCH_TURN_OFF_NUMBERS = [30, 50, 100, 150]
amiiboname = requests.get(OLD_AMIIBO_URL, headers=HEADERS).json()["data"]["name"]
amiiboname_2 = requests.get(NEW_AMIIBO_URL, headers=HEADERS).json()["data"]["name"]

bot = commands.Bot(command_prefix="!", description="")

CHARACTER_NAME_TO_ID_MAPPING = {
    "mario": "bcfaf3a7-049c-478f-901f-31ac873260f3",
    "bowser": "0b325755-b138-4dd6-bbc8-c9604ed0f90c",
    "sheik": "0be3828e-571c-44dc-9fc4-cf947b60aad5",
    "olimar": "11d7c49d-8677-4f87-876b-6db94fae00ef",
    "ridley": "1874d724-bd91-43ab-91ae-a8b4a740b951",
    "snake": "1aedb3f5-e352-4ebf-b701-7502bbf62366",
    "pichu": "21c5ccdd-d157-42bb-92ac-b99fd07dd247",
    "corrin": "25543733-526a-4d7e-ba50-081597cf28d3",
    "palutena": "279e8c96-d915-480d-acbe-98306c958a19",
    "dr. mario": "28afc91e-bdfd-45c6-83e9-ff0e9ad52938",
    "incineroar": "2cf4a409-b186-43a9-948f-175abbef3426",
    "lucas": "3527fd64-64e0-4793-806e-a3656553c7ab",
    "koopaling": "363d4b63-ba5a-4685-8762-dff02b28266c",
    "wolf": "39f4f717-151a-4cb0-b672-7a66ba3c5274",
    "wario": "3a80cdac-93bb-4a75-8e38-f69f37d10ec6",
    "piranha plant": "3b44eedd-131c-4131-89a1-2f8bc4867e89",
    "lucina": "3c6e1beb-0d2a-4387-adad-fa833bf6e3fd",
    "meta knight": "3e8519a2-faa6-4bcc-98b9-bff3ac95b504",
    "ryu": "42f53983-2889-4f04-9b2f-d2d7b4ef1823",
    "ice climbers": "47c5c078-6112-48ad-9e29-18c6e1077a81",
    "peach": "4baddb51-1a48-481b-9c29-332c0f0fa5cb",
    "zelda": "4c8513b8-a7c7-42f4-a4d4-55f5415d92fb",
    "little mac": "4d6019ea-9540-4dfe-a6d9-56caa35e7047",
    "greninja": "4dcbb633-58b0-481a-9d6a-c350b2c08640",
    "ganondorf": "518596af-acc8-4205-b24e-db8f8a953756",
    "pikachu": "592fb00b-2943-47de-973a-3a4a5ca56e6a",
    "pac-man": "599edd14-687c-4264-812e-bc246f562f31",
    "terry": "5a6be0b7-a734-4507-8999-65130e56e292",
    "bayonetta": "5c63c8cc-6afa-4bd5-ad30-815856cb845d",
    "mega man": "5d06d81c-dad5-414b-9e6d-d8c0adeda607",
    "yoshi": "5d4c8535-fc65-4ebd-9c13-4a96ecd3e94d",
    "rob": "6537aebc-7b92-4b1c-94ca-50ab350a7c46",
    "dark samus": "65b431e9-84ec-4b85-8a5c-a225e9d40934",
    "pokemon trainer": "66d89a85-3323-444c-907d-67f7d130c6e6",
    "daisy": "6998259f-982b-47ee-90ea-c1dae66fca5a",
    "mii gunner": "6a728c16-df81-4513-9896-3222fbce4ea1",
    "chrom": "6be7e121-5b65-405f-9905-6a9279ab199d",
    "shulk": "6ed721a9-e20a-4d69-8d4f-567ba13cbb29",
    "duck hunt": "759f3e11-0708-4cec-8fcd-f0374ab6aeeb",
    "jigglypuff": "7a8f391b-e3ca-4c47-8ecb-d7eaa3d605aa",
    "zero suit samus": "7b2f87a9-4631-42d0-9f4a-86a1c3ac4465",
    "dark pit": "7b423052-3d6a-49a7-805b-f4e818792a5c",
    "richter": "7bf8c562-4dc3-44ce-80ec-cc66f0bb8ff7",
    "pit": "7c869bdb-0101-4aa7-9ea8-82f1d7420928",
    "robin": "7eb55c9b-4109-4064-a643-cdc809672d7c",
    "king krool": "7f5de07d-9c82-45fb-adae-73c8a2b811e3",
    "falco": "81bb935e-51ad-4a35-92e6-9d7565bed6a9",
    "inkling": "85c1dc46-460c-453e-ba7a-123ba8e19128",
    "mii brawler": "8bae1c7b-a783-45ee-a246-1ab9507080ba",
    "byleth": "8df1cca7-8810-425b-8f6a-0e65a8eda7a3",
    "game & watch": "96b8056f-9f5d-4908-8acf-34353db33d74",
    "roy": "96e48494-946f-4280-a419-488d644135e0",
    "donkey kong": "9e7024ec-4a72-4887-bdad-4adbb9b0e3a9",
    "link": "9f3caa1b-1dbd-49da-b3fd-28dfadd18828",
    "captain falcon": "b2e680f3-0c62-4387-a4ac-b539d85e90c0",
    "falcon": "b2e680f3-0c62-4387-a4ac-b539d85e90c0",
    "ike": "b89763e0-222e-472b-a5f8-2de3dba550a7",
    "villager": "ba94257a-9223-4210-a542-ffd8a798d74c",
    "diddy kong": "be1fbfb9-9555-42bb-9e77-7aa2f82c5ded",
    "ken": "bf83ce13-5c43-462b-8baa-c7d1336508ba",
    "king dedede": "c0cb713e-e431-4ebe-9dec-dd63bfd2b807",
    "kirby": "c3a30ee3-52a5-4380-bf5f-a5514890a55f",
    "samus": "c54fd324-6f7a-46a0-9353-29f80abb8c45",
    "fox": "cc43dc32-d6fd-43eb-be16-47c498521272",
    "marth": "d0d93ac1-1681-41df-baa3-7e3968103432",
    "ness": "d2d68453-454c-41a2-bf12-7b001d4c8f41",
    "sonic": "d444e8eb-0140-4e51-9203-b374d9a4431d",
    "young link": "d65e8fc2-a593-4fef-bead-408a967fbb1e",
    "cloud": "d86a3a2b-363d-4fcd-94da-fa7122e9b626",
    "hero": "da0c84d7-9c43-4e74-92e7-113194694b25",
    "luigi": "da7df432-47e4-4cbe-9b29-1c7958197105",
    "rosalina & luma": "e2531ffe-e834-49ae-b233-56386472a6ed",
    "mii swordfighter": "e3891498-94f6-4ccc-a527-c5f4e26051d1",
    "wii fit trainer": "e6f9ab43-8434-48bb-a765-ebbb97f66fae",
    "joker": "e7d9e195-f86e-4ac8-8bd2-7302889147eb",
    "lucario": "e9128698-7812-4636-9074-127f1983bf1b",
    "toon link": "eea3bb5b-564a-46c4-9c4c-8cef6e59c8b1",
    "isabelle": "f40fdcb7-a785-4681-8c04-c66cc84edcac",
    "simon": "fa1ac3ba-0880-483b-b94e-9b4952e3f999",
    "mewtwo": "fd264bc3-a141-400f-9e55-adabc783322d",
    "banjo & kazooie": "fe995f08-d261-47ba-ac69-81bbd272f8ce",
}