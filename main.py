#!/usr/bin/env python3
import asyncio
import sys
import time
import os
import platform
import json
import requests
from pathlib import Path
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
PREFIX = "."
SESSION = "nexus"
NAME = "NEXUS"
VERSION = "2.0.0"
ADMINS = [7909649275, 7383593060]
GROUP_LINK = "https://t.me/userbotnexus"

BASE = Path(__file__).parent
MODS = BASE / "modules"
DATA_FILE = BASE / "data.json"
PHOTOS_DIR = BASE / "photos"
MODS.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(exist_ok=True)

client = None
cmds = {}
loaded = {}
start = time.time()
current_prefix = PREFIX
current_lang = "ru"

TEXTS = {
    "ru": {
        "ping": "[🏓] Понг...",
        "pong": "[🏓] Понг!\n📡 Задержка: `{} мс`",
        "owner": "[👑] Владелец: @nopxcket & @shitlame",
        "you": "[👤] Ты: {}",
        "version": "[🤖] Версия: {}",
        "prefix": "[📷] Префикс: «{}»",
        "uptime": "[🔄] Аптайм: {}",
        "ping_stat": "[📊] Пинг: {} мс",
        "system": "[💻] Система: {}",
        "install_btn": "[🔗] [УСТАНОВИТЬ]({})",
        "nexus_title": "[🤖] NEXUS {}",
        "no_modules": "[📦] Нет загруженных модулей",
        "modules": "[📦] МОДУЛИ:\n\n",
        "install_usage": "[❌] Использование: `{}install <url>` или ответь на .py файл",
        "installing": "[📥] Установка...",
        "installed": "[✅] Установлен: `{}`",
        "error_http": "[❌] Ошибка: HTTP {}",
        "reloading": "[🔄] Перезагрузка модулей...",
        "reloaded": "[✅] Перезагружено {} модулей",
        "only_admin": "[❌] Только админы могут менять префикс!",
        "current_prefix": "[📷] Текущий префикс: `{}`\nИспользование: `{}prefix <новый_префикс>`",
        "prefix_changed": "[✅] Префикс изменен!\n\nСтарый: `{}`\nНовый: `{}`",
        "help_title": "[🤖] NEXUS USERBOT {}\n[👑] Владелец: {}",
        "commands": "[📌] КОМАНДЫ:\n\n[📷] `{}info` → Информация о боте\n[🏓] `{}ping` → Проверка задержки\n[✨] `{}nexus` → Фото с информацией\n[📦] `{}modules` → Список модулей\n[📥] `{}install` → Установка модуля\n[🔄] `{}reload` → Перезагрузка модулей\n[⚙️] `{}prefix` → Смена префикса\n[🌐] `{}language` → Смена языка (ru/en)\n[❓] `{}help` → Это меню",
        "lang_changed": "[✅] Язык изменен на {}",
        "lang_usage": "[❌] Использование: `{}language ru/en`",
        "photo_set": "[✅] Фото для .{} установлено!",
        "photo_usage": "[❌] Использование: `.sendphoto <info|nexus|help>` (ответь на фото)",
        "photo_only_admin": "[❌] Только админы могут менять фото!"
    },
    "en": {
        "ping": "[🏓] Pong...",
        "pong": "[🏓] Pong!\n📡 Ping: `{} ms`",
        "owner": "[👑] Owner: @nopxcket & @shitlame",
        "you": "[👤] You: {}",
        "version": "[🤖] Version: {}",
        "prefix": "[📷] Prefix: «{}»",
        "uptime": "[🔄] Uptime: {}",
        "ping_stat": "[📊] Ping: {} ms",
        "system": "[💻] System: {}",
        "install_btn": "[🔗] [INSTALL]({})",
        "nexus_title": "[🤖] NEXUS {}",
        "no_modules": "[📦] No modules loaded",
        "modules": "[📦] MODULES:\n\n",
        "install_usage": "[❌] Usage: `{}install <url>` or reply to .py file",
        "installing": "[📥] Installing...",
        "installed": "[✅] Installed: `{}`",
        "error_http": "[❌] Error: HTTP {}",
        "reloading": "[🔄] Reloading modules...",
        "reloaded": "[✅] Reloaded {} modules",
        "only_admin": "[❌] Only admins can change prefix!",
        "current_prefix": "[📷] Current prefix: `{}`\nUsage: `{}prefix <new_prefix>`",
        "prefix_changed": "[✅] Prefix changed!\n\nOld: `{}`\nNew: `{}`",
        "help_title": "[🤖] NEXUS USERBOT {}\n[👑] Owner: {}",
        "commands": "[📌] COMMANDS:\n\n[📷] `{}info` → Bot information\n[🏓] `{}ping` → Check ping\n[✨] `{}nexus` → Photo with info\n[📦] `{}modules` → List modules\n[📥] `{}install` → Install module\n[🔄] `{}reload` → Reload modules\n[⚙️] `{}prefix` → Change prefix\n[🌐] `{}language` → Change language (ru/en)\n[❓] `{}help` → This menu",
        "lang_changed": "[✅] Language changed to {}",
        "lang_usage": "[❌] Usage: `{}language ru/en`",
        "photo_set": "[✅] Photo for .{} set!",
        "photo_usage": "[❌] Usage: `.sendphoto <info|nexus|help>` (reply to photo)",
        "photo_only_admin": "[❌] Only admins can change photo!"
    }
}

