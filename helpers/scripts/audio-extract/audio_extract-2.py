import subprocess
import json
import os

# --- AYARLAR ---
video_dosyasi = "/srv/downloads/Movies/VOL-i - WALL-E (2008) 1080p DUAL [TR-EN] BluRay 10bit AAC 6.1 HEVC x265-QxR .mkv"
# --- AYARLAR SONU ---


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
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            dosya_yolu
        ]
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
    turkce_ses_codec = None # YENİ: Codec adını saklamak için
    aranan_diller = ["tur", "turkish", "tr", "türkçe"]

    for stream in dosya_bilgisi.get("streams", []):
        if stream.get("codec_type") == "audio":
            dil_bilgisi = stream.get("tags", {}).get("language", "").lower()
            if dil_bilgisi in aranan_diller:
                turkce_ses_index = stream["index"]
                turkce_ses_codec = stream["codec_name"] # YENİ: Codec adını yakala
                print(f"Türkçe ses izi bulundu! Index: {turkce_ses_index}, Dil Kodu: '{dil_bilgisi}'")
                print(f"Ses formatı (codec) bulundu: {turkce_ses_codec}") # YENİ: Ekrana codec'i yazdır
                break

    # 3. Adım: Türkçe ses izi bulunduysa ffmpeg ile dışa aktar.
    if turkce_ses_index is not None:
        dosya_adi, dosya_uzantisi = os.path.splitext(dosya_yolu)
        
        # YENİ: Çıktı dosyasının uzantısını bulunan codec'e göre dinamik olarak belirle
        cikti_dosyasi = f"{dosya_adi}_turkce.{turkce_ses_codec}" 

        print(f"Ses izi '{cikti_dosyasi}' olarak dışa aktarılıyor...")

        ffmpeg_komutu = [
            "ffmpeg",
            "-i", dosya_yolu,
            "-map", f"0:{turkce_ses_index}",
            "-c:a", "copy",
            "-y",
            cikti_dosyasi
        ]

        try:
            print(f"\nÇalıştırılan FFmpeg Komutu:\n{' '.join(ffmpeg_komutu)}\n")
            subprocess.run(ffmpeg_komutu, check=True)
            print("İşlem başarıyla tamamlandı!")
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg çalıştırılırken bir hata oluştu: {e}")
            print(f"Hata Çıktısı:\n{e.stderr}")

    else:
        print("Bu dosyada belirtilen kriterlere uygun Türkçe ses izi bulunamadı.")


# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    turkce_ses_izini_bul_ve_cikar(video_dosyasi)
