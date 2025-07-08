#!/bin/bash
# DÜZELTME: set -e kaldırıldı. Hata kontrolü artık manuel yapılacak.

# Ana çalışma dizini
BASE_DIR="$HOME/homelab"

# Şifrelenecek dosyaların tam listesi
files_to_encrypt=(
  "immich/.env"
  "mailcow/.env"
  "nextcloud/.env"
  "portainer/.env"
  "torrent-tools/.env"
  "traefik/.env"
  "traefik/data/acme.json"
  "wireguard/.env"
)

read -sp "Vault password for encrypt: " VAULT_PASS_1
echo
read -sp "Confirm password: " VAULT_PASS_2
echo

if [[ "$VAULT_PASS_1" != "$VAULT_PASS_2" ]]; then
    echo "Hata: Şifreler eşleşmiyor! İşlem iptal edildi."
    exit 1
fi
VAULT_PASS=$VAULT_PASS_1

echo "--- Şifreleme işlemleri başlıyor ---"

success_count=0
skipped_count=0
not_found_count=0
total_files=${#files_to_encrypt[@]}

for file_path in "${files_to_encrypt[@]}"; do
  full_path="$BASE_DIR/$file_path"

  if [[ ! -f "$full_path" ]]; then
    echo "BULUNAMADI: Dosya mevcut değil, atlanıyor: $full_path"
    ((not_found_count++))
    continue
  fi

  if ! head -n 1 "$full_path" | grep -q "^\$ANSIBLE_VAULT;"; then
    echo "ŞİFRELENİYOR: $full_path"

    # DÜZELTME: Komutu çalıştır ve çıkış kodunu hemen yakala
    ansible-vault encrypt --vault-password-file=/dev/stdin "$full_path" <<< "$VAULT_PASS"
    exit_code=$?

    # DÜZELTME: Çıkış kodunu manuel olarak kontrol et
    if [[ $exit_code -eq 0 ]]; then
      ((success_count++))
    else
      # Gerçek bir hata varsa, script'i durdur.
      echo "HATA: '$full_path' için şifreleme başarısız oldu (Çıkış Kodu: $exit_code)."
      exit 1
    fi
  else
    echo "ATLANDI: Dosya zaten şifreli: $full_path"
    ((skipped_count++))
  fi
done

echo "--- İşlem Özeti ---"
echo "Toplam $total_files dosya hedeflendi."
echo "  - Başarıyla şifrelenen: $success_count"
echo "  - Atlanan (zaten şifreliydi): $skipped_count"
echo "  - Bulunamayan: $not_found_count"
echo "---------------------"

if (( not_found_count == 0 && skipped_count == 0 && success_count == total_files )); then
    echo "Sonuç: Tüm dosyalar başarıyla şifrelendi."
else
    echo "Sonuç: İşlemler tamamlandı."
fi
