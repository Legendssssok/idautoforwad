from pyrogram import Client, filters
from pyrogram.types import Message
import os
from pyrogram.types import InputMediaPhoto


import random

API_ID = 11573285
API_HASH = "f2cc3fdc32197c8fbaae9d0bf69d2033"

BOT_TOKEN = "5311900774:AAGjyqQ6JfjP5y2W-PD95txGoJ_e2Dsjugo"

STRING = "BQAXMZ75eY_gHEijakYvTGyS7Ai453JLMgc7czW6cXQzlAw6wq1k14_CCYFIlkwHKlBfBkDoJCBYaD5hKbZv9KKh60AfjGAbliNeTix-PKmsJM4FscyNWbfwzCcEYO7qJCwYRwCdb-AobNbgNjAbwwY_wE2szfUdUUn9qYH1a7oCBEwA3hH-l8WuuBHneytGNJQ3gVIJcQMLbJHXmMgyvMy_T5NxuiWysXNN5KspoDbjIw_sG7X2Y2yxio47kFzKrj8AkQdnIaV64ekFPBkrAibgAa-6UEHspdmsLOh4xTJnOJW-HbPZ5rdk_SeihY3JMBO9nIGr1cetL5l4zjrav9dSAAAAATMiPY8A"


app = Client(name="Mousa", api_id=API_ID, api_hash=API_HASH,
             bot_token=BOT_TOKEN, session_string=STRING)

# Source and target channel IDs
source_channel_id = -1001802779833
target_channel_id = -1001746279641

# Store id for update
store_id = {}

# Whitelist and blacklist
whitelist_words = ["gl", "vc", "c", "@mousa11prime_leaker", "dream11", "pick"]
blacklist_words = ["t.me/mousaprimeleaks",
                   "t.me/+ekRbqpexagE3MGE9", "@Auto_Forward_Messages_Bot", "schedule", "coming", "wickets", "Upcoming" , "Cleansweep" ,"@Mousaprimes"]

auto_forwarding = True


@app.on_message(filters.command(["start"], ".") & filters.me)
async def start(client: Client, message: Message):
    ex = await message.edit_text("Processing...")
    await ex.edit("Hello i am online.")


@app.on_message(filters.command(["autoforward"], ".") & filters.me)
async def start(client: Client, message: Message):
    global auto_forwarding
    ex = await message.edit_text("Processing...")
    command = message.text.split()[1]
    if command == 'start':
        if not auto_forwarding:
            # Start auto-forwarding logic here
            auto_forwarding = True
            await ex.edit('Auto-forwarding started.')
        else:
            await ex.edit('Auto-forwarding is already started.')
    elif command == 'stop':
        if auto_forwarding:
            # Stop auto-forwarding logic here
            auto_forwarding = False
            await ex.edit('Auto-forwarding stopped.')
        else:
            await ex.edit('Auto-forwarding is already stopped.')


@app.on_message(filters.chat(source_channel_id) & filters.text)
def forward_text(client, message):
    global auto_forwarding
    # Check if the message contains any whitelisted or blacklisted words
    text = message.text.lower()
    if any(word in text for word in blacklist_words):
        return
    if not any(word in text for word in whitelist_words):
        return
    if not auto_forwarding:
        return
    # Send the text message to target channel
    try:
        forwarded_message = client.send_message(
            target_channel_id, message.text + "\n\n➡️ Mousa FinaL \n\n➡️ Join Channel : @Mousa11Prime_Leaker\n➡️ Link : https://t.me/Mousa11Prime_Leaker", disable_web_page_preview=True)
        store_id[message.id] = forwarded_message.id
    except Exception as e:
        print(f"Failed to forward text message: {e}")


@app.on_message(filters.chat(source_channel_id) & filters.photo)
def forward_photo(client, message):
    # Send the photo message to target channel.
    if not auto_forwarding:
        return
    file_id = client.download_media(message)
    try:
        forwarded_message = client.send_photo(
            target_channel_id, file_id, caption="\n\n➡️ Mousa FinaL \n\n➡️ Join Channel : @Mousa11Prime_Leaker\n➡️ Link : https://t.me/Mousa11Prime_Leaker")
        store_id[message.id] = forwarded_message.id
    except Exception as e:
        print(f"Failed to forward photo message: {e}")
    os.remove(file_id)

@app.on_edited_message(filters.chat(source_channel_id) & filters.text)
# Check if the message contains any whitelisted or blacklisted words
def update_text(client, message):
    text = message.text.lower()
    if any(word in text for word in blacklist_words):
        return
    if not any(word in text for word in whitelist_words):
        return
    if not auto_forwarding:
        return
    # Update the edited text message in target channel
    message_id = store_id.get(message.id)
    try:
        client.edit_message_text(target_channel_id, message_id, message.text +
                                 "\n\n➡️ Mousa FinaL \n\n➡️ Join Channel : @Mousa11Prime_Leaker\n➡️ Link : https://t.me/Mousa11Prime_Leaker", disable_web_page_preview=True)
    except Exception as e:
        print(f"Failed to update text message: {e}")


@app.on_edited_message(filters.chat(source_channel_id) & filters.photo)
def update_photo(client, message):
    # Update the edited photo message in target channel
    if not auto_forwarding:
        return
    print("Updating Photo")
    file_id = client.download_media(message)
    message_id = store_id.get(message.id)
    try:
        client.edit_message_media(
            target_channel_id, message_id, InputMediaPhoto(file_id))
    except Exception as e:
        print(f"Failed to update photo message: {e}")
    os.remove(file_id)


print("started")
app.run()
