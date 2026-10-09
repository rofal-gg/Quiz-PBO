"""Interface PyQt6 untuk Sistem Kafe Belbel Cafe.

File ini TERPISAH dari logika. Semua aturan bisnis tetap di kafe.py:
- tambah / hapus / cari pegawai -> ShiftKerja + SistemCafe
- nilai + pecat             -> StoreManager
- simpan / muat             -> DatabaseJSON
- contoh data               -> contoh_awal()

File ini hanya tampilan (GUI): mengambil input dari widget,
memanggil fungsi di atas, lalu menampilkan hasilnya.
kafe.py TIDAK diubah sama sekali.

Cara jalan:
    python gui_kafe.py
"""

import io
import sys
from contextlib import redirect_stdout

from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QTabWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QTableWidget, QTableWidgetItem, QTextBrowser,
    QMessageBox, QGroupBox, QHeaderView,
)

# Logika diimpor utuh, tidak ditulis ulang.
from kafe import (
    SistemCafe, ShiftKerja, StoreManager, DatabaseJSON,
    Waiter, Kasir, Baker, Barista, contoh_awal,
)

PATH = "data/karyawan.json"


def parse_gaji(teks):
    """Salinan cara tanya_angka() di kafe.py: koma jadi titik, harus angka positif."""
    s = teks.strip().replace(",", ".")
    titik = s.replace(".", "", 1)
    if len(s) > 0 and titik.isdigit():
        return float(s)
    return -1


