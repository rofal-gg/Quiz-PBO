import json

# 1. Induk abstrak (kontrak kosong)
class Pegawai:
    def __init__(self, nama, id_pegawai, gaji):
        self.nama = nama
        self.id_pegawai = id_pegawai
        self._poin = 100
        self.__gaji = gaji
    def aktivitas(self):
        pass
    def get_gaji(self):
        return self.__gaji
    def set_gaji(self, nominal):
        if nominal > 0:
            self.__gaji = nominal
            return True
        return False
    def get_poin(self):
        return self._poin
    def info(self):
        return self.nama + " (" + self.id_pegawai + ") | " + str(self.aktivitas()) + " | gaji:" + str(self.__gaji) + " | poin:" + str(self._poin)
    def ke_dict(self):
        return {"peran": self.__class__.__name__, "nama": self.nama, "id": self.id_pegawai, "gaji": self.__gaji, "poin": self._poin}

# 2-3. Perantara
class FrontOfHouse(Pegawai):
    def layani(self):
        return "Tersenyum dan menyapa pelanggan."

class BackOfHouse(Pegawai):
    def layani(self):
        return "Fokus produksi, tidak langsung melayani."

# 4-7. Peran nyata
class Waiter(FrontOfHouse):
    def aktivitas(self):
        return "Mengantar pesanan ke meja."

class Kasir(FrontOfHouse):
    def aktivitas(self):
        return "Memproses pembayaran di kasir."

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

class Barista(BackOfHouse):
    def aktivitas(self):
        return "Menyeduh kopi dan meracik minuman."

# Pembangun ulang dari JSON (tanpa decorator)
def buat_pegawai(d):
    r = d.get("peran", "Waiter")
    p = None
    if r == "Baker":
        p = Baker(d["nama"], d["id"], d["gaji"], d.get("spesialisasi", "Pastry"))
    elif r == "Kasir":
        p = Kasir(d["nama"], d["id"], d["gaji"])
    elif r == "Barista":
        p = Barista(d["nama"], d["id"], d["gaji"])
    elif r == "Waiter":
        p = Waiter(d["nama"], d["id"], d["gaji"])
    else:
        print("Peringatan: peran '" + str(r) + "' tidak dikenal, dianggap Waiter.")
        p = Waiter(d["nama"], d["id"], d["gaji"])
    p._poin = d.get("poin", 100)
    return p

# 8. Wadah (aggregation)
class ShiftKerja:
    def __init__(self, nama_shift):
        self.nama_shift = nama_shift
        self.daftar = []
    def tambah(self, p):
        self.daftar.append(p)
    def cari(self, id_pegawai):
        for p in self.daftar:
            if p.id_pegawai == id_pegawai:
                return p
        return None
    def ke_dict(self):
        daftar = []
        for p in self.daftar:
            daftar.append(p.ke_dict())
        return {"nama": self.nama_shift, "isi": daftar}

def buat_shift(d):
    s = ShiftKerja(d["nama"])
    for item in d.get("isi", []):
        s.tambah(buat_pegawai(item))
    return s

# 9. Pengawas (dependency ke Pegawai)
class StoreManager:
    def __init__(self, nama):
        self.nama = nama
    def evaluasi(self, p):
        if p._poin < 200:
            p._poin = p._poin + 10
        return self.nama + " menilai " + p.nama + " poin=" + str(p._poin)

# 10. Koordinator (composition ke Shift)
class SistemCafe:
    def __init__(self, nama_cafe):
        self.nama_cafe = nama_cafe
        self.jadwal = []
    def atur_shift(self, s):
        self.jadwal.append(s)
    def cari_shift(self, nama):
        for s in self.jadwal:
            if s.nama_shift == nama:
                return s
        return None
    def cari_pegawai(self, id_pegawai):
        for s in self.jadwal:
            p = s.cari(id_pegawai)
            if p is not None:
                return p
        return None
    def operasional(self):
        print("=== Operasional " + self.nama_cafe + " ===")
        for s in self.jadwal:
            print(">> Shift " + s.nama_shift + " (" + str(len(s.daftar)) + " orang)")
            if len(s.daftar) == 0:
                print("   (belum ada pegawai)")
            for p in s.daftar:
                print("   - " + p.nama + " (" + p.__class__.__name__ + "): " + str(p.aktivitas()))
    def laporan(self):
        print("=== Laporan " + self.nama_cafe + " ===")
        for s in self.jadwal:
            print("- Shift " + s.nama_shift)
            for p in s.daftar:
                print("  " + p.info() + " | " + p.layani())

