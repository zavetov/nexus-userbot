cd ~/nexus-userbot
cat > install.sh << 'EOF'
#!/bin/bash
clear
echo -e "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
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
rm -rf nexus-userbot
mkdir nexus-userbot
cd nexus-userbot

# Установка зависимостей
if [ -d "/data/data/com.termux" ]; then
    pkg update -y
    pkg install python python-pip git -y
else
    apt update -y
    apt install python3 python3-pip git -y
fi

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка telethon
pip install telethon python-dotenv requests

# Создание папок
mkdir -p modules photos logs

# СКАЧИВАЕМ ФОТО С GITHUB
echo "[*] Скачивание фото..."
curl -sL https://raw.githubusercontent.com/zavetov/nexus-userbot/main/photos/info.jpg -o photos/info.jpg
curl -sL https://raw.githubusercontent.com/zavetov/nexus-userbot/main/photos/nexus.jpg -o photos/nexus.jpg
curl -sL https://raw.githubusercontent.com/zavetov/nexus-userbot/main/photos/help.jpg -o photos/help.jpg

# Скачиваем main.py
curl -sL https://raw.githubusercontent.com/zavetov/nexus-userbot/main/main.py -o main.py

# Создаём .env
cat > .env << 'EOF'
API_ID=22571834
API_HASH=039f7fae6585323effef914021271238
EOF

echo ""
echo -e "\033[95m[✓] УСТАНОВКА ЗАВЕРШЕНА!"
echo -e "[✓] Фото загружены!"
echo -e "[✓] Запуск бота...\033[0m"
echo ""

python main.py
EOF

# Заливаем на GitHub
git add install.sh
git commit -m "Обновлен install.sh — добавлена загрузка фото"
git push
