# HERŞEY DAHİL NEXTCLOUD - TRAEFİK REHBER
###### çok basit bir şekilde docker-compose.yml yi kurucaz ve sadece files/config/config.php ye birkaç satır ekliyeceğiz
###### Docker ve Docker Compose kurulumu için /helper/docker-compose/README.md yi okuyabilirsiniz
###### Herşeyden önce traefik kurulu olduğuna emin olun bu rehber sadece traefik arkasında nextcloud kurulumu için

##### bu klasordeki dosyaları .env.example ve docker-compose.yml yi sunucunuzda kullanıcağınız klasore alın ve içlerinde değiştirilecek yerleri kendinize gore değiştirin ve 

``` bash
docker compose up -d 
``` 

##### yapın ve nextcloudun inmesini bekleyin.


##### bittikten sonra files/config/config.php yi nano ile açıp  ``` 'version' => '30.0.2.2', ```  satırının altına aşağıdaki satırları kendinize gore duzenleyip yapıştırın dikkat edin tekrarlanan değerler olmasın


``` bash 
'overwriteprotocol' => 'https',
  'overwritehost' => 'nextcloud.yourdomain.com',
  'overwritewebroot' => '/',
  'overwrite.cli.url' => 'https://nextcloud.yourdomain.com',
  'enable_previews' => true,
  'enabledPreviewProviders' => 
  array (
    0 => 'OC\\Preview\\Movie',
    1 => 'OC\\Preview\\PNG',
    2 => 'OC\\Preview\\JPEG',
    3 => 'OC\\Preview\\GIF',
    4 => 'OC\\Preview\\BMP',
    5 => 'OC\\Preview\\XBitmap',
    6 => 'OC\\Preview\\MP3',
    7 => 'OC\\Preview\\MP4',
    8 => 'OC\\Preview\\TXT',
    9 => 'OC\\Preview\\MarkDown',
    10 => 'OC\\Preview\\PDF',
  ),
  'trusted_proxies' => 
  array (
    0 => '127.0.0.1',
    1 => '192.168.1.1',
  ),
```
##### bunu yapma sebebimiz 
![HTTP 401 when I try to grant access to Android client ](/readme-media/mailcow-error.png) 
##### gibi hatalar yaşamamanız için
