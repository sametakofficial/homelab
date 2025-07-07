import subprocess
import json
import os
import argparse

def turkce_ses_izini_bul_ve_cikar(kaynak_dosya_yolu, ana_kaynak_dizin, ana_cikti_dizini):
    # Bu fonksiyonun içeriği aynı kalıyor, hiç bir değişiklik yok.
    print("-" * 70)
    print(f"İŞLENİYOR: '{kaynak_dosya_yolu}'")
    try:
        ffprobe_komutu = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", kaynak_dosya_yolu]
        result = subprocess.run(ffprobe_komutu, capture_output=True, text=True, check=True, encoding='utf-8')
        dosya_bilgisi = json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"HATA: Dosya analizi başarısız. Sebep: {e}")
        return False
    turkce_ses_index, turkce_ses_codec = None, None
    aranan_diller = ["tur", "turkish", "tr", "türkçe"]
    for stream in dosya_bilgisi.get("streams", []):
        if stream.get("codec_type") == "audio" and stream.get("tags", {}).get("language", "").lower() in aranan_diller:
            turkce_ses_index = stream["index"]
            turkce_ses_codec = stream["codec_name"]
            print(f"-> Türkçe ses izi bulundu! Index: {turkce_ses_index}, Codec: {turkce_ses_codec}")
            break
    if not turkce_ses_index:
        print("-> Bu dosyada Türkçe ses izi bulunamadı.")
        return False
    goreceli_yol = os.path.relpath(kaynak_dosya_yolu, ana_kaynak_dizin)
    yeni_hedef_yolu = os.path.join(ana_cikti_dizini, goreceli_yol)
    dosya_adi_temeli, _ = os.path.splitext(yeni_hedef_yolu)
    cikti_dosyasi = f"{dosya_adi_temeli}_turkce.{turkce_ses_codec}"
    cikti_klasoru = os.path.dirname(cikti_dosyasi)
    os.makedirs(cikti_klasoru, exist_ok=True)
    if os.path.exists(cikti_dosyasi):
        print(f"-> ZATEN MEVCUT: Çıktı dosyası zaten var, işlem atlanıyor.")
        return True
    print(f"-> Ses izi şuraya aktarılıyor: '{cikti_dosyasi}'")
    ffmpeg_komutu = ["ffmpeg", "-i", kaynak_dosya_yolu, "-map", f"0:{turkce_ses_index}", "-c:a", "copy", "-y", cikti_dosyasi]
    try:
        subprocess.run(ffmpeg_komutu, check=True, capture_output=True, text=True)
        print("-> BAŞARILI: İşlem tamamlandı!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"HATA: ffmpeg çalıştırılırken bir hata oluştu.\n{e.stderr}")
        return False

def ana_fonksiyon(kaynak_dizin, cikti_dizin, uzantilar):
    """
    Belirtilen kaynak dizini ve tüm alt dizinlerini tarar,
    bulunan video dosyalarını işleyerek seslerini hedef dizine çıkarır.
    """
    if not os.path.isdir(kaynak_dizin):
        print(f"HATA: Belirtilen kaynak dizini bulunamadı: '{kaynak_dizin}'")
        return

    # === YENİ VE ÖNEMLİ DEĞİŞİKLİK BURADA ===
    # Kaynak dizinin kendi adını da hedef yola ekliyoruz.
    # Önce os.path.normpath ile yolun sonundaki / işaretini (varsa) temizleyip saf klasör adını alıyoruz.
    dizi_klasor_adi = os.path.basename(os.path.normpath(kaynak_dizin))
    yeni_cikti_dizini_basi = os.path.join(cikti_dizin, dizi_klasor_adi)
    # ==========================================

    print(f"\nKaynak Dizin: '{kaynak_dizin}'")
    # DEĞİŞTİ: Kullanıcıya yeni ve tam hedef yolu gösteriyoruz.
    print(f"Hedef Dizin: '{yeni_cikti_dizini_basi}'") 
    print(f"Taranacak Uzantılar: {uzantilar}\n")
    print("Tarama ve işleme başlıyor...")
    
    toplam_dosya = 0
    basarili_islem = 0
    for root, dirs, files in os.walk(kaynak_dizin):
        for file in files:
            if file.lower().endswith(tuple(uzantilar)):
                toplam_dosya += 1
                tam_dosya_yolu = os.path.join(root, file)
                # DEĞİŞTİ: Fonksiyona yeni hesaplanan yolu gönderiyoruz.
                if turkce_ses_izini_bul_ve_cikar(tam_dosya_yolu, kaynak_dizin, yeni_cikti_dizini_basi):
                    basarili_islem +=1

    print("-" * 70)
    if toplam_dosya == 0:
        print("Tarama tamamlandı! Belirtilen yolda işlenecek video dosyası bulunamadı.")
    else:
        print(f"Tarama tamamlandı! Toplam {toplam_dosya} adet video dosyası kontrol edildi, {basarili_islem} adet ses dosyası oluşturuldu veya zaten mevcuttu.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bir dizi klasöründeki tüm videolardan Türkçe ses izlerini ayıklar.")
    parser.add_argument("-k", "--kaynak", required=True, help="İşlenecek ana dizi klasörünün tam yolu.")
    parser.add_argument("-h_dir", "--hedef", default="/srv/downloads/Audios", help="Ayıklanan seslerin kaydedileceği ana klasör. (Varsayılan: /srv/downloads/Audios)")
    parser.add_argument("-u", "--uzanti", nargs='+', default=['.mkv', '.mp4'], help="Taranacak dosya uzantıları. (Varsayılan: .mkv .mp4)")
    
    args = parser.parse_args()
    ana_fonksiyon(args.kaynak, args.hedef, args.uzanti)
