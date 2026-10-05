# Proyek Pemrograman Berorientasi Objek: Sistem Kebun Binatang Gembira

## 1. Pembukaan (Elevator Pitch)

Proyek ini merupakan simulasi sederhana dari sistem pengelolaan kebun binatang yang dimodelkan dengan pendekatan Pemrograman Berorientasi Objek (PBO) menggunakan bahasa Python.

Apabila diibaratkan dalam kehidupan nyata, sistem ini terdiri atas pemilik kebun yang mengelola seluruh area, kandang sebagai tempat penampung, hewan sebagai penghuni, serta dokter hewan sebagai tenaga perawat. Pengguna tidak mengatur setiap hewan secara manual, melainkan membuat satu cetakan umum, kemudian mencetak objek-objek nyata seperti Singa bernama Leo, Gajah bernama Eli, Elang bernama Edo, dan Ular bernama Ulo. Selanjutnya, objek-objek tersebut ditempatkan ke dalam kandang, kandang dihimpun ke dalam kebun, dan kebun menyelenggarakan parade suara sebagai bentuk interaksi kolektif.

Dengan demikian, proyek ini mendemonstrasikan bagaimana objek-objek yang berbeda dapat saling bekerja sama dalam satu sistem yang terstruktur, modular, dan mudah dikembangkan.

Kesepuluh class dalam proyek ini adalah: `Hewan, Mamalia, Burung, Singa, Gajah, Elang, Ular, Kandang, DokterHewan, KebunBinatang`.

---

## 2. Bedah Konsep OOP (Inti Presentasi)

### A. Abstraksi dan Inheritance (Pewarisan)

**Class induk: `class Hewan`**

Class `Hewan` berperan sebagai cetakan utama atau induk abstrak. Class ini tidak dimaksudkan untuk dibuat objeknya secara langsung, melainkan sebagai pedoman bagi seluruh class turunannya:

```python
class Hewan:
    def suara(self):
        pass  # kosong, anak wajib isi sendiri
    def gerak(self):
        pass  # kosong, anak wajib isi sendiri
```

Pernyataan `pass` berarti metode tersebut sengaja dikosongkan. Class induk hanya menetapkan ketentuan bahwa setiap hewan wajib memiliki kemampuan bersuara dan bergerak, sedangkan rincian pelaksanaannya diserahkan kepada class anak.

**Class turunan (inheritance):**

1. Tingkat pertama:
   - `class Mamalia(Hewan)` mengisi `gerak()` menjadi `berjalan` dan menambahkan `menyusui()`.
   - `class Burung(Hewan)` mengisi `gerak()` menjadi `terbang`.
   - `class Ular(Hewan)` mengisi langsung `suara()` menjadi `Hiss!` dan `gerak()` menjadi `melata`.

2. Tingkat kedua:
   - `class Singa(Mamalia)` mengisi `suara()` menjadi `Roar!`, sedangkan cara bergerak diwarisi dari `Mamalia`.
   - `class Gajah(Mamalia)` mengisi `suara()` menjadi `Trumpet!`.
   - `class Elang(Burung)` mengisi `suara()` menjadi `Screech!`.

Dengan pewarisan ini, class anak tidak perlu menulis ulang kode yang sudah dimiliki induknya. Sebagai contoh, `Singa` tidak perlu mendefinisikan ulang metode `gerak()`, karena telah mewarisinya dari `Mamalia`.

Class `Kandang`, `DokterHewan`, dan `KebunBinatang` bukan merupakan turunan `Hewan`, melainkan class pendukung yang berelasi secara asosiatif (wadah dan pengelola).

### B. Polimorfisme (Satu Perintah, Perilaku Berbeda)

Bukti polimorfisme terdapat pada metode `parade()` milik class `KebunBinatang`:

```python
for h in k.isi: print(f"{h.nama}: {h.suara()} ({h.gerak()})")
```

Perintah yang dieksekusi sama, yaitu `h.suara()`, namun hasil yang diperoleh berbeda sesuai dengan jenis objeknya:

- Objek `Singa` menghasilkan `Roar! (berjalan)`
- Objek `Gajah` menghasilkan `Trumpet! (berjalan)`
- Objek `Elang` menghasilkan `Screech! (terbang)`
- Objek `Ular` menghasilkan `Hiss! (melata)`

Dengan demikian, satu instruksi yang sama mampu menghasilkan perilaku yang beragam tanpa memerlukan percabangan `if-else`. Inilah esensi polimorfisme melalui overriding metode.

### C. Enkapsulasi (Perlindungan Data)

Di dalam class `Hewan` terdapat tiga tingkat akses data, sesuai dengan materi enkapsulasi:

```python
self.nama = nama          # public: dapat diakses dari mana saja
self._kesehatan = 100     # protected: sebaiknya hanya diakses oleh kalangan kebun
self.__berat = berat      # private: disembunyikan, tidak dapat diakses langsung
```

Data yang dilindungi secara ketat adalah `__berat`. Akses langsung seperti `eli.__berat` dari luar class akan menghasilkan kesalahan. Oleh karena itu, disediakan metode getter dan setter sebagai jalur akses yang aman:

```python
def get_berat(self): return self.__berat
def set_berat(self, b):
    if b > 0: self.__berat = b
```

Metode `get_berat()` digunakan untuk membaca nilai, sedangkan `set_berat()` digunakan untuk mengubah nilai dengan validasi bahwa berat harus bernilai positif. Dengan mekanisme ini, integritas data tetap terjaga.

Atribut `_kesehatan` bersifat protected. Sebagai contoh, metode `DokterHewan.periksa()` diperkenankan mengubah `h._kesehatan = 100` karena dokter merupakan bagian dari sistem kebun. Pihak luar diimbau untuk tidak mengubahnya secara langsung.

### D. Konstruktor dan Instance (Pembuatan Objek)

**Konstruktor (`__init__`)** berfungsi untuk memberikan nilai awal pada saat objek dibuat. Konstruktor terdapat pada `Hewan, Gajah, Kandang, DokterHewan, dan KebunBinatang`. Contoh dasar:

```python
def __init__(self, nama, berat):
    self.nama = nama
    self.__berat = berat
```

Contoh khusus pada `Gajah` yang memerlukan atribut tambahan:

```python
def __init__(self, nama, berat, belalai=2):
    super().__init__(nama, berat)
    self.belalai = belalai
```

Pernyataan `super().__init__()` berarti meminjam proses inisialisasi milik induk, kemudian menambahkan atribut `belalai` secara khusus.

**Instance (objek nyata)** dibuat pada bagian `Main`, yaitu blok `if __name__ == "__main__":`:

```python
leo = Singa("Leo", 190)
eli = Gajah("Eli", 1200, 1.8)
edo = Elang("Edo", 6)
ulo = Ular("Ulo", 8)

k1 = Kandang("Mamalia")
kebun = KebunBinatang("Gembira")
dok = DokterHewan("Dr. Ani")
```

Class `Singa` merupakan cetakan, sedangkan `leo` merupakan wujud nyata yang memiliki nama Leo dan berat 190 kg. Tanpa pembuatan instance, seluruh class hanya berupa rancangan tanpa realisasi.

---

## 3. Alur Kerja Program (Dari Main Hingga Selesai)

1. **Tahap pembuatan objek:** Program membuat empat objek hewan (`leo, eli, edo, ulo`), dua objek kandang (`k1, k2`), satu objek kebun (`kebun`), dan satu objek dokter (`dok`).
2. **Tahap pengisian kandang:** Metode `k1.tambah(leo)` memasukkan singa dan gajah ke kandang Mamalia, sedangkan `k2` menampung elang dan ular.
3. **Tahap penghimpunan:** Metode `kebun.tambah_kandang(k1)` memasukkan kedua kandang ke dalam Kebun Binatang Gembira.
4. **Tahap pemeriksaan:** Metode `dok.periksa(leo)` memeriksa kondisi Leo dan mengembalikan status kesehatan menjadi 100.
5. **Tahap demonstrasi pewarisan dan enkapsulasi:** Metode `eli.menyusui()` membuktikan warisan dari `Mamalia`, sedangkan `get_berat()` dan `set_berat()` membuktikan akses data yang aman.
6. **Tahap parade:** Metode `kebun.parade()` menelusuri setiap kandang dan memanggil `h.suara()` secara berurutan, sehingga menghasilkan empat jenis suara yang berbeda sebagai wujud polimorfisme.

