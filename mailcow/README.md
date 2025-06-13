## 2 farklı şekilde traefik arkasında çalışan mailcow kurulumu yaptım traefik reverse proxy için statik ve dinamik kurulum olarak ikiye ayırabiliriz.

## LÜTFEN OKU
### Traefik kurulumun yoksa, önce traefik klasorundeki readme'yi oku
### Daha rahat log kontrolü için portainer kullanmanızı tavsiye ederim

### Statik Kurulum

##### Kurulum yapmak istediğiniz dizine gidin, mesela benim istediğim dizin /homelab, ``` cd /homelab ``` yapıp gidiyorum ardından 

``` bash

git clone https://github.com/mailcow/mailcow-dockerized

```

##### git ile mailcow orjinal reposunu çekiyorum.

##### ``` cd /mailcow-dockerized ``` yapıp githubdan çektiğimiz reponun içine giriyoruz ve hazır kurulum scriptini çalıştırıyoruz

```bash

./generate_config.sh

```

##### mailcow reposunun içindeki mailcow.conf dosyasının içindekileri kopyalayıp .env dosyası oluşturup yapıştırmalısınız bunun ardından bu env dosyasının içindeki `SKIP_LETS_ENCRYPT=n` kısmını `SKIP_LETS_ENCRYPT=y` yapıyoruz.


##### Sonrasında docker-compose.yml deki port expose kısmını yorum satırları içine alıcaksınız

```yml
         #ports:
        #- "${HTTPS_BIND:-0.0.0.0}:${HTTPS_PORT:-443}:${HTTPS_PORT:-443}"
        #- "${HTTP_BIND:-0.0.0.0}:${HTTP_PORT:-80}:${HTTP_PORT:-80}"
```
##### Şimdi docker compose üzerine yazmak için yeni bir dosya oluşturuyoruz docker-compose.override.yml nano ile oluşturabiliriz
``` bash
nano docker-compose.override.yml
```

#### docker-compose.override.yml
```yml
services:
  nginx-mailcow:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nginx-mailcow.entrypoints=web" # Your Traefik HTTP name
      - "traefik.http.routers.nginx-mailcow.rule=HostRegexp(`{host:(autodiscover|autoconfig|webmail|mail|email).+}`)"
      - "traefik.http.middlewares.nginx-mailcow-https-redirect.redirectscheme.scheme=https"
      - "traefik.http.routers.nginx-mailcow.middlewares=nginx-mailcow-https-redirect"
      - "traefik.http.routers.nginx-mailcow-secure.entrypoints=web-secure" # Your Traefik HTTPS name
      - "traefik.http.routers.nginx-mailcow-secure.rule=Host(`mail.yourdomain.com`)" # Your Domain
      - "traefik.http.routers.nginx-mailcow-secure.tls=true"
      - "traefik.http.routers.registry-secured.tls.certresolver=your_certresolver" # Your Certresolver name
      - "traefik.http.routers.nginx-mailcow-secure.service=nginx-mailcow"
      - "traefik.http.services.nginx-mailcow.loadbalancer.server.port=80"
      - "traefik.docker.network=proxy" # Your traefik network
    networks:
      proxy:
  certdumper:
    image: humenius/traefik-certs-dumper
    container_name: traefik_certdumper
    restart: unless-stopped
    network_mode: none
    command: --restart-containers mailcowdockerized_postfix-mailcow_1,mailcowdockerized_dovecot-mailcow_1
    volumes:
      #  The folder which contains Traefik's `acme.json' file
      - /docker_volumes/traefik/data:/traefik:ro

      # Mailcow's SSL folder
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./data/assets/ssl:/output:rw
    environment:
      - DOMAIN=mail.sametak.com # Your Domain
networks:
  proxy: # Your traefik network
    external: true

