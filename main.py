cd ~/nexus-userbot

# Обновляем requirements.txt
cat > requirements.txt << 'EOF'
telethon>=1.34.0
pyrogram>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0
EOF

# Устанавливаем
source venv/bin/activate
pip install -r requirements.txt

# Создаём новый main.py с поддержкой двух клиентов
cat > main.py << 'EOF'
#!/usr/bin/env python3
"""
NEXUS USERBOT - Hikka Style
Поддержка Telethon + Pyrogram
@nopxcket | @shitlame
"""

import asyncio
import sys
import time
import os
import platform
import json
from pathlib import Path

from telethon import TelegramClient as TelethonClient
from telethon import events as telethon_events
from pyrogram import Client as PyrogramClient
from pyrogram import filters as pyrogram_filters
from pyrogram.types import Message as PyrogramMessage

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
PREFIX = "."
SESSION_NAME = "nexus"
BOT_NAME = "NEXUS"
VERSION = "2.0.0"
OWNER_ID = 7909649275
GROUP_LINK = "https://t.me/userbotnexus"

BASE = Path(__file__).parent
PHOTOS_DIR = BASE / "photos"
PHOTOS_DIR.mkdir(exist_ok=True)

# Клиенты
telethon_client = None
pyrogram_client = None

cmds = {}
start = time.time()
current_prefix = PREFIX

def get_photo_bytes(photo_name):
    photo_path = PHOTOS_DIR / f"{photo_name}.jpg"
    if photo_path.exists():
        with open(photo_path, 'rb') as f:
            return f.read()
    return None

