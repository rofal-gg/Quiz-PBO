import json

# 1. Induk abstrak (kontrak kosong)
class Pegawai:
    def __init__(self, nama, id_pegawai, gaji):
        self.nama = nama
        self.id_pegawai = id_pegawai
        self._poin = 0
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
    def __init__(self, nama, id_pegawai, gaji, spesialisasi="Menyeduh Kopi"):
        super().__init__(nama, id_pegawai, gaji)
        self.spesialisasi = spesialisasi
    def aktivitas(self):
        return "Menyeduh kopi dan meracik minuman.(Spesialis: " + self.spesialisasi + ")."
    def ke_dict(self):
        d = super().ke_dict()
        d["spesialisasi"] = self.spesialisasi
        return d

# Pembangun ulang dari JSON (tanpa decorator)
def buat_pegawai(d):
    r = d.get("peran", "Waiter")
    p = None
    if r == "Baker":
        p = Baker(d["nama"], d["id"], d["gaji"], d.get("spesialisasi", "Pastry"))
    elif r == "Kasir":
        p = Kasir(d["nama"], d["id"], d["gaji"])
    elif r == "Barista":
        p = Barista(d["nama"], d["id"], d["gaji"], d.get("spesialisasi", "Menyeduh Kopi"))
    elif r == "Waiter":
        p = Waiter(d["nama"], d["id"], d["gaji"])
    else:
        print("Peringatan: peran '" + str(r) + "' tidak dikenal, dianggap Waiter.")
        p = Waiter(d["nama"], d["id"], d["gaji"])
    p._poin = d.get("poin", 0)
    return p

# 8. Wadah (aggregation)
class ShiftKerja:
    def __init__(self, nama_shift):
        self.nama_shift = nama_shift
        self.daftar = []
    def tambah(self, p):
        self.daftar.append(p)
    def hapus(self, id_pegawai):
        for i in range(len(self.daftar)):
            if self.daftar[i].id_pegawai == id_pegawai:
                del self.daftar[i]
                return True
        return False
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
        # Poin naik +25 per evaluasi, 0 -> 25 -> 50 -> 75 -> 100
        if p._poin < 100:
            p._poin = p._poin + 25
            if p._poin > 100:
                p._poin = 100
        if p._poin >= 100:
            return self.nama + " menilai " + p.nama + " poin=100 (DIPECAT)"
        return self.nama + " menilai " + p.nama + " poin=" + str(p._poin)
    def pecat(self, cafe, id_pegawai, tanggal):
        for s in cafe.jadwal:
            p = s.cari(id_pegawai)
            if p is not None:
                if p._poin >= 100:
                    s.hapus(id_pegawai)
                    data = p.ke_dict()
                    data["tanggal_pecat"] = tanggal
                    cafe.riwayat_pecat.append(data)
                    return p.nama + " (" + id_pegawai + ") DIPECAT tgl " + tanggal + " dan dihapus dari shift " + s.nama_shift
                return p.nama + " belum bisa dipecat, poin=" + str(p._poin) + " (batas 100)"
        return "ID tidak ketemu."

# 10. Koordinator (composition ke Shift)
class SistemCafe:
    def __init__(self, nama_cafe):
        self.nama_cafe = nama_cafe
        self.jadwal = []
        self.riwayat_pecat = []
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
        print("--- Laporan Pemecatan ---")
        if len(self.riwayat_pecat) == 0:
            print("  (belum ada yang dipecat)")
        for d in self.riwayat_pecat:
            print("  " + d["nama"] + " (" + d["id"] + ") DIPECAT tgl " + d.get("tanggal_pecat", "-"))

