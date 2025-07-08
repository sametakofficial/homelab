#!/bin/bash
# DÜZELTME: set -e kaldırıldı. Hata kontrolü artık manuel yapılacak.

# Ana çalışma dizini
BASE_DIR="$HOME/homelab"

# Şifresi çözülecek dosyaların tam listesi
files_to_decrypt=(
  "immich/.env"
  "mailcow/.env"
  "nextcloud/.env"
  "portainer/.env"
  "torrent-tools/.env"
  "traefik/.env"
  "traefik/data/acme.json"
  "wireguard/.env"
)

read -sp "Vault password for decrypt: " VAULT_PASS
echo

echo "--- Şifre çözme işlemleri başlıyor ---"

success_count=0
skipped_count=0
not_found_count=0
total_files=${#files_to_decrypt[@]}

for file_path in "${files_to_decrypt[@]}"; do
  full_path="$BASE_DIR/$file_path"

  if [[ ! -f "$full_path" ]]; then
    echo "BULUNAMADI: Dosya mevcut değil, atlanıyor: $full_path"
    ((not_found_count++))
    continue
  fi

  if head -n 1 "$full_path" | grep -q "^\$ANSIBLE_VAULT;"; then
    echo "ÇÖZÜLÜYOR: $full_path"
    
    # DÜZELTME: Komutu çalıştır ve çıkış kodunu hemen yakala
    ansible-vault decrypt --vault-password-file=/dev/stdin "$full_path" <<< "$VAULT_PASS"
    exit_code=$?

    # DÜZELTME: Çıkış kodunu manuel olarak kontrol et
    if [[ $exit_code -eq 0 ]]; then
      ((success_count++))
    else
      # Gerçek bir hata varsa (yanlış şifre vb.), script'i durdur.
      echo "HATA: '$full_path' için şifre çözme başarısız oldu (Çıkış Kodu: $exit_code). Şifre yanlış olabilir."
      exit 1
    fi
  else
    echo "ATLANDI: Dosya zaten şifresiz: $full_path"
    ((skipped_count++))
  fi
done

echo "--- İşlem Özeti ---"
echo "Toplam $total_files dosya hedeflendi."
echo "  - Başarıyla şifresi çözülen: $success_count"
echo "  - Atlanan (zaten şifresizdi): $skipped_count"
echo "  - Bulunamayan: $not_found_count"
echo "---------------------"

if (( not_found_count == 0 && skipped_count == 0 && success_count == total_files )); then
    echo "Sonuç: Tüm dosyaların şifresi başarıyla çözüldü."
else
    echo "Sonuç: İşlemler tamamlandı."
fi
