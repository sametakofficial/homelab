import subprocess
import json
import os

# --- AYARLAR ---
# Buraya analiz etmek istediğiniz MKV dosyasının tam yolunu yazın.
# Windows için örnek: "C:\\Users\\Kullanici\\Videolar\\dizi_bolumu.mkv"
# Linux/macOS için örnek: "/home/kullanici/Videolar/dizi_bolumu.mkv"

# --- AYARLAR SONU ---

# Örnek Düzeltme (.mkv uzantılı dosya varsayılarak)

video_dosyasi = "/srv/downloads/Movies/VOL-i - WALL-E (2008) 1080p DUAL [TR-EN] BluRay 10bit AAC 6.1 HEVC x265-QxR .mkv"
def turkce_ses_izini_bul_ve_cikar(dosya_yolu):
    """
    Belirtilen video dosyasındaki Türkçe ses izini bulur ve dışa aktarır.
    """
    if not os.path.exists(dosya_yolu):
        print(f"HATA: Belirtilen dosya bulunamadı: {dosya_yolu}")
        return

    print(f"'{dosya_yolu}' dosyası analiz ediliyor...")

    # 1. Adım: ffprobe ile dosyanın stream bilgilerini JSON formatında al.
    try:
        ffprobe_komutu = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            dosya_yolu
        ]
        # Komutu çalıştır ve çıktısını al
        result = subprocess.run(ffprobe_komutu, capture_output=True, text=True, check=True, encoding='utf-8')
        dosya_bilgisi = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ffprobe çalıştırılırken bir hata oluştu: {e}")
        print(f"Hata Çıktısı: {e.stderr}")
        return
    except json.JSONDecodeError:
        print("ffprobe çıktısı JSON formatında okunamadı.")
        return

    # 2. Adım: Ses izlerini tara ve Türkçe olanı bul.
    turkce_ses_index = None
    aranan_diller = ["tur", "turkish", "tr", "türkçe"]

    for stream in dosya_bilgisi.get("streams", []):
        if stream.get("codec_type") == "audio":
            # Stream'in etiketleri (tags) içinde dil bilgisi ara
            dil_bilgisi = stream.get("tags", {}).get("language", "").lower()
            if dil_bilgisi in aranan_diller:
                turkce_ses_index = stream["index"]
                print(f"Türkçe ses izi bulundu! Index: {turkce_ses_index}, Dil Kodu: '{dil_bilgisi}'")
                break # İlk bulunanı al ve döngüden çık

    # 3. Adım: Türkçe ses izi bulunduysa ffmpeg ile dışa aktar.
    if turkce_ses_index is not None:
        dosya_adi, dosya_uzantisi = os.path.splitext(dosya_yolu)
        cikti_dosyasi = f"{dosya_adi}_turkce.aac" # Çıktı formatı olarak AAC yaygındır.

        print(f"Ses izi '{cikti_dosyasi}' olarak dışa aktarılıyor...")

        ffmpeg_komutu = [
            "ffmpeg",
            "-i", dosya_yolu,
            "-map", f"0:{turkce_ses_index}", # Bulunan ses izini seç
            "-c:a", "copy",                # Ses izini yeniden encode etmeden kopyala
            "-y",                          # Eğer dosya varsa üzerine yaz
            cikti_dosyasi
        ]

        try:
            # Ekrana çalıştırılacak komutu yazdır
            print(f"\nÇalıştırılan FFmpeg Komutu:\n{' '.join(ffmpeg_komutu)}\n")
            subprocess.run(ffmpeg_komutu, check=True)
            print("İşlem başarıyla tamamlandı!")
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg çalıştırılırken bir hata oluştu: {e}")

    else:
        print("Bu dosyada belirtilen kriterlere uygun Türkçe ses izi bulunamadı.")


# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    turkce_ses_izini_bul_ve_cikar(video_dosyasi)
