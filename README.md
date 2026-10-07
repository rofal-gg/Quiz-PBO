# Sistem Manajemen Kafe Belbel Cafe & Bakery — OOP + UML + JSON

Program pendataan karyawan kafe yang bermanfaat nyata: tambah karyawan,
catat gaji float tervalidasi, nilai kinerja oleh manajer, atur shift,
tampilkan operasional dan laporan, serta simpan otomatis ke JSON agar
tidak hilang saat program ditutup. Ditulis dengan sintaks pemula:
hanya `import json`, tanpa dekorator, tanpa sintaks lanjutan.

File utama: `kafe.py` (11 class) | Data: `data/karyawan.json` |
Model: `docs/UML-kafe.md` | Arsip teman: `arsip/code_baru.py` (ber-bug, jangan dikumpulkan)

## Daftar Isi

1. [Pembukaan](#1-pembukaan)
2. [Analisis Kasus dan Manfaat Dunia Nyata](#2-analisis-kasus-dan-manfaat-dunia-nyata)
3. [Model UML dan Relasi](#3-model-uml-dan-relasi)
4. [Cara Menjalankan dan Memakai Menu](#4-cara-menjalankan-dan-memakai-menu)
5. [Struktur JSON](#5-struktur-json)
6. [Penjelasan Kode per Class](#6-penjelasan-kode-per-class)
7. [Panduan Lengkap Sintaks Class untuk Pemula](#7-panduan-lengkap-sintaks-class-untuk-pemula)
8. [Tata Cara Menambah Peran Baru](#8-tata-cara-menambah-peran-baru)
9. [Bedah Konsep OOP](#9-bedah-konsep-oop)
10. [Bukti Keselarasan Model vs Program](#10-bukti-keselarasan-model-vs-program)
11. [Alur Program](#11-alur-program)
12. [Pembelajaran Bertahap](#12-pembelajaran-bertahap)
13. [Naskah Presentasi 4 Orang](#13-naskah-presentasi-4-orang)
14. [Tips Presentasi](#14-tips-presentasi)
15. [Prediksi Pertanyaan Dosen](#15-prediksi-pertanyaan-dosen)

---

## 1. Pembukaan

Proyek ini merupakan simulasi sistem informasi kafe yang dimodelkan
dengan Pemrograman Berorientasi Objek menggunakan bahasa Python.
Apabila diibaratkan dalam kehidupan nyata, kafe memiliki pegawai
dengan peran berbeda (Waiter, Kasir, Baker, Barista), shift kerja
sebagai wadah (Pagi, Sore), manajer sebagai penilai, sistem kafe
sebagai koordinator, dan database JSON sebagai arsip.

Pengguna tidak mencatat di kertas, melainkan mencetak objek nyata
seperti `Waiter("Andi","W01",3000000.0)`, memasukkannya ke shift,
menilainya, lalu menampilkan operasional. Satu perintah operasional
menampilkan empat aktivitas berbeda secara otomatis.

Kesebelas class: `Pegawai, FrontOfHouse, BackOfHouse, Waiter, Kasir,
Baker, Barista, ShiftKerja, StoreManager, SistemCafe, DatabaseJSON`.

## 2. Analisis Kasus dan Manfaat Dunia Nyata

Masalah nyata kafe kecil: data karyawan tersebar, gaji lupa dicatat,
penilaian kinerja tidak terdokumentasi, jadwal shift tertukar, data
hilang saat pergantian shift. Solusi program ini: tambah karyawan
lewat ketikan dengan validasi (ID unik, gaji angka positif float),
set gaji ulang via `set_gaji()`, evaluasi manajer (+25 poin per nilai,
awal 0, menyentuh 100 langsung dipecat dan dihapus dari shift),
laporan (termasuk laporan pemecatan) dan operasional sebagai rekap
harian, simpan ke `data/karyawan.json` sehingga besok dibuka tetap ada.

Contoh manfaat yang sudah teruji: tambah Eka (W02) ke Pagi, tolak
duplikat W02, tolak gaji huruf, nilai Andi (W01) 0→25→50→75→100
lalu DIPECAT tgl 07-10-2026 dan tampil di laporan pemecatan,
operasional bertambah satu baris tanpa mengubah kode
`operasional()`.

## 3. Model UML dan Relasi

Diagram lengkap juga di `docs/UML-kafe.md`. Penomoran sejajar laporan:
Gambar 3.1 Use Case, Gambar 3.2 Class, Gambar 3.3 Activity,
Gambar 3.4 Sequence.

### 3.1 Use Case Diagram (Gambar 3.1)

```mermaid
flowchart LR
    PG([Pengguna])
    MG([StoreManager<br/>Pak Anton])
    U1([Menu 1<br/>Tambah Pegawai])
    U2([Menu 2<br/>Lihat Laporan])
    U3([Menu 3<br/>Evaluasi +25 poin])
    U4([Pecat saat poin 100])
    U5([Menu 4<br/>Lihat Operasional])
    U6([Menu 5<br/>Kelola Shift])
    U7([Menu 6<br/>Ubah Gaji])
    U8([Menu 7<br/>Simpan dan Keluar])
    UB([Buat Shift Baru<br/>otomatis])
    PG --> U1
    PG --> U2
    PG --> U3
    PG --> U5
    PG --> U6
    PG --> U7
    PG --> U8
    MG --> U3
    U3 -.->|include, poin = 100| U4
    U1 -.->|extend, nama shift baru| UB
    U6 -.->|pindah atau buat baru| UB
```

Pengguna memakai tujuh menu, sedangkan StoreManager hanya terlibat
pada evaluasi dan pemecatan. Evaluasi berelasi *include* ke pecat
(otomatis saat poin mencapai 100 dan langsung meminta tanggal),
sedangkan tambah dan kelola shift berelasi *extend* ke buat shift baru
(shift otomatis dibuat bila nama belum ada).

### 3.2 Class Diagram (Gambar 3.2)

```mermaid
classDiagram
    class Pegawai {
        <<abstract>>
        +String nama
        +String id_pegawai
        #int poin
        -float gaji
        +__init__(nama, id_pegawai, gaji)
        +aktivitas() String
        +get_gaji() float
        +set_gaji(nominal) bool
        +get_poin() int
        +info() String
        +ke_dict() dict
    }
    class FrontOfHouse {
        +layani() String
    }
    class BackOfHouse {
        +layani() String
    }
    class Waiter {
        +aktivitas() String
    }
    class Kasir {
        +aktivitas() String
    }
    class Baker {
        +String spesialisasi
        +__init__(nama, id_pegawai, gaji, spesialisasi)
        +aktivitas() String
        +ke_dict() dict
    }
    class Barista {
        +String spesialisasi
        +__init__(nama, id_pegawai, gaji, spesialisasi)
        +aktivitas() String
        +ke_dict() dict
    }
    class ShiftKerja {
        +String nama_shift
        +List daftar
        +__init__(nama_shift)
        +tambah(p) void
        +hapus(id_pegawai) bool
        +cari(id_pegawai) Pegawai
        +ke_dict() dict
    }
    class StoreManager {
        +String nama
        +__init__(nama)
        +evaluasi(p) String
        +pecat(cafe, id_pegawai, tanggal) String
    }
    class SistemCafe {
        +String nama_cafe
        +List jadwal
        +List riwayat_pecat
        +__init__(nama_cafe)
        +atur_shift(s) void
        +cari_shift(nama) ShiftKerja
        +cari_pegawai(id_pegawai) Pegawai
        +operasional() void
        +laporan() void
    }
    class DatabaseJSON {
        +String path
        +__init__(path)
        +simpan(cafe) void
        +muat(cafe) bool
    }

    Pegawai <|-- FrontOfHouse : Generalization
    Pegawai <|-- BackOfHouse : Generalization
    FrontOfHouse <|-- Waiter : Generalization
    FrontOfHouse <|-- Kasir : Generalization
    BackOfHouse <|-- Baker : Generalization
    BackOfHouse <|-- Barista : Generalization
    SistemCafe *-- ShiftKerja : composition 1..*
    ShiftKerja o-- Pegawai : aggregation 0..*
    StoreManager ..> Pegawai : dependency menilai
    StoreManager ..> SistemCafe : dependency memecat
    SistemCafe --> StoreManager : association memakai
    DatabaseJSON ..> SistemCafe : dependency simpan-muat
    DatabaseJSON ..> ShiftKerja : dependency bangun-ulang

    note for Pegawai "Kontrak kosong:\naktivitas() = pass.\nAnak wajib override.\nVersi pemula tanpa ABC."
    note for StoreManager "Aturan poin:\nawal 0, +25 per evaluasi.\n100 = DIPECAT,\ndihapus + arsip."
    note for SistemCafe "laporan() = tabel aktif\n+ bagian pemecatan.\npecat tersimpan JSON."
```

Makna: Generalization 6 panah (warisi tanpa tulis ulang),
Composition cafe-shift (`self.jadwal`, `atur_shift`),
Aggregation shift-pegawai (`self.daftar`, `tambah`),
Dependency manajer-pegawai (`evaluasi` +25 dan `pecat` yang menghapus
via `hapus()` serta mencatat ke `riwayat_pecat`, tampil gabung di
`laporan()`),
Dependency JSON (`simpan/muat`, kunci `pecat` ikut tersimpan).
Fungsi bebas pembantu: `buat_pegawai()` (bangun ulang berdasar kunci
`peran`), `buat_shift()`, `contoh_awal()`, `tanya_angka()`, `menu()`.

Abstraksi memakai `pass` agar mudah dipahami pemula (kontrak kosong,
bukan `ABC` ketat). Konsekuensinya induk masih bisa dibuat langsung
dan hasilnya `None` — ini keterbatasan yang disengaja dan menjadi
bahan Q&A, bukan bug tersembunyi.

### 3.3 Activity Diagram (Gambar 3.3)

```mermaid
flowchart TD
    S([Mulai: python kafe.py]) --> M[muat data/karyawan.json]
    M --> C{File ada dan valid?}
    C -->|Tidak| A[contoh_awal lalu simpan]
    C -->|Ya| L[Tampil laporan dan operasional awal]
    A --> L
    L --> MN{Pilih menu 1-7}
    MN -->|1 Tambah| V1{ID unik dan gaji positif?}
    V1 -->|Tidak| T1[Tolak dengan pesan] --> MN
    V1 -->|Ya| T2[ShiftKerja.tambah] --> MN
    MN -->|2 Laporan| LP[laporan dan riwayat pecat] --> MN
    MN -->|3 Evaluasi| EV[StoreManager.evaluasi +25]
    EV --> P{Poin = 100?}
    P -->|Tidak| MN
    P -->|Ya| PC[Input tanggal, pecat: hapus + arsip] --> MN
    MN -->|4 Operasional| OP[Loop p.aktivitas] --> MN
    MN -->|5 Shift| SH[Buat baru, hapus kosong, pindah] --> MN
    MN -->|6 Gaji| GJ[set_gaji tervalidasi] --> MN
    MN -->|7 Simpan dan Keluar| SV[DatabaseJSON.simpan] --> E([Selesai])
```

Alur berputar pada menu hingga pengguna memilih 7. Setiap masukan
tidak valid ditolak dengan pesan lalu kembali ke menu. Evaluasi yang
mencapai poin 100 langsung beralih ke pemecatan: meminta tanggal,
menghapus pegawai dari shift, dan mencatatnya ke `riwayat_pecat`.

### 3.4 Sequence Diagram (Gambar 3.4)

```mermaid
sequenceDiagram
    actor PG as Pengguna
    participant MN as menu()
    participant CF as cafe:SistemCafe
    participant SH as shift:ShiftKerja
    participant MG as mgr:StoreManager
    participant DB as db:DatabaseJSON
    participant JS as karyawan.json
    PG->>MN: 1 Tambah Eka W02 ke Pagi
    MN->>CF: cari_pegawai(W02)
    CF->>SH: cari(W02)
    SH-->>MN: None, ID bebas
    MN->>SH: tambah(Eka)
    PG->>MN: 3 Evaluasi W01
    MN->>CF: cari_pegawai(W01)
    CF-->>MN: Andi
    loop 4 kali evaluasi
        MN->>MG: evaluasi(Andi)
        MG->>MG: poin +25
    end
    MG-->>MN: poin=100 DIPECAT
    MN->>PG: minta tanggal pecat
    PG-->>MN: 07-10-2026
    MN->>MG: pecat(cafe, W01, tanggal)
    MG->>SH: hapus(W01)
    MG->>CF: riwayat_pecat.append(data)
    MN->>CF: laporan()
    CF-->>MN: tabel aktif + laporan pemecatan
    MN->>DB: simpan(cafe)
    DB->>JS: json.dump(nama_cafe, shift, pecat)
    PG->>MN: 7 Simpan dan Keluar
```

Skenario mencakup tiga bukti utama: tambah dengan cek ID unik,
evaluasi bertahap 0→25→50→75→100 hingga DIPECAT beserta tanggal,
dan simpan JSON yang mempertahankan riwayat pemecatan.

## 4. Cara Menjalankan dan Memakai Menu

```bash
python kafe.py
```

Menu:

```
1 Tambah | 2 Laporan | 3 Evaluasi | 4 Operasional | 5 Shift | 6 Gaji | 7 Simpan+Keluar
```

Tata cara: pilih 1 isi Nama, ID unik, Gaji angka positif, peran 1-4
(Barista/Baker ditanya spesialisasi), shift tujuan (baru otomatis
dibuat). Pilih 2 untuk tabel + laporan pemecatan, 3 isi ID untuk
+25 poin (100 langsung minta tanggal dan dipecat), 4 parade aktivitas,
5 kelola shift (buat baru, hapus kosong, pindah pegawai),
6 ubah gaji via `set_gaji()`, 7 simpan dan keluar.
Wajib keluar via 5 agar tersimpan (termasuk riwayat pecat).
Data awal otomatis dibuat bila JSON belum ada.

## 5. Struktur JSON

`data/karyawan.json`:

```json
{
  "nama_cafe": "Belbel Cafe",
  "shift": [{"nama": "Pagi", "isi": [
    {"peran": "Waiter", "nama": "Andi", "id": "W01", "gaji": 3000000.0, "poin": 0},
    {"peran": "Baker", "nama": "Cici", "id": "B01", "gaji": 4000000.0, "poin": 0, "spesialisasi": "Pastry"}
  ]}],
  "pecat": []
}
```

`peran` wajib agar `buat_pegawai()` tahu membuat class yang tepat.
Gaji diambil via `get_gaji()` karena `__gaji` private. Data asing
(`peran` tak dikenal) diberi peringatan dan dianggap Waiter agar
tidak diam-diam salah.

## 6. Penjelasan Kode per Class

### 6.1 `Pegawai` — induk abstrak
`__init__(nama, id_pegawai, gaji)` mengisi `nama/id` public,
`_poin=0` protected (menyentuh 100 = dipecat), `__gaji` private.
`aktivitas(): pass` sengaja kosong sebagai kontrak.
`get_gaji/set_gaji(>0)`, `get_poin`, `info()`, `ke_dict()` untuk JSON.

### 6.2 `FrontOfHouse`, `BackOfHouse`
`FrontOfHouse(Pegawai)` mengisi `layani()` ramah,
`BackOfHouse(Pegawai)` mengisi `layani()` dapur. Diwarisi ke anak.

### 6.3 `Waiter, Kasir, Baker, Barista`
Masing-masing mengisi `aktivitas()` berbeda. `Baker` dan `Barista`
contoh `__init__+super().__init__+spesialisasi` dan override `ke_dict`.
`Waiter("Andi","W01",3000000.0)` bisa walau tanpa `__init__`
karena warisan.

### 6.4 `ShiftKerja`, `StoreManager`, `SistemCafe`, `DatabaseJSON`
`ShiftKerja`: `daftar=[]`, `tambah(p)`, `hapus(id)` untuk pemecatan,
`cari(id)`, `ke_dict()`.
`StoreManager`: `evaluasi(p)` +25 hingga 100 (DIPECAT),
`pecat(cafe,id,tanggal)` menghapus dari shift dan mencatat ke
`riwayat_pecat`.
`SistemCafe`: `jadwal=[]`, `riwayat_pecat=[]`, `atur_shift`,
`cari_shift/pegawai`, `operasional()` loop `p.aktivitas()`,
`laporan()` tabel + bagian pemecatan.
`DatabaseJSON(path)`: `simpan` dump (termasuk kunci `pecat`),
`muat` load, gagal False.
`DatabaseJSON(path)`: `simpan` dump, `muat` load, gagal False.
Tanpa dekorator, metode biasa. Fungsi bebas: `buat_pegawai`,
`buat_shift`, `contoh_awal`, `tanya_angka`, `menu`.

## 7. Panduan Lengkap Sintaks Class untuk Pemula

Rumus dasar: `class Nama:` menjorok 4 spasi. Nama PascalCase.
`def __init__(self,...):` otomatis jalan saat
`andi = Waiter("Andi","W01",3000000.0)`. `self` artinya objek ini
dan wajib parameter pertama. `self.nama=nama` menempelkan data.
Warisan: `class Anak(Induk):`, contoh `class Waiter(FrontOfHouse):`.
`super().__init__(...)` meminjam init induk sebelum tambah atribut
baru (contoh `Baker`). Method: `def nama(self):` + `return`,
dipanggil `andi.aktivitas()`. `pass` artinya kosongkan.
Komposisi: `self.daftar=[]` + `tambah(p)` menampung objek lain.
Empat langkah pakai class: definisikan → wariskan bila perlu →
lahirkan di Main/menu → gunakan (`p.aktivitas()`, `get_gaji()`).

## 8. Tata Cara Menambah Peran Baru

Pilih induk terdekat: pelayan → `FrontOfHouse`, dapur →
`BackOfHouse`. Override `aktivitas()` (dan `layani()` bila perlu),
buat instance, masukkan via `shift.tambah()`, uji di operasional.
Contoh: `class CleaningService(BackOfHouse): def aktivitas(self):
return "Membersihkan meja."` lalu otomatis ikut operasional.
Bila butuh atribut baru, tiru `Baker` (`super` + `ke_dict`).
Checklist: `return` bukan `print`, ID unik, uji `get/set`,
pastikan muncul di operasional tanpa ubah `operasional()`.
Kesalahan umum: lupa `self`, salah induk, `__init__` tanpa `super`.

## 9. Bedah Konsep OOP

Abstraksi: `Pegawai` kontrak kosong. Inheritance:
`Waiter(FrontOfHouse(Pegawai))` warisi nama/id/gaji/poin.
Polimorfisme: satu `p.aktivitas()` → antar/bayar/panggang/seduh,
satu `p.layani()` → ramah/dapur, tanpa `if` di operasional.
Enkapsulasi: `__gaji` via getter/setter, `_poin` via manajer.
Konstruktor/Instance: `__init__` nilai awal,
`andi=Waiter(...)` wujud nyata di Main/menu.

## 10. Bukti Keselarasan Model vs Program

| UML | Kode `kafe.py` | Uji |
|---|---|---|
| 11 class | 11 nama sama, 0 dekorator | AST cocok |
| Abstract `pass` | `def aktivitas: pass` | Lupa override → `None` |
| `Baker/Barista+super+spesialisasi` | `super().__init__`, override `ke_dict` | JSON simpan spesialisasi, reload utuh |
| Composition/Aggregation | `jadwal/atur_shift`, `daftar/tambah/hapus` | Eka masuk Pagi, Andi dipecat terhapus |
| Pemecatan | `evaluasi+25`, `pecat`, `riwayat_pecat`, laporan gabung | 0→100 DIPECAT, hilang dari shift, muncul di laporan |
| Validasi | `set_gaji>0`, ID unik, `tanya_angka` | -5/huruf/duplikat/kosong ditolak |
| JSON round-trip | `simpan/muat`, `buat_pegawai`, kunci `pecat` | Tutup-buka cocok, riwayat awet |
| Polimorfisme | `operasional()` loop | Tambah peran tanpa ubah metode |

Perbaikan dari `arsip/code_baru.py`: tambah `self.id_pegawai`
(crash diperbaiki), buang dekorator/`os`/`with`, rapikan nama dan
path, gaji float, muat umum semua shift, ID unik, poin dibatasi.

## 11. Alur Program

`muat(data/karyawan.json)` → bila gagal `contoh_awal+simpan` →
`laporan+operasional` awal → `menu()` loop 1-7 → keluar `simpan()`.
Tambah/timbang/nilai langsung bisa dicek via laporan/operasional.

## 12. Pembelajaran Bertahap

1. Bedakan class vs objek (`Waiter` vs `andi`).
2. Telusuri `__init__` dan `super()` di `Baker`.
3. Uji enkapsulasi (`get/set_gaji`, manajer).
4. Telusuri rantai `Pegawai→Front→Waiter`.
5. Jalankan operasional, amati satu perintah banyak hasil.
6. Tambah peran baru dan simpan-muat JSON.

## 13. Naskah Presentasi 4 Orang

Pembagian: 1 pembuka+UML+abstraksi/inheritance, 2 polimorfisme+demo,
3 enkapsulasi+konstruktor+menu/JSON, 4 bukti+alur+penutup.

> Assalamu'alaikum. Kami mempresentasikan `kafe.py`: Sistem Manajemen
> Belbel Cafe, 11 class, hanya `import json`, tanpa dekorator.
> Masalah nyata: data kertas hilang. Solusi: input shift, gaji float
> tervalidasi, evaluasi manajer, simpan JSON.
> Induk `Pegawai` berisi kontrak kosong `pass`, dilengkapi anak:
> Front ramah, Back dapur, Waiter antar, Kasir bayar, Baker panggang
> plus spesialisasi via `super`, Barista seduh plus spesialisasi.
> Satu perintah `p.aktivitas()` di `operasional()` menghasilkan empat
> keluaran beda tanpa `if`. Gaji private hanya via getter/setter,
> poin protected via manajer (awal 0, +25, 100 = dipecat dan dihapus
> dari shift, tercatat di laporan pemecatan). Objek lahir di Main/menu,
> contoh `andi=Waiter(...)`. Alur: muat, laporan, menu, simpan.
> Bukti: tambah Eka, tolak duplikat, evaluasi Andi 0→100 DIPECAT
> tgl 07-10-2026, JSON awet termasuk riwayat.
> Kelemahan: `pass` belum memaksa. Siap tanya jawab.
> Wassalamu'alaikum.

Orang 1 baca paragraf 1-2 + tunjuk UML. Orang 2 tunjuk operasional
dan jalankan menu 4. Orang 3 tunjuk `set_gaji` dan demo menu 1-3-5-6-7
plus buka JSON. Orang 4 tunjuk tabel bukti dan tutup.

## 14. Tips Presentasi

Awali masalah kafe nyata, demo operasional langsung, tunjukkan
penolakan (duplikat, huruf, negatif) dan bukti JSON tetap ada.
Jangan baca semua baris, tunjuk 3 titik: `pass`, `p.aktivitas()`,
`set_gaji`.

## 15. Prediksi Pertanyaan Dosen

1. Kenapa Pegawai tidak dibuat langsung? Kontrak kosong agar tidak seragam.
2. Kenapa Waiter tanpa init punya nama? Warisan `Front→Pegawai`.
3. Kenapa Baker/Barista pakai `super()`? Butuh `spesialisasi`.
4. Beda nama/id/poin/gaji? public/protected/private.
5. Manajer ubah protected melanggar? Tidak, internal.
6. Bukti poli? Operasional + tambah tanpa ubah metode.
7. Lupa override? Warisi `pass` → `None`.
8. Shift-pegawai warisan? Bukan, wadah.
9. Aturan pecat? Poin awal 0, +25 per evaluasi, 100 = DIPECAT,
   dihapus via `hapus()` dan tampil di laporan pemecatan + JSON.
10. Bug teman apa? Lupa id, dekorator, validasi, hardcode shift.
11. Kelemahan? `pass` belum memaksa; lanjut ABC + fitur gaji.