```



##### Yorum satırlarındaki kısımları kendi ayarlarınıza göre düzenleyin. Burdaki mantık certresolver containeri sayesinde var olan acme dosyası içindeki mail.sametak.com için oluşturulan ssl sertifikasını manuel olarak çekip mailcowun nginx containerinin ssl sertifikasına yerleştirmek. Bu yontem hem karmaşık hemde artık birazdaha legacy bir yontem olduğu için community dokumantasyonda da bu tarz static bir yöntem kullanılmıyor bknz https://docs.mailcow.email/post_installation/reverse-proxy/r_p-traefik2/ 

### Onemli olan ve sık hata yapılan kısımlar 

#### 1.
##### Certresolver olmayan bir subdomainin sertifikasını çekemezi o yüzden ya manual olarak traefik klasoru içindeki acme.json unun içindeki örneğin yourdomain.com için olan sertifikayı kopyalayıp tekrar yapıştırıp domain kısmına oluşturacağınız subdomaini ekleyebilirsiniz sub.yourdomain.com. Bununla uğraşmak istemezsenizde certresolverin env kısmında domain istediği yere subdomaininizi değilde ana domaini yani sub.yourdomain.com değilde yourdomain.com yazıp traefik acme.jsonundan ana domainin sertifikasını çekmesini sağlayabilirsiniz zaten iki türlüde aynı sonuça varılıyor ilk yontem daha istifli çalışmama katkı sağlıyor oyuzden bende kullandım.

#### 2.
##### daha önce yaptığınız başarısız mailcow kurulumlarından arta kalan volumeleri ve diğer verileri sunucunuzdan silmediğiniz sürece işleminiz sürekli baltalanır en basit örnek veritabanı volumesi eski kurlumunuzdan kaldığında mailcow veritabanına yanlış şifre ve kullanıcı adı kombinasyonu ile bağlanıyor ve karşınıza   

```
2025/06/11 17:53:03 [error] 15#15: *1 connect() failed (111: Connection refused) while connecting to upstream, client: 31.223.48.110, server: mail.yourdomain.com, request: GET / HTTP/1.1 , upstream: fastcgi://172.22.1.6:9002 , host: mail.yourdomain.com 
```
![connect() failed (111: Connection refused) while connecting to upstream, client:](/readme-media/mailcow-error.png)

##### bu tarz hatalar çıkabilir. Aynı zamanda docker-compose.override.yml üzerinde yapacağınız her değişiklik sonrası once ``` docker compose up -d --build --force-recreate ``` ile containeri tekrar başlatmalısınız yoksa değişiklikler uygulanmaz.


### Dinamik Kurulum


##### Kurulum yapmak istediğiniz dizine gidin, mesela benim istediğim dizin /homelab, ``` cd /homelab ``` yapıp gidiyorum ardından 

``` bash

git clone https://github.com/mailcow/mailcow-dockerized

```

##### git ile mailcow orjinal reposunu çekiyorum.

##### ``` cd /mailcow-dockerized ``` yapıp githubdan çektiğimiz reponun içine giriyoruz ve hazır kurulum scriptini çalıştırıyoruz

```bash

./generate_config.sh

```

##### mailcow reposunun içindeki mailcow.conf dosyasının içindekileri kopyalayıp .env dosyası oluşturup yapıştırmalısınız bunun ardından bu env dosyasının içindeki `AUTODISCOVER_SAN=y` kısmını `AUTODISCOVER_SAN=n` yapıyoruz.

##### traefik kurulum klasorunuzdeki traefik.yml yanına bir dinamik konfigrasyon dosyası açın ( yoksa )

###### dynamic_conf.yml
``` yml
http:
  routers:
    mailcow-frontend:
      entryPoints:
        - https
      rule: "Host(`mail.yourdomain.com`)"
      service: mailcow-service
      tls:
        certResolver: your_cert_resolcer

    mailcow-autoconfig:
      entryPoints:
        - https
      rule: "Host(`autoconfig.yourdomain.com`)"
      service: mailcow-service
      tls:
        certResolver: your_cert_resolcer

    mailcow-autodiscover:
      entryPoints:
        - https
      rule: "Host(`autodiscover.yourdomain.com`)"
      service: mailcow-service
      tls:
        certResolver: your_cert_resolcer

  services:
    mailcow-service:
      loadBalancer:
        servers:
          - url: "http://10.0.0.16:80"
```

###### Eğer dosyayı yeni oluşturduysanız traefik.yml nize 

``` yml 
providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false
  ###### __________
  file:
     filename: ./dynamic_conf.yml
  ###### __________
```

###### bu kısımı ekleyebilirsiniz. İşte bu kadar dinamik kurulum daha basit ama static ve dinamiki ikisinide anlatmak istedim gorusuruz
![mail tester success](/readme-media/mailcow-success.png)