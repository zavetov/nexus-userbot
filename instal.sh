#!/bin/bash
clear
echo -e "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
echo -e "\033[95m  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗"
echo -e "  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝"
echo -e "  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗"
echo -e "  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║"
echo -e "  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║"
echo -e "  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
echo -e "\033[95m         NEXUS USERBOT 2.0"
echo -e "\033[95m         @nopxcket  |  @shitlame\033[0m"
echo ""
cd ~
rm -rf nexus
mkdir nexus
cd nexus
pkg update -y
pkg upgrade -y
pkg install python python-pip -y
pip install telethon
cat > main.py << 'EOF'
import asyncio
import time
from telethon import TelegramClient, events

API_ID = 22571834
API_HASH = "039f7fae6585323effef914021271238"

client = TelegramClient("nexus", API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r'\.ping'))
async def ping(e):
    s = time.time()
    await e.edit("🏓")
    await e.edit(f"🏓 {int((time.time()-s)*1000)}ms")

@client.on(events.NewMessage(pattern=r'\.info'))
async def info(e):
    user = await e.get_sender()
    name = f"@{user.username}" if user.username else user.first_name
    await e.edit(f"[👤] You: {name}\n[🤖] NEXUS 2.0\n@nopxcket | @shitlame")

@client.on(events.NewMessage(pattern=r'\.nexus'))
async def nexus(e):
    user = await e.get_sender()
    name = f"@{user.username}" if user.username else user.first_name
    await e.edit(f"[👑] @nopxcket & @shitlame\n[👤] You: {name}\n[🤖] NEXUS 2.0\n[📷] Prefix: .")

@client.on(events.NewMessage(pattern=r'\.help'))
async def help_cmd(e):
    await e.edit("""
[🤖] NEXUS 2.0
[📌] COMMANDS:
.info → Bot info
.ping → Check ping
.nexus → Photo info
.help → This menu
@nopxcket | @shitlame""")

async def main():
    await client.start()
    print("✅ NEXUS STARTED!")
    await client.run_until_disconnected()

asyncio.run(main())
EOF
python main.py