# 11. Penyimpanan JSON (metode biasa, tanpa dekorator)
class DatabaseJSON:
    def __init__(self, path):
        self.path = path
    def simpan(self, cafe):
        daftar = []
        for s in cafe.jadwal:
            daftar.append(s.ke_dict())
        data = {"nama_cafe": cafe.nama_cafe, "shift": daftar, "pecat": cafe.riwayat_pecat}
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
        cafe.riwayat_pecat = data.get("pecat", [])
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
        print("1 Tambah | 2 Laporan | 3 Evaluasi | 4 Operasional | 5 Shift | 6 Gaji | 7 Simpan+Keluar")
        p = input("Pilih 1-7: ")
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
                spes = input("Spesialisasi Barista (kosongkan = Menyeduh Kopi): ").strip()
                if spes == "":
                    spes = "Menyeduh Kopi"
                orang = Barista(nama, ide, gaji, spes)
            else:
                orang = Waiter(nama, ide, gaji)
            print("Shift ada:", ", ".join([s.nama_shift for s in cafe.jadwal]))
            ns = input("Masuk shift mana (ketik nama baru untuk buat shift baru): ").strip()
            if ns == "":
                print("Nama shift tidak boleh kosong, pegawai dibatalkan.")
                continue
            s = cafe.cari_shift(ns)
            if s is None:
                s = ShiftKerja(ns)
                cafe.atur_shift(s)
            s.tambah(orang)
            print(orang.info() + " masuk " + s.nama_shift)
        elif p == "2":
            cafe.laporan()
        elif p == "3":
            ide = input("ID dinilai: ").strip()
            orang = cafe.cari_pegawai(ide)
            if orang is None:
                print("Tidak ketemu (mungkin sudah dipecat).")
                continue
            print(manager.evaluasi(orang))
            if orang.get_poin() >= 100:
                tgl = input("Tanggal pecat (misal 07-10-2026): ").strip()
                if tgl == "":
                    tgl = "tanpa-tanggal"
                print(manager.pecat(cafe, ide, tgl))
        elif p == "4":
            cafe.operasional()
        elif p == "5":
            print("Kelola shift: 1 Buat baru | 2 Hapus kosong | 3 Pindah pegawai | 4 Kembali")
            q = input("Pilih 1-4: ").strip()
            if q == "1":
                ns = input("Nama shift baru: ").strip()
                if ns == "":
                    print("Nama tidak boleh kosong.")
                elif cafe.cari_shift(ns) is not None:
                    print("Shift sudah ada.")
                else:
                    cafe.atur_shift(ShiftKerja(ns))
                    print("Shift " + ns + " dibuat.")
            elif q == "2":
                ns = input("Nama shift dihapus: ").strip()
                s = cafe.cari_shift(ns)
                if s is None:
                    print("Tidak ketemu.")
                elif len(s.daftar) > 0:
                    print("Tidak bisa, masih ada " + str(len(s.daftar)) + " pegawai. Pindahkan dulu.")
                else:
                    cafe.jadwal.remove(s)
                    print("Shift " + ns + " dihapus.")
            elif q == "3":
                ide = input("ID pegawai dipindah: ").strip()
                asal = None
                orang = None
                for s in cafe.jadwal:
                    orang = s.cari(ide)
                    if orang is not None:
                        asal = s
                        break
                if orang is None:
                    print("Tidak ketemu.")
                else:
                    print("Shift ada:", ", ".join([s.nama_shift for s in cafe.jadwal]))
                    ns = input("Pindah ke shift (ketik baru untuk buat): ").strip()
                    if ns == "":
                        print("Dibatalkan.")
                    else:
                        tujuan = cafe.cari_shift(ns)
                        if tujuan is None:
                            tujuan = ShiftKerja(ns)
                            cafe.atur_shift(tujuan)
                        asal.hapus(ide)
                        tujuan.tambah(orang)
                        print(orang.nama + " pindah " + asal.nama_shift + " -> " + tujuan.nama_shift)
        elif p == "6":
            ide = input("ID diubah gajinya: ").strip()
            orang = cafe.cari_pegawai(ide)
            if orang is None:
                print("Tidak ketemu.")
                continue
            print("Gaji sekarang: " + str(orang.get_gaji()))
            gaji = tanya_angka("Gaji baru: ")
            if orang.set_gaji(gaji):
                print("Gaji baru: " + str(orang.get_gaji()))
            else:
                print("Ditolak, harus angka positif.")
        elif p == "7":
            db.simpan(cafe)
            print("Tersimpan di " + db.path)
            break
        else:
            print("Pilih 1 sampai 7.")

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
