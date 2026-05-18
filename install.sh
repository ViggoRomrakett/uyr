#!/bin/bash set -x
cd "$(dirname "$0")"
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root: sudo bash install.sh"
    exit 1
fi

$SUDO pacman -Sy --noconfirm --needed kitty python python-requests pipewire-pulse

mkdir -p /usr/local/share/uyr
cp -r assets /usr/local/share/uyr/
cp uyr.py /usr/local/share/uyr/
$SUDO cp uyr.sh /usr/local/bin/uyr
chmod +x /usr/local/bin/uyr
sudo chmod 755 /usr/local/bin/uyr
sudo chmod -R 755 /usr/local/share/uyr
