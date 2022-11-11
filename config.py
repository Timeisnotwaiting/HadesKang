from os import envrion as e

BOT_TOKEN = e["BOT_TOKEN"]

SUDOS = e["SUDO_USERS"].split()

x = []

for y in SUDOS:
    x.append(int(y))

SUDO_USERS = x
