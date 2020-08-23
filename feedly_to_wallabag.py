#!/usr/bin/env python3

import requests
import webbrowser
import json
import sys

from env import *

def err_on_status_code(request, msg):
    if request.status_code != 200:
        print(f"{msg} : {r.status_code} - {r.text}")
        sys.exit(1)

headers = {
    "Authorization": f"Bearer {FEEDLY_ACCESS_TOKEN}",
    "Content-Type": "application/json",
    "X-Accept": "application/json",
}

# 1 - get user id
r = requests.get(f"{FEEDLY_URL}/profile", headers=headers)

err_on_status_code(r, "[feedly] error while getting user_id")

FEEDLY_USER_ID = r.json()['id']
print(f"[feedly] user_id = {FEEDLY_USER_ID}")

# 3 - get all saved for later items

r = requests.get(f"{FEEDLY_URL}/streams/contents?streamId=user/{FEEDLY_USER_ID}/tag/global.saved&count=10000&ranked=oldest", headers=headers)

err_on_status_code(r, "[feedly] error while getting all saved for later items")

saved_later_items = r.json()['items']

# 4 - wallabag oAuth - get access token
headers = {
    "X-Accept": "application/json",
}
payload = {
    "grant_type": "password",
    "client_id": WALLABAG_CLIENT_ID,
    "client_secret": WALLABAG_CLIENT_SECRET,
    "username": WALLABAG_USERNAME,
    "password": WALLABAG_PASSWORD
}
r = requests.post(f"{WALLABAG_URL}/oauth/v2/token", data=payload, headers=headers)

err_on_status_code(r, "[wallabag] error while getting access token")

WALLABAG_ACCESS_TOKEN=r.json()['access_token']
print(f"[wallabag] access_token = {WALLABAG_ACCESS_TOKEN}")

# 5 - import urls in wallabag
# the API to import a list of urls seems buggy, I dont know why, so we'll import one by one
# https://app.wallabag.it/api/doc#post--api-entries-lists.{_format}
headers = {
    "X-Accept": "application/json",
    "Authorization": f"Bearer {WALLABAG_ACCESS_TOKEN}"
}
# TODO make it faster (concurrency, threads, asyncio, futures, gevent ...)
for index, item in enumerate(saved_later_items):
    url = item['alternate'][0]['href']
    payload = {
        "url": url,
        "origin_url": item['originId'],
        "tags": "feedly",
    }
    r = requests.post(f"{WALLABAG_URL}/api/entries.json", data=payload, headers=headers)

    if r.status_code != 200:
        print(f"[wallabag] error while importing {index+1}/{len(saved_later_items)} {url} : {r.status_code} - {r.text}")
    else :
        print(f"[wallabag] success importing {index+1}/{len(saved_later_items)} : {url}")

print("done :) gg! your pocket items were successfully migrated to wallabag")