import asyncio
import datetime
import csv
import os
import random
from tqdm import tqdm
from colorama import init, Fore, Style
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import (
    UserStatusRecently, UserStatusLastWeek, UserStatusLastMonth,
    UserStatusOffline, SendMessageTypingAction, ChannelParticipantsSearch
)
from telethon.tl.functions.channels import GetParticipantsRequest, JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, SetTypingRequest

# ==== INIT ====
init(autoreset=True)

# ==== CONFIG ====
API_ID = 27679359
API_HASH = '719d7eaf21354f560ac5b932d6d98c14'
SESSION_NAME = 'scraper_session'
INVITE_LINK = "https://t.me/+yKqwd7-D1xM5NTQ1"  # Your channel invite link
CSV_FILE = 'scraped_users.csv'
OUTPUT_FILE = 'invited_users.txt'
MAX_DAYS_INACTIVE = 7
RATE_LIMIT_RANGE = (70, 120)  # Random delay between messages (in seconds)

INVITE_MESSAGES = [
    "Hey {name}, check this out! {link}",
    "Hi {name}, I think you might like this: {link}",
    "Hey there {name}! Join us here: {link}",
    "Yo {name}, don’t miss this! {link}",
    "Hey! Thought you’d enjoy this: {link}",
    "Hello {name}, you’re invited to something cool! {link}",
    "What’s up {name}? Here’s something for you: {link}",
    "Hey {name}, we’d love to have you: {link}",
    "Hi {name}! Come join our channel: {link}",
    "{name}, this might interest you: {link}"
]

def is_user_active(user, max_days=7):
    status = getattr(user, 'status', None)
    if isinstance(status, UserStatusRecently):
        return True
    elif isinstance(status, UserStatusLastWeek):
        return max_days >= 7
    elif isinstance(status, UserStatusLastMonth):
        return max_days >= 30
    elif isinstance(status, UserStatusOffline):
        last_seen = status.was_online.replace(tzinfo=None)
        days_ago = (datetime.datetime.utcnow() - last_seen).days
        return days_ago <= max_days
    return False

async def simulate_typing(client, user, message):
    await client(SetTypingRequest(peer=user, action=SendMessageTypingAction()))
    await asyncio.sleep(min(5, len(message) / 15))

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    print(Fore.CYAN + "[✓] Logged in as user.")

    group_input = input(Fore.BLUE + "🔗 Enter @group username or full invite link: ").strip()
    entity = await client.get_entity(group_input)
    participants = await client(GetParticipantsRequest(
        channel=entity,
        filter=ChannelParticipantsSearch(''),
        offset=0,
        limit=200,
        hash=0
    ))

    usernames = [u.username for u in participants.users if u.username]

    success, skipped = 0, 0

    with open(OUTPUT_FILE, 'a', encoding='utf-8') as outfile:
        for username in tqdm(usernames, desc="Inviting", colour='MAGENTA'):
            try:
                user = await client.get_entity(username)
                if not is_user_active(user, MAX_DAYS_INACTIVE):
                    print(Fore.YELLOW + f"[-] Skipped inactive: @{username}")
                    skipped += 1
                    continue

                message = random.choice(INVITE_MESSAGES).format(
                    name=getattr(user, 'first_name', username),
                    link=INVITE_LINK
                )

                try:
                    await simulate_typing(client, user, message)
                    await client.send_message(user, message)
                    print(Fore.GREEN + f"[+] Invited: @{username}")
                    outfile.write(f"@{username}\n")
                    success += 1
                    await asyncio.sleep(random.randint(*RATE_LIMIT_RANGE))

                except FloodWaitError as f:
                    print(Fore.RED + f"[!] Flood wait triggered. Sleeping for {f.seconds} seconds.")
                    await asyncio.sleep(f.seconds)
                    continue

                except Exception as e:
                    print(Fore.RED + f"[x] Failed @{username}: {e}")
                    skipped += 1
                    continue

            except Exception as e:
                print(Fore.RED + f"[x] Failed to process @{username}: {e}")
                skipped += 1

    print(Style.BRIGHT + Fore.MAGENTA + f"\n✨ Summary: Sent: {success} | Skipped: {skipped}")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
