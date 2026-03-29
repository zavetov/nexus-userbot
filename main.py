#!/usr/bin/env python3
import asyncio
import sys
import time
import os
import platform
from pathlib import Path
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

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

client = None
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

async def ping(e, a):
    s = time.time()
    await e.edit("🏓 Pong...")
    await asyncio.sleep(0.05)
    await e.edit(f"🏓 Pong!\n📡 Ping: `{int((time.time()-s)*1000)} ms`")

async def info(e, a):
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
        await client.send_file(e.chat_id, photo_bytes, caption=text, parse_mode='markdown')
        await e.delete()
    else:
        await e.edit(text, parse_mode='markdown')

async def nexus(e, a):
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
        await client.send_file(e.chat_id, photo_bytes, caption=text, parse_mode='markdown')
        await e.delete()
    else:
        await e.edit(text, parse_mode='markdown')

async def modules(e, a):
    await e.edit("[📦] Modules command")

async def install(e, a):
    await e.edit("[📥] Install command")

async def reload(e, a):
    await e.edit("[🔄] Reload command")

async def prefix_cmd(e, a):
    global current_prefix
    if e.sender_id != OWNER_ID:
        await e.edit("[❌] Only owner can change prefix!")
        return
    if not a:
        await e.edit(f"[📷] Current prefix: `{current_prefix}`")
        return
    current_prefix = a[0]
    await e.edit(f"[✅] Prefix changed to: `{current_prefix}`")

async def help_cmd(e, a):
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
        await client.send_file(e.chat_id, photo_bytes, caption=text)
        await e.delete()
    else:
        await e.edit(text)

cmds['ping'] = ping
cmds['info'] = info
cmds['nexus'] = nexus
cmds['modules'] = modules
cmds['install'] = install
cmds['reload'] = reload
cmds['prefix'] = prefix_cmd
cmds['help'] = help_cmd

async def handler(e):
    t = e.raw_text
    if not t.startswith(current_prefix): return
    p = t.split()
    c = p[0][len(current_prefix):].lower()
    a = p[1:]
    if c in cmds:
        try:
            await cmds[c](e, a)
        except Exception as ex:
            await e.reply(f"[❌] {ex}")

async def main():
    global client
    banner()
    client.add_event_handler(handler, events.NewMessage)
    print(f"\n\033[95m[✓] NEXUS STARTED! {len(cmds)} commands\033[0m")
    print(f"\033[95m[✓] {current_prefix}help\033[0m\n")
    await client.run_until_disconnected()

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
        
        print("[*] Connecting...")
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        client.start()
        print("\033[95m[✓] NEXUS STARTED!\033[0m\n")
        
        asyncio.get_event_loop().run_until_complete(main())
        
    except SessionPasswordNeededError:
        pwd = input("2FA: ")
        client.sign_in(password=pwd)
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("\n[!] Stopping...")
    except Exception as e:
        print(f"[✗] {e}")
