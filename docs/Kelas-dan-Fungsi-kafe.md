# Bedah Semua Class dan Fungsi — Kafe (Bahasa Mudah)

File ini menjelaskan 11 class + semua fungsi di `kafe.py` satu per satu
dengan bahasa sederhana. Cocok untuk belajar dan presentasi.

## Daftar Isi

1. [Pegawai](#1-pegawai--induk-semua-karyawan)
2. [FrontOfHouse](#2-frontofhouse--pelayan-depan)
3. [BackOfHouse](#3-backofhouse--tim-dapur)
4. [Waiter](#4-waiter)
5. [Kasir](#5-kasir)
6. [Baker](#6-baker)
7. [Barista](#7-barista)
8. [ShiftKerja](#8-shiftkerja--wadah-shift)
9. [StoreManager](#9-storemanager--penilai)
10. [SistemCafe](#10-sistemcafe--koordinator)
11. [DatabaseJSON](#11-databasejson--arsip-json)
12. [Fungsi Bebas](#12-fungsi-bebas-di-luar-class)
13. [Contoh Alur Pakai](#13-contoh-alur-pakai)

---

## 1. Pegawai — induk semua karyawan

Cetakan utama. Tidak dibuat langsung, hanya diwarisi.

```python
class Pegawai:
    def __init__(self, nama, id_pegawai, gaji):
        self.nama = nama            # bebas dibaca
        self.id_pegawai = id_pegawai  # bebas dibaca, harus unik
        self._poin = 0             # poin awal 0, menyentuh 100 langsung dipecat
        self.__gaji = gaji          # gaji dikunci
```

- `__init__(nama, id_pegawai, gaji)` — akta lahir. Begitu
  `Waiter("Andi","W01",3000000.0)` dipanggil, tiga data langsung terisi.
- `aktivitas(): pass` — sengaja dikosongkan. Artinya setiap peran
  wajib mengisi kerjaannya sendiri. Kalau lupa diisi hasilnya `None`.
- `get_gaji()` — cara baca gaji yang dikunci. Contoh `andi.get_gaji()`.
- `set_gaji(nominal)` — cara ubah gaji yang aman. Hanya mau bila
  `nominal > 0`, hasilnya `True/False`. Contoh `set_gaji(-5)` ditolak.
- `get_poin()` — baca nilai kinerja.
- `info()` — ringkasan satu baris: nama, aktivitas, gaji, poin.
- `ke_dict()` — ubah objek jadi kamus untuk disimpan ke JSON.
  Isinya `peran, nama, id, gaji, poin`. `peran` memakai
  `self.__class__.__name__` agar otomatis tertulis `Waiter/Kasir/dll`.

## 2. FrontOfHouse — pelayan depan

```python
class FrontOfHouse(Pegawai):
    def layani(self):
        return "Tersenyum dan menyapa pelanggan."
```

Anak `Pegawai`. Menambah cara melayani yang ramah. Diwarisi oleh
`Waiter` dan `Kasir` tanpa tulis ulang.

## 3. BackOfHouse — tim dapur

```python
class BackOfHouse(Pegawai):
    def layani(self):
        return "Fokus produksi, tidak langsung melayani."
```

Kebalikan Front. Diwarisi oleh `Baker` dan `Barista`.

## 4. Waiter

```python
class Waiter(FrontOfHouse):
    def aktivitas(self):
        return "Mengantar pesanan ke meja."
```

Cucu `Pegawai`. Tidak punya `__init__` sendiri, jadi memakai
warisan. `gerakannya`: aktivitas diisi sendiri, `layani()` warisan
ramah dari Front.

## 5. Kasir

```python
class Kasir(FrontOfHouse):
    def aktivitas(self):
        return "Memproses pembayaran di kasir."
```

Sama seperti Waiter, beda kalimat aktivitasnya. Inilah polimorfisme:
nama metode sama, isi beda.

## 6. Baker

```python
class Baker(BackOfHouse):
    def __init__(self, nama, id_pegawai, gaji, spesialisasi="Pastry"):
        super().__init__(nama, id_pegawai, gaji)
        self.spesialisasi = spesialisasi
    def aktivitas(self):
        return "Memanggang roti (Spesialis: " + self.spesialisasi + ")."
    def ke_dict(self):
        d = super().ke_dict()
        d["spesialisasi"] = self.spesialisasi
        return d
```

Satu-satunya peran dengan data tambahan. `super().__init__(...)`
artinya pinjam akta induk dulu, baru tambah `spesialisasi`.
`ke_dict()` juga meminjam punya induk lalu menambah kunci
`spesialisasi` agar tersimpan di JSON.

## 7. Barista

```python
class Barista(BackOfHouse):
    def __init__(self, nama, id_pegawai, gaji, spesialisasi="Menyeduh Kopi"):
        super().__init__(nama, id_pegawai, gaji)
        self.spesialisasi = spesialisasi
    def aktivitas(self):
        return "Menyeduh kopi dan meracik minuman.(Spesialis: " + self.spesialisasi + ")."
    def ke_dict(self):
        d = super().ke_dict()
        d["spesialisasi"] = self.spesialisasi
        return d
```

Seperti Baker: punya data tambahan `spesialisasi` via `super()`,
disimpan ke JSON via override `ke_dict()`. Menu tambah menanyakan
spesialisasi Barista (kosong = default).

## 8. ShiftKerja — wadah shift

```python
class ShiftKerja:
    def __init__(self, nama_shift):
        self.nama_shift = nama_shift
        self.daftar = []
```

- `tambah(p)` — masukkan satu pegawai ke `daftar` via `append`.
- `hapus(id_pegawai)` — keluarkan pegawai yang dipecat dari `daftar`,
  ketemu kembalikan `True`, tidak ketemu `False`.
- `cari(id_pegawai)` — kelilingi daftar, cocokkan ID, ketemu
  kembalikan orangnya, tidak ketemu kembalikan `None`.
- `ke_dict()` — ubah shift jadi kamus `{"nama":..., "isi":[...]}`.
  Setiap pegawai diubah via `p.ke_dict()`.

## 9. StoreManager — penilai dan pemecat

```python
class StoreManager:
    def __init__(self, nama):
        self.nama = nama
    def evaluasi(self, p):
        if p._poin < 100:
            p._poin = p._poin + 25  # 0 -> 25 -> 50 -> 75 -> 100
        if p._poin >= 100:
            return "... poin=100 (DIPECAT)"
        return "... poin=" + str(p._poin)
    def pecat(self, cafe, id_pegawai, tanggal):
        ... s.hapus(id_pegawai) ...
        ... cafe.riwayat_pecat.append(data) ...
```

- `evaluasi(p)` — menyentuh `_poin` yang protected (boleh karena
  masih kalangan kafe). Naik +25 per evaluasi. Menyentuh 100
  berarti DIPECAT.
- `pecat(cafe, id_pegawai, tanggal)` — cari pegawai di semua shift,
  bila poin >= 100 hapus via `s.hapus()`, catat ke
  `cafe.riwayat_pecat` beserta tanggal, bila belum 100 tolak dengan
  pesan sisa poin.

## 10. SistemCafe — koordinator

```python
class SistemCafe:
    def __init__(self, nama_cafe):
        self.nama_cafe = nama_cafe
        self.jadwal = []
        self.riwayat_pecat = []  # arsip yang sudah dipecat
```

- `atur_shift(s)` — tambah shift ke `jadwal`.
- `cari_shift(nama)` — cari shift berdasarkan nama.
- `cari_pegawai(id)` — cari ke semua shift, memakai `s.cari(id)`.
- `operasional()` — parade kafe. Loop tiap shift lalu tiap pegawai,
  cetak `p.aktivitas()`. Satu perintah, empat hasil beda.
- `laporan()` — tabel lengkap `p.info()` + `p.layani()`, ditambah
  bagian `--- Laporan Pemecatan ---` berisi `riwayat_pecat`
  (nama, ID, tanggal). Jadi laporan pemecatan gabung di laporan biasa.

## 11. DatabaseJSON — arsip JSON

```python
class DatabaseJSON:
    def __init__(self, path):
        self.path = path
    def simpan(self, cafe):
        ...
        json.dump(data, f, indent=2)
    def muat(self, cafe):
        try:
            ...
            json.load(f)
        except Exception:
            return False
```

- `simpan(cafe)` — ubah semua shift jadi list kamus, bungkus
  `{"nama_cafe":..., "shift":..., "pecat": riwayat_pecat}`, tulis ke file.
- `muat(cafe)` — baca file, kosongkan `jadwal`, bangun ulang via
  `buat_shift()`, pulihkan `riwayat_pecat`. Gagal kembalikan `False`
  agar program membuat contoh awal. Tanpa dekorator, metode biasa.

## 12. Fungsi Bebas di Luar Class

- `buat_pegawai(d)` — baca `d["peran"]`, buat `Waiter/Kasir/Baker/
  Barista` yang tepat, pulihkan `_poin`. Peran asing diberi
  peringatan dan dianggap Waiter.
- `buat_shift(d)` — buat `ShiftKerja`, isi ulang via `buat_pegawai`.
- `contoh_awal()` — buat kafe contoh Andi, Budi, Cici, Dedi + 2 shift.
- `tanya_angka(teks)` — minta ketikan, rapikan koma/spasi, terima
  hanya angka positif, selain itu `-1`. Mencegah crash ketik huruf.
- `menu(cafe, manager, db)` — loop 1-7: 1 tambah (cek kosong, ID unik,
  gaji positif, shift baru otomatis dibuat bila ketik nama baru),
  2 laporan (termasuk pemecatan), 3 evaluasi (+25, bila 100 langsung
  minta tanggal dan panggil `pecat()`), 4 operasional,
  5 kelola shift (buat baru, hapus kosong, pindah pegawai),
  6 ubah gaji via `set_gaji()`, 7 simpan+keluar.

## 13. Contoh Alur Pakai + Pemecatan

```python
andi = Waiter("Andi", "W01", 3000000.0)
cici = Baker("Cici", "B01", 4000000.0, "Pastry")
s1 = ShiftKerja("Pagi"); s1.tambah(andi)
cafe = SistemCafe("Belbel Cafe"); cafe.atur_shift(s1)
mgr = StoreManager("Pak Anton")
print(mgr.evaluasi(andi))  # poin 25
print(mgr.evaluasi(andi))  # poin 50
print(mgr.evaluasi(andi))  # poin 75
print(mgr.evaluasi(andi))  # poin 100 (DIPECAT)
print(mgr.pecat(cafe, "W01", "07-10-2026"))  # dihapus dari Pagi
cafe.laporan()  # Andi tampil di Laporan Pemecatan
db = DatabaseJSON("data/karyawan.json"); db.simpan(cafe)
```