def t(key, *args):
    text = TEXTS[current_lang].get(key, key)
    return text.format(*args) if args else text

if DATA_FILE.exists():
    try:
        with open(DATA_FILE, 'r') as f:
            saved = json.load(f)
            current_prefix = saved.get('prefix', PREFIX)
            current_lang = saved.get('lang', "ru")
    except:
        pass

def save_data():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump({'prefix': current_prefix, 'lang': current_lang}, f)
    except:
        pass

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
    print("\n" * 30)
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
    await e.edit(t("ping"))
    await asyncio.sleep(0.05)
    await e.edit(t("pong", int((time.time()-s)*1000)))

async def info(e, a):
    user = await e.get_sender()
    username = f"@{user.username}" if user.username else user.first_name
    uptime = get_uptime()
    s = time.time()
    ping_real = int((time.time() - s) * 1000)
    text = f"""
{t("you", username)}
{t("version", VERSION)}
{t("prefix", current_prefix)}
{t("uptime", uptime)}
{t("ping_stat", ping_real)}
{t("system", platform.system())}
{t("install_btn", GROUP_LINK)}"""
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
{t("owner")}
{t("you", username)}
{t("nexus_title", VERSION)}
{t("prefix", current_prefix)}
{t("install_btn", GROUP_LINK)}"""
    photo_bytes = get_photo_bytes("nexus")
    if photo_bytes:
        await client.send_file(e.chat_id, photo_bytes, caption=text, parse_mode='markdown')
        await e.delete()
    else:
        await e.edit(text, parse_mode='markdown')

async def modules(e, a):
    if not loaded:
        await e.edit(t("no_modules"))
        return
    text = t("modules")
    for n, i in loaded.items():
        cmds_list = ", ".join(i.get('cmds', []))
        text += f"🔷 {n}\n"
        if cmds_list:
            text += f"   └ Команды: {cmds_list}\n"
    await e.edit(text)

async def install(e, a):
    if a:
        url = a[0]
        msg = await e.edit(t("installing"))
        try:
            if "github.com" in url:
                if "/blob/" in url:
                    url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                else:
                    url = url.replace("github.com", "raw.githubusercontent.com")
                    if not url.endswith(".py"):
                        url = f"{url}/main/main.py"
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                file_name = f"{int(time.time())}_{url.split('/')[-1]}"
                file_path = MODS / file_name
                with open(file_path, 'w') as f:
                    f.write(r.text)
                n = file_path.stem
                spec = importlib.util.spec_from_file_location(n, file_path)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[n] = mod
                spec.loader.exec_module(mod)
                cmds_list = []
                for cmd_name, cmd_func in cmds.items():
                    if hasattr(cmd_func, '__module__') and cmd_func.__module__ == n:
                        cmds_list.append(cmd_name)
                loaded[n] = {'t': 'native', 'cmds': cmds_list}
                await msg.edit(t("installed", n) + (f"\n📝 Команды: {', '.join(cmds_list)}" if cmds_list else ""))
            else:
                await msg.edit(t("error_http", r.status_code))
        except Exception as ex:
            await msg.edit(f"[❌] {ex}")
        return
    if e.is_reply:
        reply = await e.get_reply_message()
        if reply.file and reply.file.name and reply.file.name.endswith('.py'):
            msg = await e.edit(t("installing"))
            try:
                file_name = f"{int(time.time())}_{reply.file.name}"
                file_path = MODS / file_name
                await client.download_file(reply.media, file_path)
                n = file_path.stem
                spec = importlib.util.spec_from_file_location(n, file_path)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[n] = mod
                spec.loader.exec_module(mod)
                cmds_list = []
                for cmd_name, cmd_func in cmds.items():
                    if hasattr(cmd_func, '__module__') and cmd_func.__module__ == n:
                        cmds_list.append(cmd_name)
                loaded[n] = {'t': 'native', 'cmds': cmds_list}
                await msg.edit(t("installed", n) + (f"\n📝 Команды: {', '.join(cmds_list)}" if cmds_list else ""))
            except Exception as ex:
                await msg.edit(f"[❌] {ex}")
        else:
            await e.edit(t("install_usage", current_prefix))
    else:
        await e.edit(t("install_usage", current_prefix))

async def reload(e, a):
    msg = await e.edit(t("reloading"))
    loaded.clear()
    c = 0
    for f in MODS.glob("*.py"):
        if f.name != "__init__.py":
            try:
                n = f.stem
                if n in sys.modules:
                    del sys.modules[n]
                spec = importlib.util.spec_from_file_location(n, f)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[n] = mod
                spec.loader.exec_module(mod)
                cmds_list = []
                for cmd_name, cmd_func in cmds.items():
                    if hasattr(cmd_func, '__module__') and cmd_func.__module__ == n:
                        cmds_list.append(cmd_name)
                loaded[n] = {'t': 'native', 'cmds': cmds_list}
                c += 1
            except:
                pass
    await msg.edit(t("reloaded", c))

async def prefix_cmd(e, a):
    global current_prefix
    if e.sender_id not in ADMINS:
        await e.edit(t("only_admin"))
        return
    if not a:
        await e.edit(t("current_prefix", current_prefix, current_prefix))
        return
    new_prefix = a[0]
    old_prefix = current_prefix
    current_prefix = new_prefix
    save_data()
    await e.edit(t("prefix_changed", old_prefix, current_prefix))

async def language_cmd(e, a):
    global current_lang
    if e.sender_id not in ADMINS:
        await e.edit("[❌] Only admins can change language!")
        return
    if not a or a[0] not in ["ru", "en"]:
        await e.edit(t("lang_usage", current_prefix))
        return
    current_lang = a[0]
    save_data()
    await e.edit(t("lang_changed", "🇷🇺 Русский" if current_lang == "ru" else "🇬🇧 English"))

async def sendphoto_cmd(e, a):
    if e.sender_id not in ADMINS:
        await e.edit(t("photo_only_admin"))
        return
    if not a:
        await e.edit(t("photo_usage"))
        return
    cmd_type = a[0].lower()
    if cmd_type not in ["info", "nexus", "help"]:
        await e.edit("[❌] Доступные типы: info, nexus, help")
        return
    if not e.is_reply:
        await e.edit("[❌] Ответь на фото командой!")
        return
    reply = await e.get_reply_message()
    if not reply.photo:
        await e.edit("[❌] Ответь именно на фото!")
        return
    msg = await e.edit(f"[📸] Сохраняю фото для .{cmd_type}...")
    photo_path = PHOTOS_DIR / f"{cmd_type}.jpg"
    await client.download_media(reply.photo, photo_path)
    await msg.edit(t("photo_set", cmd_type))

async def help_cmd(e, a):
    user = await e.get_sender()
    username = f"@{user.username}" if user.username else user.first_name
    text = t("help_title", VERSION, username) + "\n\n" + t("commands", 
        current_prefix, current_prefix, current_prefix, current_prefix, 
        current_prefix, current_prefix, current_prefix, current_prefix, current_prefix)
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
cmds['language'] = language_cmd
cmds['sendphoto'] = sendphoto_cmd
cmds['help'] = help_cmd

async def handler(e):
    t = e.raw_text
    if not t.startswith(current_prefix):
        return
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
    for f in MODS.glob("*.py"):
        if f.name != "__init__.py":
            try:
                n = f.stem
                spec = importlib.util.spec_from_file_location(n, f)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[n] = mod
                spec.loader.exec_module(mod)
                cmds_list = []
                for cmd_name, cmd_func in cmds.items():
                    if hasattr(cmd_func, '__module__') and cmd_func.__module__ == n:
                        cmds_list.append(cmd_name)
                loaded[n] = {'t': 'native', 'cmds': cmds_list}
                print(f"[✓] {n}")
            except Exception as ex:
                print(f"[✗] {f.stem}: {ex}")
    client.add_event_handler(handler, events.NewMessage)
    print(f"\n\033[95m[✓] NEXUS STARTED! {len(cmds)} commands, {len(loaded)} modules\033[0m")
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
        client = TelegramClient(SESSION, API_ID, API_HASH)
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
