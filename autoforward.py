from pyrogram import Client, filters
from pyrogram.types import Message
import os
from pyrogram.types import InputMediaPhoto


import random

API_ID = 11573285
API_HASH = "f2cc3fdc32197c8fbaae9d0bf69d2033"

BOT_TOKEN = "5311900774:AAGjyqQ6JfjP5y2W-PD95txGoJ_e2Dsjugo"

STRING = "BQCbwq2Pl0pKidq3IcAyK3XVGQyXsPVTkZtUJ17QCThvhchulcnohmEY8wTrNzB7hqMd3H8xh8mfyn8KXp8odBsj8e68Uk4MaqohPC3rLvKHK5qgEyYbAws6CgMOlYk57tLEIP_t9bTN6kjvdpcIlsKBDXf2BRaS68oqVks5iUU__fatXDRri61vSTENxV8BQ67oUtxpIOWICUR79hQr30vkMca0hrinJDPKL4SL5CFYXW3LPBo-iAWYM1vaYDLE6Rc4c3DyWxWbuTgc8jWm58b2uT9bVkyBnCbEuSPua-Gj9vCaFNtEzohjrNZGsB95tUgkIKEujo3IG6qj1B6yj4idAAAAATMiPY8A"


app = Client(name="Mousa", api_id=API_ID, api_hash=API_HASH,
             bot_token=BOT_TOKEN, session_string=STRING)

# Source and target channel IDs
source_channel_id = -1001802779833
target_channel_id = -1001746279641

# Store id for update
store_id = {}

# Whitelist and blacklist
whitelist_words = ["gl", "vc", "c", "@mousa11prime_leaker", "dream11"]
blacklist_words = ["https://t.me/mousaprimeleaks",
                   "https://t.me/+ekRbqpexagE3MGE9", "@Auto_Forward_Messages_Bot"]


@app.on_message(filters.command(["start"], ".") & filters.me)
async def start(client: Client, message: Message):
    ex = await message.edit_text("Processing...")
    await ex.edit("Hello i am online.")


@app.on_message(filters.chat(source_channel_id) & filters.text)
def forward_text(client, message):
    # Check if the message contains any whitelisted or blacklisted words
    text = message.text
    if any(word in text for word in blacklist_words):
        return
    if not any(word in text for word in whitelist_words):
        return
    # Send the text message to target channel
    try:
        forwarded_message = client.send_message(
            target_channel_id, message.text + "\n\n@Mousa11Prime_Leaker")
        store_id[message.id] = forwarded_message.id
    except Exception as e:
        print(f"Failed to forward text message: {e}")


@app.on_message(filters.chat(source_channel_id) & filters.photo)
def forward_photo(client, message):
    # Send the photo message to target channel.
    file_id = client.download_media(message)
    try:
        forwarded_message = client.send_photo(target_channel_id, file_id, caption="@Mousa11Prime_Leaker")
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
    # Update the edited text message in target channel
    message_id = store_id.get(message.id)
    try:
        client.edit_message_text(target_channel_id, message_id, message.text + "\n\n@Mousa11Prime_Leaker")
    except Exception as e:
        print(f"Failed to update text message: {e}")


@app.on_edited_message(filters.chat(source_channel_id) & filters.photo)
def update_photo(client, message):
    # Update the edited photo message in target channel
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
