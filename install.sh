#!/bin/bash
clear
echo -e "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
echo -e "\033[95m  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗"
echo -e "  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝"
echo -e "  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗"
echo -e "  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║"
echo -e "  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║"
echo -e "  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
echo -e "\033[95m         NEXUS USERBOT {VERSION}"
echo -e "\033[95m         @nopxcket  |  @shitlame\033[0m"
echo ""

# Проверка Termux или Linux
if [ -d "/data/data/com.termux" ]; then
    pkg update -y
    pkg upgrade -y
    pkg install python python-pip git -y
else
    apt update -y
    apt upgrade -y
    apt install python3 python3-pip git -y
fi

# Создание папок
cd ~
rm -rf nexus-userbot
mkdir nexus-userbot
cd nexus-userbot

# Создание виртуального окружения (как в Hikka)
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install telethon python-dotenv requests

# Создание файлов
mkdir -p modules photos logs

# Создание .env
cat > .env << 'EOF'
API_ID=22571834
API_HASH=039f7fae6585323effef914021271238
EOF

# Скачивание main.py
curl -sL https://raw.githubusercontent.com/zavetov/nexus-userbot/main/main.py -o main.py

# Запуск
python main.py