def get_uptime():
    u = time.time() - start
    days = int(u // 86400)
    hours = int((u % 86400) // 3600)
    minutes = int((u % 3600) // 60)
    return f"{days}d {hours}h {minutes}m"

def banner():
    print("\n" * 50)
    print("\033[95m  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗")
    print("  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝")
    print("  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗")
    print("  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║")
    print("  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║")
    print("  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝")
    print("\033[95m         NEXUS USERBOT {VERSION}")
    print("\033[95m         @nopxcket  |  @shitlame\033[0m")

# ==================== TELEGRAM COMMANDS (Telethon) ====================

async def ping_telethon(e, a):
    s = time.time()
    await e.edit("🏓 Pong...")
    await asyncio.sleep(0.05)
    await e.edit(f"🏓 Pong!\n📡 Ping: `{int((time.time()-s)*1000)} ms`")

async def info_telethon(e, a):
    user = await e.get_sender()
    username = f"@{user.username}" if user.username else user.first_name
    uptime = get_uptime()
    text = f"""
[👤] You: {username}
[🤖] Version: {VERSION}
[📷] Prefix: «{current_prefix}»
[🔄] Uptime: {uptime}
[💻] System: {platform.system()}
[🔗] [УСТАНОВИТЬ]({GROUP_LINK})"""
    photo_bytes = get_photo_bytes("info")
    if photo_bytes:
        await telethon_client.send_file(e.chat_id, photo_bytes, caption=text, parse_mode='markdown')
        await e.delete()
    else:
        await e.edit(text, parse_mode='markdown')

async def nexus_telethon(e, a):
    user = await e.get_sender()
    username = f"@{user.username}" if user.username else user.first_name
    text = f"""
[👑] Owner: @nopxcket & @shitlame
[👤] You: {username}
[🤖] NEXUS {VERSION}
[📷] Prefix: «{current_prefix}»
[🔗] [УСТАНОВИТЬ]({GROUP_LINK})"""
    photo_bytes = get_photo_bytes("nexus")
    if photo_bytes:
        await telethon_client.send_file(e.chat_id, photo_bytes, caption=text, parse_mode='markdown')
        await e.delete()
    else:
        await e.edit(text, parse_mode='markdown')

async def help_telethon(e, a):
    user = await e.get_sender()
    username = f"@{user.username}" if user.username else user.first_name
    text = f"""
[🤖] NEXUS USERBOT {VERSION}
[👑] Owner: {username}
[📌] COMMANDS:
[📷] `{current_prefix}info` → Bot information
[🏓] `{current_prefix}ping` → Check ping
[✨] `{current_prefix}nexus` → Photo with info
[⚙️] `{current_prefix}prefix` → Change prefix
[❓] `{current_prefix}help` → This menu"""
    photo_bytes = get_photo_bytes("help")
    if photo_bytes:
        await telethon_client.send_file(e.chat_id, photo_bytes, caption=text)
        await e.delete()
    else:
        await e.edit(text)

# ==================== PYROGRAM COMMANDS ====================

async def ping_pyrogram(client, message):
    s = time.time()
    msg = await message.reply("🏓 Pong...")
    await msg.edit(f"🏓 Pong!\n📡 Ping: `{int((time.time()-s)*1000)} ms`")

async def info_pyrogram(client, message):
    user = message.from_user
    username = f"@{user.username}" if user.username else user.first_name
    uptime = get_uptime()
    text = f"""
[👤] You: {username}
[🤖] Version: {VERSION}
[📷] Prefix: «{current_prefix}»
[🔄] Uptime: {uptime}
[💻] System: {platform.system()}
[🔗] [УСТАНОВИТЬ]({GROUP_LINK})"""
    photo_bytes = get_photo_bytes("info")
    if photo_bytes:
        await client.send_photo(message.chat.id, photo_bytes, caption=text)
        await message.delete()
    else:
        await message.edit(text)

async def nexus_pyrogram(client, message):
    user = message.from_user
    username = f"@{user.username}" if user.username else user.first_name
    text = f"""
[👑] Owner: @nopxcket & @shitlame
[👤] You: {username}
[🤖] NEXUS {VERSION}
[📷] Prefix: «{current_prefix}»
[🔗] [УСТАНОВИТЬ]({GROUP_LINK})"""
    photo_bytes = get_photo_bytes("nexus")
    if photo_bytes:
        await client.send_photo(message.chat.id, photo_bytes, caption=text)
        await message.delete()
    else:
        await message.edit(text)

async def help_pyrogram(client, message):
    user = message.from_user
    username = f"@{user.username}" if user.username else user.first_name
    text = f"""
[🤖] NEXUS USERBOT {VERSION}
[👑] Owner: {username}
[📌] COMMANDS:
[📷] `{current_prefix}info` → Bot information
[🏓] `{current_prefix}ping` → Check ping
[✨] `{current_prefix}nexus` → Photo with info
[⚙️] `{current_prefix}prefix` → Change prefix
[❓] `{current_prefix}help` → This menu"""
    photo_bytes = get_photo_bytes("help")
    if photo_bytes:
        await client.send_photo(message.chat.id, photo_bytes, caption=text)
        await message.delete()
    else:
        await message.edit(text)

# ==================== TELEGRAM HANDLER (Telethon) ====================

@telethon_client.on(telethon_events.NewMessage)
async def telethon_handler(e):
    t = e.raw_text
    if not t.startswith(current_prefix): return
    p = t.split()
    c = p[0][len(current_prefix):].lower()
    a = p[1:]
    if c == "ping":
        await ping_telethon(e, a)
    elif c == "info":
        await info_telethon(e, a)
    elif c == "nexus":
        await nexus_telethon(e, a)
    elif c == "help":
        await help_telethon(e, a)

# ==================== PYROGRAM HANDLER ====================

@pyrogram_client.on_message(pyrogram_filters.command(["ping"], prefixes=current_prefix))
async def pyrogram_ping(client, message):
    await ping_pyrogram(client, message)

@pyrogram_client.on_message(pyrogram_filters.command(["info"], prefixes=current_prefix))
async def pyrogram_info(client, message):
    await info_pyrogram(client, message)

@pyrogram_client.on_message(pyrogram_filters.command(["nexus"], prefixes=current_prefix))
async def pyrogram_nexus(client, message):
    await nexus_pyrogram(client, message)

@pyrogram_client.on_message(pyrogram_filters.command(["help"], prefixes=current_prefix))
async def pyrogram_help(client, message):
    await help_pyrogram(client, message)

# ==================== MAIN ====================

async def main():
    global telethon_client, pyrogram_client
    banner()
    
    print("[*] Starting Telethon client...")
    telethon_client = TelethonClient(SESSION_NAME + "_telethon", API_ID, API_HASH)
    await telethon_client.start()
    print("[✓] Telethon client started!")
    
    print("[*] Starting Pyrogram client...")
    pyrogram_client = PyrogramClient(
        SESSION_NAME + "_pyrogram",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    )
    await pyrogram_client.start()
    print("[✓] Pyrogram client started!")
    
    print(f"\n\033[95m[✓] NEXUS STARTED! Both clients active\033[0m")
    print(f"\033[95m[✓] {current_prefix}help\033[0m\n")
    
    # Запускаем оба клиента
    await asyncio.gather(
        telethon_client.run_until_disconnected(),
        pyrogram_client.run_until_disconnected()
    )

if __name__ == "__main__":
    try:
        env = Path(".env")
        if env.exists():
            with open(env) as f:
                for l in f:
                    if '=' in l and not l.startswith('#'):
                        k, v = l.strip().split('=', 1)
                        os.environ[k] = v
        
        API_ID = int(os.getenv("API_ID", 0))
        API_HASH = os.getenv("API_HASH", "")
        
        if not API_ID or not API_HASH:
            print("[!] No API keys!")
            print("[!] Create .env file")
            sys.exit(1)
        
        asyncio.get_event_loop().run_until_complete(main())
        
    except KeyboardInterrupt:
        print("\n[!] Stopping...")
    except Exception as e:
        print(f"[✗] {e}")
EOF

# Запускаем
python main.py
