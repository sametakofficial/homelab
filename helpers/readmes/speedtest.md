# Debian/Ubuntu (apt)

## 1) Repo ekle
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash

## 2) Kur
sudo apt-get update
sudo apt-get install -y speedtest

## 3) İlk test (etkileşimsiz)
speedtest --accept-license --accept-gdpr

## Örnekler:
speedtest -L                                   # Yakın sunucuları listele
speedtest -s <SUNUCU_ID>                       # Belirli bir sunucuya test
speedtest --interface=eth0                     # Belirli arayüzden test
speedtest --format=json-pretty --progress=no   # JSON çıktı + progress kapalı

# Arch

## Gerekli araçlar
sudo pacman -S --needed base-devel git

## AUR’dan indir ve kur (yay yoksa makepkg ile)
git clone https://aur.archlinux.org/ookla-speedtest-bin.git
cd ookla-speedtest-bin
makepkg -si

## Çalıştır
speedtest --accept-license --accept-gdpr
