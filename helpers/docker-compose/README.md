# Docker, Docker Compose ve diğer gerekli paketlerin kurulumu

### UBUNTU ve Debian için ayrı ayrı yazıcam ve kurulumlar paket yöneticisi üzerinden yapıcam ki kolay güncellensin

#### UBUNTU

##### 🔧 1. Gerekli bağımlılıkları yükle
``` bash

sudo apt update
sudo apt install -y ca-certificates curl gnupg
```

 ##### 🔐 2. Docker GPG anahtarını indir ve ekle
``` bash

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
##### 📦 3. Docker deposunu Ubuntu noble için ekle
``` bash

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  noble stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    ❗ Eğer noble henüz desteklenmiyorsa jammy (22.04) olarak değiştirin:

    sed -i 's/noble/jammy/' /etc/apt/sources.list.d/docker.list
```
##### 📥 4. Paket listesini güncelle ve Docker’ı kur
``` bash

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```


##### ✅ Kurulum Testi
``` bash

sudo docker run hello-world
```

#### Debian Docker Kurulumu

##### 🔧 1. Gerekli bağımlılıkları yükle
``` bash

sudo apt update
sudo apt install -y ca-certificates curl gnupg
```
##### 🔐 2. Docker GPG anahtarını indir ve ekle
``` bash

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
 ##### 📦 3. Docker deposunu Debian bookworm için ekle
``` bash

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  bookworm stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
##### 📥 4. Paket listesini güncelle ve Docker’ı kur
``` bash

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
##### ✅ Kurulum Testi
``` bash

sudo docker run hello-world
```