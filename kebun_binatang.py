# 1. Parent abstrak: cetak biru semua hewan (versi pemula, tanpa import aneh-aneh)
class Hewan:
    def __init__(self, nama, berat):
        self.nama = nama            # public: bebas dibaca
        self._kesehatan = 100       # protected: anggap milik dalam kebun saja
        self.__berat = berat        # private: disembunyikan
    def suara(self):
        pass  # kosong, anak wajib isi sendiri
    def gerak(self):
        pass  # kosong, anak wajib isi sendiri
    def get_berat(self): 
        return self.__berat            # getter
    def set_berat(self, b):                             # setter + validasi
        if b > 0: self.__berat = b
    def info(self): 
        return f"{self.nama} | {self.gerak()} | {self.suara()} | {self.__berat}kg"

# 2-3. Keluarga perantara (pewaris level 1)
class Mamalia(Hewan):
    def gerak(self): 
        return "berjalan"  # sifat umum mamalia
    def menyusui(self): 
        return f"{self.nama} menyusui anaknya"

class Burung(Hewan):
    def gerak(self): 
        return "terbang"   # sifat umum burung

# 4-7. Hewan nyata (pewaris level 2, perilaku beda-beda)
class Singa(Mamalia):
    def suara(self): 
        return "Roar!"

class Gajah(Mamalia):
    def __init__(self, nama, berat, belalai=2):  # konstruktor + super()
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

# 8. Wadah hewan
class Kandang:
    def __init__(self, nama): 
        self.nama = nama 
        self.isi = []
    def tambah(self, h): 
        self.isi.append(h)

# 9. Teman hewan
class DokterHewan:
    def __init__(self, nama): 
        self.nama = nama
    def periksa(self, h):
        h._kesehatan = 100  # boleh sentuh yang protected karena masih keluarga kebun
        return f"{self.nama} memeriksa {h.nama}: sehat!"

# 10. Pengelola semua
class KebunBinatang:
    def __init__(self, nama): 
        self.nama = nama
        self.kandang = []
    def tambah_kandang(self, k): 
        self.kandang.append(k)
    def parade(self):  # POLIMORFISME: satu perintah, banyak gaya
        for k in self.kandang:
            for h in k.isi: print(f"{h.nama}: {h.suara()} ({h.gerak()})")


if __name__ == "__main__":
    # INSTANCE: mencetak hewan nyata dari cetakan class (lewat konstruktor)
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
