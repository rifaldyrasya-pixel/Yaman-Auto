import os


def baca_file(nama_file):
  """Membaca data dari file eksternal dengan penanganan error izin akses"""
  if not os.path.exists(nama_file):
    try:
      with open(nama_file, "w", encoding="utf-8") as f:
        pass
    except Exception:
      pass
    return []

  data = []
  try:
    with open(nama_file, "r", encoding="utf-8") as f:
      for baris in f:
        baris = baris.strip()
        if baris:
          data.append(baris.split(","))
  except PermissionError:
    # Jika masih terkunci, buat file cadangan atau kembalikan list kosong sementara
    pass
  return data


def simpan_file(nama_file, data):
  """Menyimpan data List of List ke file eksternal dengan aman"""
  try:
    with open(nama_file, "w", encoding="utf-8") as f:
      for item in data:
        f.write(",".join(str(x) for x in item) + "\n")
  except PermissionError:
    print(f"❌ Gagal menyimpan ke {nama_file}: Akses ditolak oleh sistem.")