Secara keseluruhan, tujuh class hewan berperan sebagai penghuni, sedangkan tiga class pengelola (`Kandang` sebagai wadah, `DokterHewan` sebagai perawat, dan `KebunBinatang` sebagai koordinator) memastikan seluruh objek saling berinteraksi.

---

## 4. Tips Presentasi (Tiga Poin Utama)

1. **Awali dari class induk.** Tegaskan bahwa seluruh sistem berawal dari `Hewan` sebagai cetakan abstrak yang hanya berisi ketentuan kosong (`pass`). Tunjukkan bahwa `Singa, Gajah, Elang, dan Ular` masing-masing mengisi ketentuan tersebut secara berbeda. Dengan demikian, penguasaan Abstraksi dan Inheritance terlihat dalam satu penjelasan.
2. **Demonstrasikan parade secara langsung.** Jalankan program dan tunjukkan empat baris output parade. Sampaikan bahwa perintahnya sama (`h.suara()`), tetapi hasilnya berbeda. Demonstrasi tersebut lebih meyakinkan daripada penjelasan teoritis yang panjang.
3. **Tekankan perlindungan data dan kelahiran objek.** Jelaskan bahwa `__berat` dikunci dan hanya dapat diubah melalui `set_berat()` dengan validasi nilai positif. Tutup dengan menunjukkan bahwa seluruh objek lahir di Main melalui konstruktor, contohnya `leo = Singa("Leo", 190)`.

---

## 5. Naskah Presentasi (Script Formal)

> Assalamu'alaikum warahmatullahi wabarakatuh. Perkenankan saya mempresentasikan proyek Pemrograman Berorientasi Objek bertema Sistem Kebun Binatang Gembira yang ditulis dalam bahasa Python.
>
> Proyek ini terdiri atas sepuluh class yang saling berhubungan: Hewan sebagai induk, Mamalia dan Burung sebagai perantara, Singa, Gajah, Elang, dan Ular sebagai hewan nyata, serta Kandang, DokterHewan, dan KebunBinatang sebagai pengelola.
>
> Pertama, dari sisi abstraksi dan inheritance. Class Hewan merupakan cetakan utama yang berisi dua ketentuan kosong, yaitu suara dan gerak. Ketentuan tersebut kemudian diwarisi dan dilengkapi oleh class anak. Mamalia melengkapinya menjadi berjalan, Burung menjadi terbang, sedangkan Singa, Gajah, Elang, dan Ular masing-masing melengkapi suaranya menjadi Roar, Trumpet, Screech, dan Hiss.
>
> Kedua, dari sisi polimorfisme. Pada metode parade milik KebunBinatang, hanya terdapat satu perintah, yaitu h.suara. Namun ketika program dijalankan, perintah tersebut menghasilkan empat keluaran yang berbeda sesuai dengan jenis hewannya. Hal ini membuktikan bahwa satu perintah dapat berperilaku banyak.
>
> Ketiga, dari sisi enkapsulasi. Atribut nama bersifat public sehingga bebas dibaca, atribut kesehatan bersifat protected sehingga hanya dikelola oleh kalangan kebun seperti dokter, dan atribut berat bersifat private sehingga hanya dapat diakses melalui get_berat dan set_berat dengan validasi nilai positif.
>
> Keempat, dari sisi konstruktor dan instance. Seluruh objek nyata dibuat di bagian Main, contohnya leo sama dengan Singa Leo 190. Konstruktor __init__ memberikan nilai awal, dan pada Gajah ditambahkan pemanggilan super init untuk meminjam inisialisasi induk sebelum menambahkan belalai.
>
> Alur programnya berurutan: objek lahir di Main, dimasukkan ke kandang, kandang dimasukkan ke kebun, diperiksa oleh dokter, kemudian ditampilkan dalam parade suara.
>
> Demikian presentasi saya. Saya siap menjawab pertanyaan. Wassalamu'alaikum warahmatullahi wabarakatuh.

