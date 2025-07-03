# Wireguard Sunucu ve İstemci Kurulumu (Linux - Android)

##### .env.example dosyasını .env olarak yeniden adlandırın ve içindeki your_ip_adres değerini sunucunuzun adresi yapın
##### Ardından docker-compose.yml dosyasını çalıştırıcaz ve wireguard docker containeri kurulucak

``` bash 
docker compose up -d
```

##### Şimdi eğer ki halihazırda istediğiniz portlar dışındaki portlardan erişimi engelleyen bir firewall ayarınız varsa örneğin ufw, sizin birkaç ayar daha yapmanız gerekicek

##### UFW Kullanıyorsanız
``` bash 
sudo ufw allow 51820/tcp
```  

##### Şuanda bağl
sudo iptables -D INPUT -m geoip --src-cc DE -j DROP


sudo cscli decisions delete --ip 5.180.148.96

