import json
import hashlib
import asyncio
import time
from pyrogram import Client, filters
import re

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)

bot = Client("core", api_id=config["api_id"], api_hash=config["api_hash"], bot_token=config["bot_token"])
ledger_channel = config.get("ledger_channel")
blocksize = 30
blocks_per_batch = 5000
inscription_batch = []
batch_lock = asyncio.Lock()
current_block_number = 1
previous_hash = "0" * 40

# Load state from file
def load_state():
    try:
        with open("state.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"current_block_number": 1, "previous_hash": "0" * 40}

# Save state to file
def save_state(block_number, prev_hash):
    with open("state.json", "w") as file:
        json.dump({"current_block_number": block_number, "previous_hash": prev_hash}, file)

# Load initial state
state = load_state()
current_block_number = state["current_block_number"]
previous_hash = state["previous_hash"]

# Generate hash for a block
def generate_hash(data, prev_hash):
    combined_data = prev_hash + data
    return hashlib.sha1(combined_data.encode()).hexdigest()

# Get the next block number
def get_next_block_number():
    global current_block_number
    block_number = current_block_number
    current_block_number += 1
    return block_number

# Store a batch in the ledger
async def store_batch_in_ledger(batch, hash, block_number, timestamp):
    global previous_hash
    batch_number = (block_number - 1) // blocks_per_batch + 1
    ledger_filename = f"ledger_{batch_number}.json"
    ledger_entry = {
        "hash": hash,
        "timestamp": timestamp,  # Add the timestamp here
        f"block {block_number}": batch
    }
    try:
        ledger = []
        try:
            with open(ledger_filename, "r") as file:
                ledger = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        ledger.append(ledger_entry)
        with open(ledger_filename, "w") as file:
            json.dump(ledger, file, indent=4)

        # Removed the file hash calculation and related logic
        if len(ledger) == blocks_per_batch:
            save_state(current_block_number, previous_hash)
            await upload_ledger_file(ledger_filename)
    except Exception as e:
        print(f"Error while storing/updating ledger file: {e}")

# Upload ledger file
async def upload_ledger_file(filename):
    max_retries = 20
    retry_delay = 10

    for attempt in range(max_retries):
        try:
            await bot.send_document(ledger_channel, filename)
            print(f"File {filename} uploaded successfully.")
            break
        except Exception as e:
            print(f"Failed to upload ledger file on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                print(f"Failed to upload ledger file after {max_retries} attempts.")

def is_valid_json(client, update, message):
    try:
        json_part = message.text
        byte_length = len(json_part.encode('utf-8'))
        if byte_length <= 96:
            json.loads(json_part)
            return True
    except (json.JSONDecodeError, TypeError):
        pass
    return False

@bot.on_message(filters.create(is_valid_json))
async def handle_json_message(bot, message):
    global inscription_batch
    async with batch_lock:
        json_data = json.loads(message.text)

        # Add to the batch
        inscription_batch.append({"user": message.from_user.id, "data": json_data})

        if len(inscription_batch) >= blocksize:
            await process_batch()

# Process a batch of inscriptions
async def process_batch():
    global inscription_batch, previous_hash, current_block_number
    block_number = get_next_block_number()
    timestamp = int(time.time())  # Timestamp is generated here

    batch_text = '\n'.join([f"User: {item['user']}\nData: {item['data']}\n" for item in inscription_batch])
    
    block_data = f"Block: {block_number}\nTimestamp: {timestamp}\nData:\n{batch_text}"
    hash = generate_hash(block_data, previous_hash)
    previous_hash = hash
    save_state(current_block_number, previous_hash)

    # Pass the timestamp to the store_batch_in_ledger function
    await store_batch_in_ledger(inscription_batch, hash, block_number, timestamp)

    if ledger_channel:
        try:
            formatted_batch_text = '\n'.join([f"User: {item['user']}\nData: {json.dumps(item['data'])}\n" for item in inscription_batch])
            ledger_message = f"Block: {block_number}\nTimestamp: {timestamp}\nHash: {hash}\n\n{formatted_batch_text}"
            await bot.send_message(ledger_channel, ledger_message)
        except Exception as e:
            print(f"Failed to send batch to ledger channel: {e}")

    inscription_batch = []

# Run the bot
bot.run()