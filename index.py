import gkeepapi
import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")
GOOGLE_LIST_ID = os.getenv("GOOGLE_LIST_ID")

# =================== KEEP ===================
keep = gkeepapi.Keep()
success = keep.login(GOOGLE_EMAIL, GOOGLE_APP_PASSWORD)
keep.sync()

glist = keep.get(GOOGLE_LIST_ID)
items = glist.unchecked

# =================== BRING (+ delete keep_items) ===================

BRING_URL = "https://api.getbring.com/rest/v2"
BRING_LIST_ID = os.getenv("BRING_LIST_ID")
BRING_EMAIL = os.getenv("BRING_EMAIL")
BRING_PASSWORD = os.getenv("BRING_PASSWORD")

BRING_HEADERS = {
    "X-BRING-API-KEY": "cof4Nc6D8saplXjE3h3HXqHH8m7VU2i1Gs0g85Sp",
    "X-BRING-CLIENT": "webApp",
    "X-BRING-CLIENT-SOURCE": "webApp",
    "X-BRING-COUNTRY": "FR",
}

BRING_PUT_CONTENT_TYPE = "application/x-www-form-urlencoded; charset=UTF-8"

auth_res = requests.post(
    f"{BRING_URL}/bringauth",
    headers=BRING_HEADERS,
    data={
        "email": BRING_EMAIL,
        "password": BRING_PASSWORD,
    }
)
auth_res.raise_for_status()
auth_res = auth_res.json()

bring_user_uuid = auth_res.get("uuid")
bring_access_token = auth_res.get("access_token")


for item in items:
    print(item)
    if item:  # removes ""
        add_item_res = requests.put(
            f"{BRING_URL}/bringlists/{BRING_LIST_ID}",
            headers={
                **BRING_HEADERS,
                "Content-Type": BRING_PUT_CONTENT_TYPE,
                "Authorization": f"Bearer {bring_access_token}" 
            },
            data=f"&purchase={urllib.parse.quote(item._text)}&recently=&remove=&sender=null"
        )
        add_item_res.raise_for_status()
    item.delete()

keep.sync()
