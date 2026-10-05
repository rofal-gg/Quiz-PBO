# Sistem Kebun Binatang Gembira — Panduan Praktikum PBO (Python)

Simulasi pengelolaan kebun binatang dengan Pemrograman Berorientasi Objek (PBO) Python.
Analogi nyata: **Pemilik kebun** mengelola area, **Kandang** sebagai wadah, **Hewan** sebagai penghuni, **DokterHewan** sebagai perawat. Pengguna tidak mengatur tiap hewan manual, melainkan membuat **satu cetakan (class)**, lalu **mencetak objek nyata** seperti `Singa("Leo")`, `Gajah("Eli")`, `Elang("Edo")`, `Ular("Ulo")`, memasukkannya ke kandang, menghimpun kandang ke kebun, lalu menjalankan parade suara.

Total **10 class**: `Hewan, Mamalia, Burung, Singa, Gajah, Elang, Ular, Kandang, DokterHewan, KebunBinatang`.

File utama: `kebun_binatang.py` (96 baris, tanpa library eksternal).

---

## Daftar Isi

1. [Cara Menjalankan Program](#1-cara-menjalankan-program)
2. [Penjelasan Lengkap Kode per Class](#2-penjelasan-lengkap-kode-per-class-untuk-dipelajari)
3. [Cara Menggunakan Class dan Fungsinya (dengan Contoh Sintaks)](#3-cara-menggunakan-class-dan-fungsinya-dengan-contoh-sintaks)
4. [Cara Menambahkan Binatang Baru](#4-cara-menambahkan-binatang-baru-panduan-lengkap)
5. [Bedah Konsep OOP](#5-bedah-konsep-oop-inti-presentasi)
6. [Alur Kerja Program (Main hingga Selesai)](#6-alur-kerja-program-dari-main-hingga-selesai)
7. [Naskah Presentasi / Script Praktikum 4 Orang](#7-naskah-presentasi--script-praktikum-4-orang-formal)
8. [Tips Presentasi](#8-tips-presentasi-tiga-poin-utama)
9. [Prediksi Pertanyaan Dosen Beserta Jawaban](#9-prediksi-pertanyaan-kritis-dosen-beserta-jawaban)

---

## 1. Cara Menjalankan Program

```bash
# dari folder proyek:
python3 kebun_binatang.py
```

Output yang benar:

```text
Dr. Ani memeriksa Leo: sehat!
Eli menyusui anaknya | belalai: 1.8 m
Berat Eli: 1200 kg
Berat baru: 1250 kg
--- Parade Suara ---
Leo: Roar! (berjalan)
Eli: Trumpet! (berjalan)
Edo: Screech! (terbang)
Ulo: Hiss! (melata)
```

> Program tidak butuh `pip install` apa pun. Cukup Python 3.

---

## 2. Penjelasan Lengkap Kode per Class (Untuk Dipelajari)

### 2.1 `class Hewan` — Induk abstrak semua hewan

```python
class Hewan:
    def __init__(self, nama, berat):
        self.nama = nama            # public: bebas dibaca
        self._kesehatan = 100       # protected: milik internal kebun
        self.__berat = berat        # private: disembunyikan
    def suara(self):
        pass  # kosong, anak wajib isi sendiri
    def gerak(self):
        pass  # kosong, anak wajib isi sendiri
    def get_berat(self):
        return self.__berat            # getter
    def set_berat(self, b):            # setter + validasi
        if b > 0: self.__berat = b
    def info(self):
        return f"{self.nama} | {self.gerak()} | {self.suara()} | {self.__berat}kg"
```

Penjelasan baris per baris:

- `__init__(self, nama, berat)` — konstruktor. Dipanggil otomatis saat `Hewan("X", 10)`. Mengisi 3 atribut: `nama`, `_kesehatan`, `__berat`.
- `self.nama` — **public**. Boleh dibaca/tulis dari mana saja: `leo.nama`, `leo.nama = "Leon"`.
- `self._kesehatan` — **protected** (konvensi satu underscore). Artinya "jangan disentuh orang luar, hanya kalangan kebun". Contoh yang boleh: `DokterHewan.periksa()` mengeset `h._kesehatan = 100`.
- `self.__berat` — **private** (dua underscore). Python mengubah namanya jadi `_Hewan__berat` (name mangling) sehingga `eli.__berat` dari luar akan error `AttributeError`. Satu-satunya jalan resmi: `get_berat()` / `set_berat()`.
- `suara()` / `gerak()` berisi `pass` — sengaja dikosongkan. Ini kontrak: "setiap hewan WAJIB punya suara dan gerak, isinya terserah anak". Ini bentuk **abstraksi sederhana** (versi ketatnya memakai `ABC` + `@abstractmethod`, lihat bagian 9 soal kelemahan).
- `get_berat()` / `set_berat(b)` — getter/setter aman. Setter menolak nilai `<= 0`, jadi berat tidak bisa negatif/nol.
- `info()` — metode bantu. Boleh membaca `self.__berat` karena ia **berada di dalam class yang sama**. Aturan private hanya melarang akses dari luar, bukan dari dalam.

### 2.2 `class Mamalia(Hewan)` dan `class Burung(Hewan)` — Perantara level 1

```python
class Mamalia(Hewan):
    def gerak(self):
        return "berjalan"  # sifat umum mamalia
    def menyusui(self):
        return f"{self.nama} menyusui anaknya"

class Burung(Hewan):
    def gerak(self):
        return "terbang"   # sifat umum burung
```

- `(Hewan)` artinya **inheritance**: mewarisi `__init__`, `nama`, `_kesehatan`, `__berat`, `get_berat`, `set_berat`, `info`, `suara` dari `Hewan` tanpa menulis ulang.
- `Mamalia` mengisi `gerak()` menjadi `"berjalan"` dan menambah kemampuan baru `menyusui()`. Semua anak Mamalia (Singa, Gajah) otomatis bisa `menyusui()` dan `berjalan`.
- `Burung` mengisi `gerak()` menjadi `"terbang"`. Semua anak Burung otomatis bisa terbang kecuali meng-override ulang (contoh: Pinguin, lihat bagian 4).

### 2.3 `class Singa, Gajah, Elang, Ular` — Hewan nyata level 2

```python
class Singa(Mamalia):
    def suara(self):
        return "Roar!"

class Gajah(Mamalia):
    def __init__(self, nama, berat, belalai=2):
        super().__init__(nama, berat)
        self.belalai = belalai
    def suara(self):
        return "Trumpet!"

class Elang(Burung):
    def suara(self):
        return "Screech!"

class Ular(Hewan):  # langsung dari Hewan, tanpa perantara
    def suara(self):
        return "Hiss!"
    def gerak(self):
        return "melata"
```

- `Singa` hanya mengisi `suara()`. `gerak()` tidak ditulis karena sudah diwarisi `"berjalan"` dari `Mamalia`. Konstruktor pun diwarisi, jadi `Singa("Leo", 190)` tetap bisa isi nama+berat walau Singa tidak punya `__init__` sendiri.
- `Gajah` contoh **konstruktor + `super()`**: butuh atribut tambahan `belalai` yang tidak dimiliki hewan lain. `super().__init__(nama, berat)` = "pinjam proses inisialisasi induk dulu", lalu tambah `self.belalai`. Nilai default `belalai=2` (meter) boleh diisi boleh tidak.
- `Elang` sama polanya seperti Singa, tapi mewarisi `"terbang"` dari `Burung`.
- `Ular` langsung mewarisi `Hewan` karena bukan mamalia maupun burung. Ia wajib mengisi **keduanya**: `suara()` → `"Hiss!"` dan `gerak()` → `"melata"`.

### 2.4 `class Kandang` — Wadah hewan

```python
class Kandang:
    def __init__(self, nama):
        self.nama = nama
        self.isi = []
    def tambah(self, h):
        self.isi.append(h)
```

- `nama`: label kandang, misal `"Mamalia"`, `"Lainnya"`.
- `isi`: list kosong yang menampung objek hewan.
- `tambah(h)`: memasukkan satu objek hewan ke list. `h` bisa objek apa saja yang punya `suara()`/`gerak()` (duck typing).

### 2.5 `class DokterHewan` — Perawat hewan

```python
class DokterHewan:
    def __init__(self, nama):
        self.nama = nama
    def periksa(self, h):
        h._kesehatan = 100
        return f"{self.nama} memeriksa {h.nama}: sehat!"
```

- `periksa(h)` menyentuh atribut **protected** `h._kesehatan`. Ini diperbolehkan karena dokter adalah "kalangan dalam kebun", bukan orang luar. Ini BUKAN pelanggaran enkapsulasi, melainkan penggunaan sesuai konvensi.

### 2.6 `class KebunBinatang` — Koordinator semua kandang

```python
class KebunBinatang:
    def __init__(self, nama):
        self.nama = nama
        self.kandang = []
    def tambah_kandang(self, k):
        self.kandang.append(k)
    def parade(self):
        for k in self.kandang:
            for h in k.isi: print(f"{h.nama}: {h.suara()} ({h.gerak()})")
```

- Struktur bersarang: `KebunBinatang` → punya banyak `Kandang` → tiap kandang punya banyak `Hewan`. Ini relasi **komposisi/asosiasi**, bukan pewarisan.
- `parade()` adalah bukti **polimorfisme**: satu perintah `h.suara()` menghasilkan output berbeda per objek (lihat bagian 5).

### 2.7 Blok `Main` — Tempat semua objek dilahirkan

```python
if __name__ == "__main__":
    leo = Singa("Leo", 190)
    eli = Gajah("Eli", 1200, 1.8)
    edo = Elang("Edo", 6)
    ulo = Ular("Ulo", 8)

    k1 = Kandang("Mamalia"); k1.tambah(leo); k1.tambah(eli)
    k2 = Kandang("Lainnya"); k2.tambah(edo); k2.tambah(ulo)

    kebun = KebunBinatang("Gembira"); kebun.tambah_kandang(k1); kebun.tambah_kandang(k2)
    dok = DokterHewan("Dr. Ani")

    print(dok.periksa(leo))
    print(eli.menyusui(), "| belalai:", eli.belalai, "m")
    print("Berat Eli:", eli.get_berat(), "kg"); eli.set_berat(1250)
    print("Berat baru:", eli.get_berat(), "kg")
    print("--- Parade Suara ---"); kebun.parade()
```

- Tanpa blok ini, semua class hanya rancangan. `leo = Singa("Leo", 190)` = mencetak objek nyata dari cetakan class lewat konstruktor.
- `if __name__ == "__main__":` artinya kode di dalamnya hanya jalan saat file dieksekusi langsung, tidak saat di-`import` dari file lain (penting untuk praktikum/import ulang).

---

## 3. Cara Menggunakan Class dan Fungsinya (dengan Contoh Sintaks)

Pola umum selalu sama 3 langkah: **import (jika beda file) → buat objek → panggil metode**.

```python
from kebun_binatang import Singa, Gajah, Elang, Ular, Kandang, DokterHewan, KebunBinatang
```

### 3.1 Membuat hewan (konstruktor + instance)

```python
leo = Singa("Leo", 190)       # (nama, berat_kg) — __init__ diwarisi dari Hewan
eli = Gajah("Eli", 1200, 1.8) # (nama, berat_kg, belalai_meter) — belalai opsional, default 2
edo = Elang("Edo", 6)         # burung kecil 6 kg
ulo = Ular("Ulo", 8)          # langsung dari Hewan

# Tanpa belalai pun bisa (pakai default):
eli2 = Gajah("Eli2", 1100)
print(eli2.belalai)  # -> 2
```

Aturan parameter:

| Class | Signature | Contoh |
|---|---|---|
| `Singa(nama, berat)` | warisan `Hewan.__init__` | `Singa("Leo", 190)` |
| `Gajah(nama, berat, belalai=2)` | `__init__` sendiri + `super()` | `Gajah("Eli", 1200, 1.8)` |
| `Elang(nama, berat)` | warisan `Hewan.__init__` | `Elang("Edo", 6)` |
| `Ular(nama, berat)` | warisan `Hewan.__init__` | `Ular("Ulo", 8)` |

### 3.2 Fungsi di dalam `Hewan` (diwarisi semua hewan)

```python
# suara() dan gerak() — perilaku khas tiap hewan (hasil overriding):
print(leo.suara())  # Roar!      (dari Singa)
print(leo.gerak())  # berjalan   (dari Mamalia)
print(edo.gerak())  # terbang    (dari Burung)
print(ulo.suara())  # Hiss!      (dari Ular)
print(ulo.gerak())  # melata     (dari Ular)

# nama (public) — bebas baca/tulis:
print(leo.nama)         # Leo
leo.nama = "Leon"       # boleh diganti langsung

# _kesehatan (protected) — JANGAN ubah manual dari luar, pakai dokter:
print(leo._kesehatan)   # 100 (boleh dibaca, tapi jangan ditimpa manual)

# __berat (private) — WAJIB lewat getter/setter:
print(eli.get_berat())  # 1200
eli.set_berat(1250)     # valid -> berubah
eli.set_berat(-50)      # tidak valid -> ditolak, berat tetap 1250
# eli.__berat           # ERROR AttributeError, jangan dilakukan

# info() — ringkasan satu baris:
print(eli.info())  # Eli | berjalan | Trumpet! | 1200kg
```

### 3.3 Fungsi khusus `Mamalia` — `menyusui()`

```python
print(leo.menyusui())  # Leo menyusui anaknya
print(eli.menyusui())  # Eli menyusui anaknya
# print(edo.menyusui())  # ERROR — Elang bukan Mamalia, tidak punya metode ini
```

Hanya `Singa` dan `Gajah` (turunan `Mamalia`) yang bisa memanggilnya.

### 3.4 Fungsi di dalam `Kandang` — `tambah()`

```python
k1 = Kandang("Mamalia")  # buat wadah
k1.tambah(leo)           # masukkan satu hewan
k1.tambah(eli)
print(len(k1.isi))       # 2
print(k1.isi[0].nama)    # Leo
```

### 3.5 Fungsi di dalam `DokterHewan` — `periksa()`

```python
dok = DokterHewan("Dr. Ani")
print(dok.periksa(leo))  # Dr. Ani memeriksa Leo: sehat!
print(leo._kesehatan)    # 100 (sudah dipulihkan dokter)
```

### 3.6 Fungsi di dalam `KebunBinatang` — `tambah_kandang()` dan `parade()`

```python
kebun = KebunBinatang("Gembira")
kebun.tambah_kandang(k1)
kebun.tambah_kandang(k2)

kebun.parade()
# Leo: Roar! (berjalan)
# Eli: Trumpet! (berjalan)
# Edo: Screech! (terbang)
# Ulo: Hiss! (melata)
```

### 3.7 Contoh alur lengkap minimal (copy-paste untuk praktikum)

```python
from kebun_binatang import Singa, Gajah, Kandang, KebunBinatang, DokterHewan

leo = Singa("Leo", 190)
eli = Gajah("Eli", 1200)

k1 = Kandang("Mamalia")
k1.tambah(leo)
k1.tambah(eli)

kebun = KebunBinatang("Gembira")
kebun.tambah_kandang(k1)

dok = DokterHewan("Dr. Ani")
print(dok.periksa(leo))
kebun.parade()
```

---

## 4. Cara Menambahkan Binatang Baru (Panduan Lengkap)

Prinsip: **pilih induk terdekat → override `suara()` (dan `gerak()` bila perlu) → buat instance → masukkan ke kandang → uji di parade**.

### 4.1 Tentukan induknya

| Kalau hewanmu... | Warisi | Yang perlu diisi |
|---|---|---|
| Menyusui / berbulu (singa, gajah, jerapah, monyet) | `Mamalia` | `suara()` saja (`gerak()` sudah `berjalan`) |
| Bersayap / bertelur (elang, merpati) | `Burung` | `suara()` saja (`gerak()` sudah `terbang`) |
| Bukan keduanya (ular, buaya, katak, ikan) | `Hewan` langsung | `suara()` + `gerak()` |
| Kasus khusus (pinguin: burung tapi tak terbang) | `Burung` + override `gerak()` | `suara()` + `gerak()` ulang |

### 4.2 Contoh 1 — Mamalia baru: `Jerapah` (paling mudah)

```python
class Jerapah(Mamalia):
    def suara(self):
        return "Humm!"
```

Pakai:

```python
jara = Jerapah("Jara", 800)
print(jara.suara())    # Humm!
print(jara.gerak())    # berjalan (warisan Mamalia, tanpa kode tambahan)
print(jara.menyusui()) # Jara menyusui anaknya (warisan Mamalia)
print(jara.info())     # Jara | berjalan | Humm! | 800kg

k1.tambah(jara)  # masukkan ke kandang yang sudah ada
kebun.parade()   # otomatis muncul: Jara: Humm! (berjalan)
```

### 4.3 Contoh 2 — Burung baru: `Merpati`

```python
class Merpati(Burung):
    def suara(self):
        return "Coo!"
```

```python
meri = Merpati("Meri", 0.5)
print(meri.suara())  # Coo!
print(meri.gerak())  # terbang (warisan Burung)
```

Kasus khusus — Pinguin (burung tapi tidak terbang), override `gerak()` juga:

```python
class Pinguin(Burung):
    def suara(self):
        return "Honk!"
    def gerak(self):
        return "berenang"  # menimpa "terbang" milik Burung
```

### 4.4 Contoh 3 — Langsung dari `Hewan`: `Buaya`

```python
class Buaya(Hewan):
    def suara(self):
        return "Growl!"
    def gerak(self):
        return "merangkak"
```

```python
baya = Buaya("Baya", 300)
print(baya.info())  # Baya | merangkak | Growl! | 300kg
```

### 4.5 Contoh 4 — Hewan dengan atribut tambahan (meniru `Gajah`)

Misal `Kanguru` butuh `panjang_ekor`:

```python
class Kanguru(Mamalia):
    def __init__(self, nama, berat, panjang_ekor=1.0):
        super().__init__(nama, berat)  # pinjam init induk
        self.panjang_ekor = panjang_ekor
    def suara(self):
        return "Chortle!"
```

```python
kang = Kanguru("Kang", 70, 1.2)
print(kang.suara(), "| ekor:", kang.panjang_ekor, "m")
```

### 4.6 Checklist setelah menambah hewan

1. `suara()` mengembalikan `str`, bukan `print` di dalam metode.
2. Jika warisi langsung `Hewan`, pastikan `gerak()` juga diisi (kalau lupa, hasilnya `None` karena `pass`).
3. Buat instance di Main / file ujimu, masukkan via `kandang.tambah(obj)`.
4. Jalankan `kebun.parade()` — hewan baru harus muncul tanpa mengubah kode `parade()` (bukti polimorfisme bekerja).
5. Uji enkapsulasi: `get_berat()` terbaca, `set_berat(-1)` ditolak.

### 4.7 Kesalahan umum praktikan

- Lupa `self`: `def suara():` → harus `def suara(self):`.
- Salah induk: `class Pinguin(Mamalia)` padahal pinguin burung → `menyusui()` jadi salah konsep.
- Mengisi `__init__` baru tanpa `super().__init__()` → `nama`/`__berat` hilang, `info()` error.
- Menulis `print` di dalam `suara()` lalu `parade()` mencetak `None` → selalu `return "..."`, bukan `print("...")`.

---

## 5. Bedah Konsep OOP (Inti Presentasi)

### A. Abstraksi dan Inheritance (Pewarisan)

`Hewan` adalah cetakan utama berisi ketentuan kosong (`pass`). Anak melengkapinya:

- Tingkat 1: `Mamalia(Hewan)` mengisi `gerak()` → `berjalan` + tambah `menyusui()`; `Burung(Hewan)` mengisi `gerak()` → `terbang`; `Ular(Hewan)` langsung mengisi `suara()` → `Hiss!` dan `gerak()` → `melata`.
- Tingkat 2: `Singa(Mamalia)` mengisi `suara()` → `Roar!` (gerak diwarisi); `Gajah(Mamalia)` → `Trumpet!`; `Elang(Burung)` → `Screech!`.

`Kandang`, `DokterHewan`, `KebunBinatang` bukan turunan `Hewan`, melainkan class pendukung berelasi asosiasi (wadah/pengelola).

### B. Polimorfisme (Satu Perintah, Perilaku Berbeda)

```python
for h in k.isi: print(f"{h.nama}: {h.suara()} ({h.gerak()})")
```

Perintah sama `h.suara()`, hasil beda: Singa → `Roar! (berjalan)`, Gajah → `Trumpet! (berjalan)`, Elang → `Screech! (terbang)`, Ular → `Hiss! (melata)`. Tanpa `if-else`. Inilah overriding.

### C. Enkapsulasi (Perlindungan Data)

```python
self.nama = nama          # public: bebas
self._kesehatan = 100     # protected: kalangan kebun saja
self.__berat = berat      # private: disembunyikan
```

- `eli.__berat` dari luar → error. Jalur resmi: `get_berat()` (baca) dan `set_berat(b)` (tulis, hanya jika `b > 0`).
- `h._kesehatan = 100` oleh dokter diperbolehkan karena dokter bagian internal sistem.

### D. Konstruktor dan Instance

Konstruktor (`__init__`) ada di `Hewan, Gajah, Kandang, DokterHewan, KebunBinatang`. Contoh khusus Gajah memakai `super().__init__(nama, berat)` lalu tambah `belalai`. Instance lahir di Main: `leo = Singa("Leo", 190)` — `Singa` cetakannya, `leo` wujud nyatanya.

---

## 6. Alur Kerja Program (Dari Main Hingga Selesai)

1. **Lahir:** Main membuat `leo, eli, edo, ulo`, `k1, k2`, `kebun`, `dok`.
2. **Isi kandang:** `k1.tambah(leo)` — Mamalia; `k2` menampung elang+ular.
3. **Himpun:** `kebun.tambah_kandang(k1)` — kandang masuk ke kebun.
4. **Periksa:** `dok.periksa(leo)` — kesehatan kembali 100.
5. **Demo warisan+enkapsulasi:** `eli.menyusui()` (warisan Mamalia); `get_berat()`/`set_berat()` (akses aman).
6. **Parade:** `kebun.parade()` — telusuri tiap kandang, panggil `h.suara()` berurutan → 4 suara beda (polimorfisme).

---

## 7. Naskah Presentasi / Script Praktikum (4 Orang, Formal)

Pembagian peran:

- **Orang 1 — Pembuka + Abstraksi & Inheritance:** salam, gambaran 10 class, bedah `Hewan`, `Mamalia`, `Burung`, `Singa/Gajah/Elang/Ular`.
- **Orang 2 — Polimorfisme + Enkapsulasi + Demo Parade:** jelaskan `parade()`, jalankan program, jelaskan `nama/_kesehatan/__berat` + `get_berat/set_berat`.
- **Orang 3 — Konstruktor, Instance & Cara Pakai + Cara Tambah Hewan Baru:** jelaskan `__init__`/`super()`, praktik `tambah()`, `periksa()`, lalu live coding `Jerapah`.
- **Orang 4 — Alur Program + Penutup + Tanya Jawab:** rangkum alur Main, kelemahan & pengembangan, penutup dan ajakan diskusi.

---

### Orang 1 — Pembuka + Abstraksi & Inheritance

> Assalamu'alaikum, kami mempresentasikan `kebun_binatang.py`: Sistem Kebun Binatang Gembira, 10 class tanpa library tambahan, yaitu `Hewan, Mamalia, Burung, Singa, Gajah, Elang, Ular, Kandang, DokterHewan, KebunBinatang`.
>
> Konsep pertama sesuai kode: `class Hewan` punya `__init__(self, nama, berat)` dengan `self.nama`, `self._kesehatan = 100`, `self.__berat`, plus `suara()`/`gerak()` berisi `pass`. `Mamalia(Hewan)` mengisi `gerak()` jadi `return "berjalan"` plus `menyusui()`, `Burung(Hewan)` jadi `return "terbang"`. Lalu `Singa(Mamalia)` isi `suara()` jadi `return "Roar!"`, `Gajah(Mamalia)` jadi `return "Trumpet!"`, `Elang(Burung)` jadi `return "Screech!"`, dan `Ular(Hewan)` langsung isi `return "Hiss!"` dan `return "melata"`. Lanjut ke rekan kedua untuk polimorfisme dan enkapsulasi.

### Orang 2 — Polimorfisme + Enkapsulasi + Demo

> Sesuai kode `KebunBinatang.parade()`: `for k in self.kandang: for h in k.isi: print(f"{h.nama}: {h.suara()} ({h.gerak()})")`. Satu perintah `h.suara()` + `h.gerak()`, tanpa `if-else`, menghasilkan empat baris persis seperti output: `Leo: Roar! (berjalan)`, `Eli: Trumpet! (berjalan)`, `Edo: Screech! (terbang)`, `Ulo: Hiss! (melata)`. [Jalankan `python3 kebun_binatang.py` dan tunjukkan blok `--- Parade Suara ---`.]
>
> Enkapsulasi sesuai kode `Hewan`: `nama` public bebas, `_kesehatan = 100` protected hanya diubah dokter via `h._kesehatan = 100` di `periksa()` yang me-return `f"{self.nama} memeriksa {h.nama}: sehat!"`, dan `__berat` private hanya via `get_berat()`/`set_berat(b)` dengan `if b > 0`. Buktinya di Main: `Berat Eli: 1200 kg` lalu `set_berat(1250)` jadi `Berat baru: 1250 kg`. Lanjut ke rekan ketiga untuk konstruktor dan cara pakai.

### Orang 3 — Konstruktor + Cara Pakai + Tambah Hewan Baru

> Semua objek lahir di `if __name__ == "__main__":` persis seperti kode: `leo = Singa("Leo", 190)`, `eli = Gajah("Eli", 1200, 1.8)`, `edo = Elang("Edo", 6)`, `ulo = Ular("Ulo", 8)`. Khusus `Gajah.__init__(self, nama, berat, belalai=2)` memanggil `super().__init__(nama, berat)` lalu `self.belalai`, sehingga `print(eli.menyusui(), "| belalai:", eli.belalai, "m")` keluar `Eli menyusui anaknya | belalai: 1.8 m`. Cara pakai sesuai kode: `k1 = Kandang("Mamalia"); k1.tambah(leo); k1.tambah(eli)`, `k2 = Kandang("Lainnya"); k2.tambah(edo); k2.tambah(ulo)`, `kebun = KebunBinatang("Gembira"); kebun.tambah_kandang(k1); kebun.tambah_kandang(k2)`, `dok = DokterHewan("Dr. Ani"); print(dok.periksa(leo))` keluar `Dr. Ani memeriksa Leo: sehat!`.
>
> Tambah hewan baru (contoh di luar kode, pola sama): `class Jerapah(Mamalia): def suara(self): return "Humm!"`, lalu `jara = Jerapah("Jara", 800); k1.tambah(jara)`, otomatis ikut `parade()` jadi `Jara: Humm! (berjalan)` tanpa ubah `parade()`, plus tetap bisa `jara.menyusui()` dan `jara.info()` format `nama | gerak | suara | beratkg`. Alur lengkap ditutup rekan keempat.

### Orang 4 — Alur Program + Penutup

> Alur sesuai urutan Main baris 81-96: lahirkan 4 hewan → isi `k1`/`k2` via `tambah()` → himpun via `tambah_kandang()` → `print(dok.periksa(leo))` → `print(eli.menyusui()...)` → `print("Berat Eli:", eli.get_berat()...)` + `set_berat(1250)` → `print("--- Parade Suara ---"); kebun.parade()`. Kelemahan sesuai kode: induk masih `pass` (belum `ABC`/`abstractmethod`), belum ada `hapus()` di `Kandang`, validasi hanya `b > 0`.
>
> Demikian presentasi kelompok kami, kami siap menjawab pertanyaan. Wassalamu'alaikum warahmatullahi wabarakatuh.

---

## 8. Tips Presentasi (Tiga Poin Utama)

1. **Awali dari induk.** Tegaskan `Hewan` hanya berisi ketentuan kosong (`pass`). Tunjukkan `Singa/Gajah/Elang/Ular` mengisinya berbeda. Satu penjelasan mencakup Abstraksi + Inheritance.
2. **Demo parade langsung.** Jalankan program, tunjukkan 4 baris output. Sampaikan perintahnya sama (`h.suara()`), hasilnya beda. Demo lebih meyakinkan daripada teori panjang.
3. **Tekankan enkapsulasi + kelahiran objek.** `__berat` dikunci, hanya via `set_berat()` tervalidasi. Tutup dengan `leo = Singa("Leo", 190)` sebagai bukti konstruktor/instance. Bonus: live tambah `Jerapah` (5 baris) lalu `parade()` ulang tanpa edit `parade()`.

---

## 9. Prediksi Pertanyaan Kritis Dosen Beserta Jawaban

**1. Mengapa class Hewan tidak dibuat objeknya secara langsung?**
Karena ia cetakan abstrak berisi ketentuan kosong (`pass`). Ia menetapkan setiap hewan wajib punya suara dan gerak, pelaksanaannya diserahkan ke anak agar tidak seragam.

**2. Mengapa Singa bisa punya nama dan berat padahal tidak punya `__init__`?**
Karena mewarisi konstruktor `Mamalia → Hewan`. Pewarisan memungkinkan pakai konstruktor induk tanpa tulis ulang.

**3. Mengapa Gajah mendefinisikan `__init__` lagi dan memakai `super().__init__()`?**
Karena butuh atribut tambahan `belalai`. `super().__init__()` meminjam inisialisasi induk, lalu tambah atribut khusus.

**4. Apa beda `nama`, `_kesehatan`, `__berat`?**
Tingkatan akses: public bebas, protected (satu underscore) hanya kalangan kebun, private (dua underscore) hanya via getter/setter.

**5. Jika `__berat` private, mengapa `info()` bisa membacanya?**
Karena `info()` ada di dalam class yang sama. Private melarang akses dari luar, bukan dari dalam.

**6. Apakah `DokterHewan` yang mengubah `_kesehatan` melanggar enkapsulasi?**
Tidak. Single underscore adalah konvensi protected untuk internal sistem. Dokter termasuk internal, jadi sesuai peruntukan.

**7. Di mana bukti konkret polimorfisme?**
Di `parade()`. `h.suara()` ditulis sekali, menghasilkan 4 keluaran beda karena overriding. Tanpa `if-else`.

**8. Apa yang terjadi jika `Ular` tidak override `suara()`?**
Mewarisi metode kosong induk (`pass`) → mengembalikan `None` / tidak bersuara. Ini menegaskan pentingnya overriding.

**9. Apakah relasi KebunBinatang–Kandang–Hewan termasuk pewarisan?**
Bukan. Itu asosiasi/komposisi (kepemilikan wadah). Kandang punya daftar hewan, kebun punya daftar kandang — kerja sama antarobjek, bukan pewarisan sifat.

**10. Apa kelemahan rancangan ini dan pengembangannya?**
Masih dasar: induk hanya pakai `pass` (belum memaksa anak mengisi), belum ada hapus hewan dari kandang, validasi terbatas. Pengembangan: pakai `ABC` + `@abstractmethod` untuk kontrak ketat, tambah `hapus()`, `cari()`, validasi umur/berat, dan persistensi data.