def tangkap_cetak(fungsi):
    """Jalankan fungsi yang memakai print() (operasional/laporan asli)
    lalu kembalikan teksnya agar bisa ditampilkan di GUI."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        fungsi()
    return buf.getvalue()


class KafeWindow(QMainWindow):
    def __init__(self, cafe, manager, db):
        super().__init__()
        self.cafe = cafe
        self.manager = manager
        self.db = db
        self.setWindowTitle("Belbel Cafe - Interface PyQt6 (logika di kafe.py)")
        self.resize(900, 600)

        pusat = QWidget()
        self.setCentralWidget(pusat)
        layout_utama = QVBoxLayout()
        pusat.setLayout(layout_utama)

        judul = QLabel("Belbel Cafe | Manager: " + manager.nama + " | Data: " + db.path)
        layout_utama.addWidget(judul)

        self.tab = QTabWidget()
        layout_utama.addWidget(self.tab)

        self.buat_tab_data()
        self.buat_tab_tambah()
        self.buat_tab_evaluasi()
        self.buat_tab_shift_ops()
        self.buat_tab_gaji()

        baris_bawah = QHBoxLayout()
        self.btn_simpan = QPushButton("Simpan (menu 7)")
        self.btn_muat = QPushButton("Muat Ulang")
        self.btn_simpan.clicked.connect(self.simpan)
        self.btn_muat.clicked.connect(self.muat_ulang)
        baris_bawah.addWidget(self.btn_simpan)
        baris_bawah.addWidget(self.btn_muat)
        self.status = QLabel("")
        baris_bawah.addWidget(self.status)
        layout_utama.addLayout(baris_bawah)

        self.refresh_semua()

    # ---------- Tab 1: Data / Laporan (menu 2) ----------
    def buat_tab_data(self):
        w = QWidget()
        v = QVBoxLayout()
        w.setLayout(v)

        baris = QHBoxLayout()
        baris.addWidget(QLabel("Filter shift:"))
        self.combo_filter_shift = QComboBox()
        self.combo_filter_shift.currentTextChanged.connect(self.refresh_tabel)
        baris.addWidget(self.combo_filter_shift)
        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.refresh_semua)
        baris.addWidget(btn_refresh)
        v.addLayout(baris)

        self.tabel = QTableWidget(0, 8)
        self.tabel.setHorizontalHeaderLabels(
            ["Nama", "ID", "Peran", "Shift", "Gaji", "Poin", "Aktivitas", "Layani"]
        )
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabel.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        v.addWidget(self.tabel)

        v.addWidget(QLabel("Laporan + riwayat pecat (memanggil cafe.laporan() asli):"))
        self.teks_laporan = QTextBrowser()
        v.addWidget(self.teks_laporan)

        self.tab.addTab(w, "1. Data / Laporan")

    # ---------- Tab 2: Tambah (menu 1) ----------
    def buat_tab_tambah(self):
        w = QWidget()
        f = QFormLayout()
        w.setLayout(f)

        self.in_nama = QLineEdit()
        self.in_id = QLineEdit()
        self.in_gaji = QLineEdit()
        self.combo_peran = QComboBox()
        self.combo_peran.addItems(["Waiter", "Kasir", "Baker", "Barista"])
        self.combo_peran.currentTextChanged.connect(self.atur_spesialisasi)
        self.in_spes = QLineEdit("Pastry")
        self.combo_shift = QComboBox()
        self.in_shift_baru = QLineEdit()
        self.in_shift_baru.setPlaceholderText("Isi ini jika shift baru (opsional)")

        f.addRow("Nama:", self.in_nama)
        f.addRow("ID (unik):", self.in_id)
        f.addRow("Gaji (angka positif):", self.in_gaji)
        f.addRow("Peran:", self.combo_peran)
        f.addRow("Spesialisasi (Baker/Barista):", self.in_spes)
        f.addRow("Shift yang ada:", self.combo_shift)
        f.addRow("Shift baru:", self.in_shift_baru)

        btn = QPushButton("Tambah Pegawai")
        btn.clicked.connect(self.tambah_pegawai)
        f.addRow(btn)

        self.tab.addTab(w, "2. Tambah")

    def atur_spesialisasi(self, peran):
        if peran == "Baker" and self.in_spes.text().strip() == "":
            self.in_spes.setText("Pastry")
        if peran == "Barista" and self.in_spes.text().strip() in ("", "Pastry"):
            self.in_spes.setText("Menyeduh Kopi")
        self.in_spes.setEnabled(peran in ("Baker", "Barista"))

    # ---------- Tab 3: Evaluasi (menu 3) ----------
    def buat_tab_evaluasi(self):
        w = QWidget()
        v = QVBoxLayout()
        w.setLayout(v)

        box_cari = QGroupBox("Cari pegawai")
        h = QHBoxLayout()
        self.in_eval_id = QLineEdit()
        self.in_eval_id.setPlaceholderText("ID dinilai, misal W01")
        btn_cari = QPushButton("Cari")
        btn_cari.clicked.connect(self.cari_eval)
        h.addWidget(self.in_eval_id)
        h.addWidget(btn_cari)
        box_cari.setLayout(h)
        v.addWidget(box_cari)

        self.label_eval_info = QLabel("Belum ada pegawai dipilih.")
        v.addWidget(self.label_eval_info)

        self.btn_nilai = QPushButton("Nilai +25 (StoreManager.evaluasi)")
        self.btn_nilai.clicked.connect(self.nilai_pegawai)
        v.addWidget(self.btn_nilai)

        box_pecat = QGroupBox("Pecat bila poin = 100")
        h2 = QHBoxLayout()
        self.in_tanggal = QLineEdit()
        self.in_tanggal.setPlaceholderText("Tanggal pecat, misal 07-10-2026")
        self.btn_pecat = QPushButton("Pecat (StoreManager.pecat)")
        self.btn_pecat.clicked.connect(self.pecat_pegawai)
        h2.addWidget(self.in_tanggal)
        h2.addWidget(self.btn_pecat)
        box_pecat.setLayout(h2)
        v.addWidget(box_pecat)

        v.addStretch()
        self.tab.addTab(w, "3. Evaluasi + Pecat")

    # ---------- Tab 4: Shift + Operasional (menu 4-5) ----------
    def buat_tab_shift_ops(self):
        w = QWidget()
        v = QVBoxLayout()
        w.setLayout(v)

        box_shift = QGroupBox("Kelola shift (menu 5)")
        fs = QFormLayout()
        self.in_shift_nama = QLineEdit()
        self.in_hapus_shift = QLineEdit()
        self.in_pindah_id = QLineEdit()
        self.in_pindah_tujuan = QLineEdit()
        btn_buat = QPushButton("Buat shift baru")
        btn_hapus = QPushButton("Hapus shift kosong")
        btn_pindah = QPushButton("Pindahkan pegawai")
        btn_buat.clicked.connect(self.buat_shift)
        btn_hapus.clicked.connect(self.hapus_shift)
        btn_pindah.clicked.connect(self.pindah_pegawai)
        fs.addRow("Nama shift baru:", self.in_shift_nama)
        fs.addRow(btn_buat)
        fs.addRow("Nama shift dihapus:", self.in_hapus_shift)
        fs.addRow(btn_hapus)
        fs.addRow("ID pegawai dipindah:", self.in_pindah_id)
        fs.addRow("Pindah ke shift:", self.in_pindah_tujuan)
        fs.addRow(btn_pindah)
        box_shift.setLayout(fs)
        v.addWidget(box_shift)

        v.addWidget(QLabel("Operasional (memanggil cafe.operasional() asli):"))
        self.teks_ops = QTextBrowser()
        v.addWidget(self.teks_ops)

        self.tab.addTab(w, "4. Shift + Operasional")

    # ---------- Tab 5: Gaji (menu 6) ----------
    def buat_tab_gaji(self):
        w = QWidget()
        v = QVBoxLayout()
        w.setLayout(v)

        f = QFormLayout()
        self.in_gaji_id = QLineEdit()
        self.label_gaji_skr = QLabel("-")
        self.in_gaji_baru = QLineEdit()
        btn_cek = QPushButton("Cek gaji sekarang")
        btn_cek.clicked.connect(self.cek_gaji)
        btn_ubah = QPushButton("Ubah gaji (set_gaji)")
        btn_ubah.clicked.connect(self.ubah_gaji)
        f.addRow("ID:", self.in_gaji_id)
        f.addRow(btn_cek)
        f.addRow("Gaji sekarang:", self.label_gaji_skr)
        f.addRow("Gaji baru:", self.in_gaji_baru)
        f.addRow(btn_ubah)
        v.addLayout(f)
        v.addStretch()

        self.tab.addTab(w, "5. Gaji")

    # ---------- Aksi: refresh ----------
    def refresh_semua(self):
        nama_shift = [s.nama_shift for s in self.cafe.jadwal]
        sekarang = self.combo_filter_shift.currentText()

        self.combo_filter_shift.blockSignals(True)
        self.combo_shift.blockSignals(True)
        self.combo_filter_shift.clear()
        self.combo_shift.clear()
        self.combo_filter_shift.addItem("Semua")
        self.combo_filter_shift.addItems(nama_shift)
        self.combo_shift.addItems(nama_shift)
        self.combo_filter_shift.blockSignals(False)
        self.combo_shift.blockSignals(False)

        if sekarang in (["Semua"] + nama_shift):
            self.combo_filter_shift.setCurrentText(sekarang)

        self.refresh_tabel()
        # Panggil fungsi asli tanpa mengubah logika, tampilkan outputnya.
        self.teks_laporan.setText(tangkap_cetak(self.cafe.laporan))
        self.teks_ops.setText(tangkap_cetak(self.cafe.operasional))

    def refresh_tabel(self):
        pilih = self.combo_filter_shift.currentText()
        baris = []
        for s in self.cafe.jadwal:
            if pilih != "Semua" and s.nama_shift != pilih:
                continue
            for p in s.daftar:
                baris.append((s.nama_shift, p))
        self.tabel.setRowCount(len(baris))
        for i, (nama_shift, p) in enumerate(baris):
            self.tabel.setItem(i, 0, QTableWidgetItem(p.nama))
            self.tabel.setItem(i, 1, QTableWidgetItem(p.id_pegawai))
            self.tabel.setItem(i, 2, QTableWidgetItem(p.__class__.__name__))
            self.tabel.setItem(i, 3, QTableWidgetItem(nama_shift))
            self.tabel.setItem(i, 4, QTableWidgetItem(str(p.get_gaji())))
            self.tabel.setItem(i, 5, QTableWidgetItem(str(p.get_poin())))
            self.tabel.setItem(i, 6, QTableWidgetItem(str(p.aktivitas())))
            self.tabel.setItem(i, 7, QTableWidgetItem(p.layani()))

    # ---------- Aksi: tambah (menu 1) ----------
    def tambah_pegawai(self):
        nama = self.in_nama.text().strip()
        ide = self.in_id.text().strip()
        if nama == "" or ide == "":
            QMessageBox.warning(self, "Ditolak", "Nama dan ID tidak boleh kosong.")
            return
        if self.cafe.cari_pegawai(ide) is not None:
            QMessageBox.warning(self, "Ditolak", "ID sudah dipakai.")
            return
        gaji = parse_gaji(self.in_gaji.text())
        if gaji <= 0:
            QMessageBox.warning(self, "Ditolak", "Gaji harus angka positif.")
            return

        peran = self.combo_peran.currentText()
        if peran == "Baker":
            spes = self.in_spes.text().strip() or "Pastry"
            orang = Baker(nama, ide, gaji, spes)
        elif peran == "Barista":
            spes = self.in_spes.text().strip() or "Menyeduh Kopi"
            orang = Barista(nama, ide, gaji, spes)
        elif peran == "Kasir":
            orang = Kasir(nama, ide, gaji)
        else:
            orang = Waiter(nama, ide, gaji)

        ns = self.in_shift_baru.text().strip()
        if ns == "":
            ns = self.combo_shift.currentText().strip()
        if ns == "":
            QMessageBox.warning(self, "Ditolak", "Nama shift tidak boleh kosong.")
            return
        s = self.cafe.cari_shift(ns)
        if s is None:
            s = ShiftKerja(ns)
            self.cafe.atur_shift(s)
        s.tambah(orang)

        QMessageBox.information(self, "Berhasil", orang.info() + " masuk " + s.nama_shift)
        self.in_nama.clear()
        self.in_id.clear()
        self.in_gaji.clear()
        self.in_shift_baru.clear()
        self.refresh_semua()

    # ---------- Aksi: evaluasi (menu 3) ----------
    def cari_eval(self):
        ide = self.in_eval_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            self.label_eval_info.setText("Tidak ketemu (mungkin sudah dipecat).")
            return
        self.label_eval_info.setText(orang.info())

    def nilai_pegawai(self):
        ide = self.in_eval_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            QMessageBox.warning(self, "Gagal", "Tidak ketemu (mungkin sudah dipecat).")
            return
        hasil = self.manager.evaluasi(orang)
        QMessageBox.information(self, "Evaluasi", hasil)
        self.label_eval_info.setText(orang.info())
        if orang.get_poin() >= 100:
            QMessageBox.information(
                self, "Poin 100",
                "Poin sudah 100. Isi tanggal lalu tekan Pecat.")
        self.refresh_semua()

    def pecat_pegawai(self):
        ide = self.in_eval_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            QMessageBox.warning(self, "Gagal", "ID tidak ketemu.")
            return
        tgl = self.in_tanggal.text().strip() or "tanpa-tanggal"
        hasil = self.manager.pecat(self.cafe, ide, tgl)
        QMessageBox.information(self, "Pecat", hasil)
        self.refresh_semua()

    # ---------- Aksi: shift (menu 5) ----------
    def buat_shift(self):
        ns = self.in_shift_nama.text().strip()
        if ns == "":
            QMessageBox.warning(self, "Gagal", "Nama tidak boleh kosong.")
            return
        if self.cafe.cari_shift(ns) is not None:
            QMessageBox.warning(self, "Gagal", "Shift sudah ada.")
            return
        self.cafe.atur_shift(ShiftKerja(ns))
        QMessageBox.information(self, "Berhasil", "Shift " + ns + " dibuat.")
        self.in_shift_nama.clear()
        self.refresh_semua()

    def hapus_shift(self):
        ns = self.in_hapus_shift.text().strip()
        s = self.cafe.cari_shift(ns)
        if s is None:
            QMessageBox.warning(self, "Gagal", "Tidak ketemu.")
            return
        if len(s.daftar) > 0:
            QMessageBox.warning(
                self, "Gagal",
                "Tidak bisa, masih ada " + str(len(s.daftar)) + " pegawai. Pindahkan dulu.")
            return
        self.cafe.jadwal.remove(s)
        QMessageBox.information(self, "Berhasil", "Shift " + ns + " dihapus.")
        self.in_hapus_shift.clear()
        self.refresh_semua()

    def pindah_pegawai(self):
        ide = self.in_pindah_id.text().strip()
        asal = None
        orang = None
        for s in self.cafe.jadwal:
            orang = s.cari(ide)
            if orang is not None:
                asal = s
                break
        if orang is None:
            QMessageBox.warning(self, "Gagal", "Tidak ketemu.")
            return
        ns = self.in_pindah_tujuan.text().strip()
        if ns == "":
            QMessageBox.warning(self, "Gagal", "Tujuan kosong, dibatalkan.")
            return
        tujuan = self.cafe.cari_shift(ns)
        if tujuan is None:
            tujuan = ShiftKerja(ns)
            self.cafe.atur_shift(tujuan)
        asal.hapus(ide)
        tujuan.tambah(orang)
        QMessageBox.information(
            self, "Berhasil",
            orang.nama + " pindah " + asal.nama_shift + " -> " + tujuan.nama_shift)
        self.in_pindah_id.clear()
        self.in_pindah_tujuan.clear()
        self.refresh_semua()

    # ---------- Aksi: gaji (menu 6) ----------
    def cek_gaji(self):
        ide = self.in_gaji_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            QMessageBox.warning(self, "Gagal", "Tidak ketemu.")
            return
        self.label_gaji_skr.setText(str(orang.get_gaji()))

    def ubah_gaji(self):
        ide = self.in_gaji_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            QMessageBox.warning(self, "Gagal", "Tidak ketemu.")
            return
        gaji = parse_gaji(self.in_gaji_baru.text())
        if orang.set_gaji(gaji):
            QMessageBox.information(self, "Berhasil", "Gaji baru: " + str(orang.get_gaji()))
        else:
            QMessageBox.warning(self, "Ditolak", "Ditolak, harus angka positif.")
            return
        self.label_gaji_skr.setText(str(orang.get_gaji()))
        self.refresh_semua()

    # ---------- Aksi: simpan / muat (menu 7) ----------
    def simpan(self):
        self.db.simpan(self.cafe)
        self.status.setText("Tersimpan di " + self.db.path)
        QMessageBox.information(self, "Simpan", "Tersimpan di " + self.db.path)

    def muat_ulang(self):
        ok = self.db.muat(self.cafe)
        if not ok:
            QMessageBox.warning(self, "Gagal", "File tidak ada / rusak.")
            return
        self.refresh_semua()
        self.status.setText("Dimuat dari " + self.db.path)


def main():
    app = QApplication(sys.argv)
    cafe = SistemCafe("Belbel Cafe")
    manager = StoreManager("Pak Anton")
    db = DatabaseJSON(PATH)
    ok = db.muat(cafe)
    if not ok:
        cafe = contoh_awal()
        db.simpan(cafe)
    win = KafeWindow(cafe, manager, db)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