# 11. Penyimpanan JSON (metode biasa, tanpa dekorator)
class DatabaseJSON:
    def __init__(self, path):
        self.path = path
    def simpan(self, cafe):
        daftar = []
        for s in cafe.jadwal:
            daftar.append(s.ke_dict())
        data = {"nama_cafe": cafe.nama_cafe, "shift": daftar}
        f = open(self.path, "w")
        json.dump(data, f, indent=2)
        f.close()
    def muat(self, cafe):
        try:
            f = open(self.path, "r")
            data = json.load(f)
            f.close()
        except Exception:
            return False
        cafe.nama_cafe = data.get("nama_cafe", cafe.nama_cafe)
        cafe.jadwal = []
        for item in data.get("shift", []):
            cafe.atur_shift(buat_shift(item))
        return True

def contoh_awal():
    cafe = SistemCafe("Belbel Cafe")
    s1 = ShiftKerja("Pagi")
    s1.tambah(Waiter("Andi", "W01", 3000000.0))
    s1.tambah(Kasir("Budi", "K01", 3200000.0))
    s2 = ShiftKerja("Sore")
    s2.tambah(Baker("Cici", "B01", 4000000.0, "Pastry"))
    s2.tambah(Barista("Dedi", "R01", 3500000.0))
    cafe.atur_shift(s1)
    cafe.atur_shift(s2)
    return cafe

def tanya_angka(teks):
    s = input(teks).strip()
    s = s.replace(",", ".")
    titik = s.replace(".", "", 1)
    if len(s) > 0 and titik.isdigit():
        return float(s)
    return -1

def menu(cafe, manager, db):
    while True:
        print("")
        print("1 Tambah | 2 Laporan | 3 Evaluasi | 4 Operasional | 5 Simpan+Keluar")
        p = input("Pilih 1-5: ")
        if p == "1":
            nama = input("Nama: ").strip()
            ide = input("ID: ").strip()
            if nama == "" or ide == "":
                print("Nama dan ID tidak boleh kosong.")
                continue
            if cafe.cari_pegawai(ide) is not None:
                print("ID sudah dipakai.")
                continue
            gaji = tanya_angka("Gaji: ")
            if gaji <= 0:
                print("Gaji harus angka positif.")
                continue
            print("Peran: 1 Waiter 2 Kasir 3 Baker 4 Barista")
            r = input("Pilih peran: ")
            orang = None
            if r == "3":
                spes = input("Spesialisasi Baker: ")
                if spes == "":
                    spes = "Pastry"
                orang = Baker(nama, ide, gaji, spes)
            elif r == "2":
                orang = Kasir(nama, ide, gaji)
            elif r == "4":
                orang = Barista(nama, ide, gaji)
            else:
                orang = Waiter(nama, ide, gaji)
            print("Shift ada:", ", ".join([s.nama_shift for s in cafe.jadwal]))
            ns = input("Masuk shift mana: ")
            s = cafe.cari_shift(ns)
            if s is None:
                s = ShiftKerja(ns)
                cafe.atur_shift(s)
            s.tambah(orang)
            print(orang.info() + " masuk " + s.nama_shift)
        elif p == "2":
            cafe.laporan()
        elif p == "3":
            ide = input("ID dinilai: ")
            orang = cafe.cari_pegawai(ide)
            if orang is None:
                print("Tidak ketemu.")
                continue
            print(manager.evaluasi(orang))
        elif p == "4":
            cafe.operasional()
        elif p == "5":
            db.simpan(cafe)
            print("Tersimpan di " + db.path)
            break
        else:
            print("Pilih 1 sampai 5.")

if __name__ == "__main__":
    PATH = "data/karyawan.json"
    cafe = SistemCafe("Belbel Cafe")
    manager = StoreManager("Pak Anton")
    db = DatabaseJSON(PATH)
    ok = db.muat(cafe)
    if not ok:
        cafe = contoh_awal()
        db.simpan(cafe)
        print("Data contoh dibuat + disimpan.")
    cafe.laporan()
    cafe.operasional()
    menu(cafe, manager, db)
