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
git clone https://github.com/zavetov/nexus-userbot.git
cd nexus-userbot
python3 -m venv venv
source venv/bin/activate
pip install telethon python-dotenv requests
mkdir -p modules photos logs

cat > .env << 'EOF'
API_ID=22571834
API_HASH=039f7fae6585323effef914021271238
EOF

python main.py