---

## 6. Prediksi Pertanyaan Kritis Dosen Beserta Jawaban

**1. Mengapa class Hewan tidak dibuat objeknya secara langsung?**
Jawaban: Karena Hewan berperan sebagai cetakan abstrak yang hanya berisi ketentuan kosong berupa `pass`. Class tersebut menetapkan bahwa setiap hewan wajib memiliki suara dan gerak, sedangkan pelaksanaannya diserahkan kepada class anak agar tidak terjadi penyeragaman perilaku.

**2. Mengapa Singa dapat memiliki nama dan berat padahal tidak memiliki `__init__`?**
Jawaban: Karena Singa mewarisi konstruktor dari Mamalia yang mewarisinya pula dari Hewan. Pewarisan memungkinkan class anak menggunakan konstruktor induk tanpa menulis ulang kode yang sama.

**3. Mengapa Gajah justru mendefinisikan `__init__` kembali dan menggunakan `super().__init__()`?**
Jawaban: Karena Gajah memerlukan atribut tambahan berupa `belalai` yang tidak dimiliki hewan lain. Pemanggilan `super().__init__()` digunakan untuk meminjam proses inisialisasi induk, kemudian menambahkan atribut khusus tersebut.

**4. Apakah perbedaan antara `nama`, `_kesehatan`, dan `__berat`?**
Jawaban: Ketiganya menunjukkan tingkatan akses. `nama` bersifat public dan bebas diakses, `_kesehatan` bersifat protected dan sebaiknya hanya diakses oleh kalangan kebun, sedangkan `__berat` bersifat private dan hanya dapat diakses melalui getter dan setter.

**5. Apabila `__berat` bersifat private, mengapa metode `info()` dapat membacanya?**
Jawaban: Karena metode `info()` berada dalam satu class yang sama dengan `__berat`. Aturan private memperbolehkan akses dari dalam class itu sendiri, tetapi melarang akses langsung dari luar class.

**6. Apakah tindakan DokterHewan yang mengubah `_kesehatan` melanggar enkapsulasi?**
Jawaban: Tidak. Atribut bertanda satu underscore merupakan konvensi protected yang memang diperuntukkan bagi kalangan internal sistem. Dokter hewan termasuk kalangan tersebut, sehingga tindakan tersebut merupakan penggunaan yang sesuai, bukan pelanggaran.

**7. Di manakah bukti konkret polimorfisme dalam kode ini?**
Jawaban: Bukti terdapat pada metode `parade()`. Perintah `h.suara()` ditulis satu kali, tetapi menghasilkan empat keluaran berbeda. Hal ini terjadi karena setiap class anak melakukan overriding dengan implementasi masing-masing, sehingga tidak diperlukan percabangan `if-else`.

**8. Apa yang terjadi apabila class Ular tidak mendefinisikan ulang `suara()`?**
Jawaban: Ular akan menggunakan metode kosong milik induk yang hanya berisi `pass`, sehingga tidak menghasilkan suara. Kondisi tersebut menegaskan pentingnya overriding agar setiap hewan memiliki perilaku yang lengkap.

**9. Apakah relasi antara KebunBinatang, Kandang, dan Hewan termasuk pewarisan?**
Jawaban: Bukan. Relasi tersebut merupakan asosiasi dan komposisi berupa kepemilikan wadah. Kandang memiliki daftar hewan, dan kebun memiliki daftar kandang. Hubungan ini menunjukkan kerja sama antarobjek, bukan pewarisan sifat.

**10. Apa kelemahan rancangan ini dan bagaimana pengembangannya?**
Jawaban: Rancangan ini masih bersifat dasar. Metode induk hanya menggunakan `pass` sehingga belum memaksa class anak untuk mengisi secara ketat, belum terdapat fitur penghapusan hewan dari kandang, serta validasi data masih terbatas. Pengembangan selanjutnya dapat menggunakan `ABC` dan `@abstractmethod` untuk penegakan kontrak yang lebih kuat, serta penambahan fitur pengelolaan yang lebih lengkap.
