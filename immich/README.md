# Traefik arkasında Immich kurulumu

#### Benim immich kurmakdaki tek sebebim nextcloudda depoladığım ve senkronize ettiğim fotoğraflarımı yüz tanıma, etiketleme gibi özelliklerle aynı google fotoğraflardaki giib goruntulemek tabiki immich fotoğraf eşitleme gibi ozellikler de barındırıyor ama benim ihtiyacımı nextcloud karşıladığı çin o konuda ben immichinb external library ozelliğini kullanıyorum docker-compose de yanlızca bir satırda volume olarak mount ediyorum nextcloudun fotoğraflar klasorunu, nasıl ayarlanıcağınıda anlatıcam hızlıca ama onun dışında traefik ayarlarınız tamamsa docker-compose.yml dosyasının içinden gerekli yerleri düzenledikten sonra 
``` bash 
docker compose up -d
```
#### yapmanız yeticektir sonrasında ayarladığınız domaine gidip panele erişebilirsiniz.



#### external librabry kurulumu için immich arayüzünden administrator settings / external library / add new / path olarakda /usr/src/app/external  yazarsanız bu iş tamamdır sonra yine aynı yerden sol kısımda settings e girip oradan external library dropdownunu açtıktan sonra orada Library Watching (Experimental) yazan toogle buttona tıkayın otomatik external libraryinizi kontrol edicek bu ozellik