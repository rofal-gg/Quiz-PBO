"""Interface PyQt6 Formal - Sistem Kafe Belbel Cafe.

Tema: Formal Navy + Gold + Slate (kantoran, rapi, berwarna tapi sopan).
File ini HANYA tampilan (GUI). Semua aturan bisnis tetap di kafe.py:
- tambah / hapus / cari pegawai -> ShiftKerja + SistemCafe
- nilai + pecat             -> StoreManager
- simpan / muat             -> DatabaseJSON
- contoh data               -> contoh_awal()

kafe.py TIDAK diubah sama sekali.

Cara jalan:
    python gui_kafe.py
"""

import io
import sys
from contextlib import redirect_stdout

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QTabWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QTableWidget, QTableWidgetItem, QTextBrowser,
    QMessageBox, QGroupBox, QHeaderView, QFrame,
)

# Logika diimpor utuh, tidak ditulis ulang.
from kafe import (
    SistemCafe, ShiftKerja, StoreManager, DatabaseJSON,
    Waiter, Kasir, Baker, Barista, contoh_awal,
)

PATH = "data/karyawan.json"

# ------------------------------------------------------------------
# Palet formal
# ------------------------------------------------------------------
NAVY = "#1B2F4B"        # header utama
NAVY_2 = "#243A5E"      # header gradasi / tombol utama
NAVY_MUDA = "#E8EDF3"   # latar panel lembut
GOLD = "#C9A86A"        # aksen formal
GOLD_TUA = "#A8874E"
BG = "#EDF0F4"          # latar aplikasi
KARTU = "#FFFFFF"
TEKS = "#1E293B"
TEKS_MUDA = "#64748B"
GARIS = "#CBD5E1"
MERAH_FORMAL = "#9E2B25"
HIJAU_FORMAL = "#2F6B4F"

STYLESHEET = f"""
QWidget {{
    font-family: "Segoe UI", Arial;
    font-size: 10pt;
    color: {TEKS};
}}
QMainWindow {{ background: {BG}; }}

/* ---------- Header ---------- */
#header {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {NAVY}, stop:1 {NAVY_2});
    border-radius: 12px;
}}
#headerJudul {{
    color: white;
    font-size: 17pt;
    font-weight: 800;
    letter-spacing: 1px;
}}
#headerSub {{
    color: #D6DEE8;
    font-size: 9.5pt;
}}
#logoBadge {{
    background: {GOLD};
    color: {NAVY};
    font-size: 16pt;
    font-weight: 800;
    border-radius: 22px;
}}
#headerInfo {{
    color: #E6EBF2;
    font-size: 9pt;
}}
#garisEmas {{
    background: {GOLD};
    border-radius: 1px;
}}

/* ---------- Kartu statistik ---------- */
#statCard {{
    background: {KARTU};
    border: 1px solid {GARIS};
    border-left: 5px solid {GOLD};
    border-radius: 10px;
}}
#statCardNavy {{
    background: {KARTU};
    border: 1px solid {GARIS};
    border-left: 5px solid {NAVY};
    border-radius: 10px;
}}
#statAngka {{
    font-size: 18pt;
    font-weight: 800;
    color: {NAVY};
}}
#statLabel {{
    font-size: 8.5pt;
    font-weight: 600;
    color: {TEKS_MUDA};
    letter-spacing: 0.5px;
}}

/* ---------- Tab ---------- */
QTabWidget::pane {{
    background: {KARTU};
    border: 1px solid {GARIS};
    border-radius: 10px;
    top: -1px;
}}
QTabBar::tab {{
    background: #DCE3EC;
    color: {NAVY};
    padding: 9px 18px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 600;
}}
QTabBar::tab:selected {{
    background: {NAVY};
    color: white;
}}
QTabBar::tab:hover:!selected {{
    background: #C7D2E0;
}}

/* ---------- Form ---------- */
QLabel {{ color: {TEKS}; }}
 QLabel.judulSekksi {{
    font-size: 11pt;
    font-weight: 700;
    color: {NAVY};
}}
QLabel.subSekksi {{
    color: {TEKS_MUDA};
    font-size: 9pt;
}}
QLineEdit, QComboBox {{
    background: white;
    border: 1px solid {GARIS};
    border-radius: 6px;
    padding: 7px 10px;
    selection-background-color: {NAVY};
}}
QLineEdit:focus, QComboBox:focus {{
    border: 2px solid {NAVY};
}}
QComboBox QAbstractItemView {{
    background: white;
    selection-background-color: {NAVY};
    selection-color: white;
}}

/* ---------- Tombol ---------- */
QPushButton {{
    background: {NAVY_2};
    color: white;
    border: none;
    border-radius: 7px;
    padding: 8px 16px;
    font-weight: 600;
}}
QPushButton:hover {{ background: #2E4A75; }}
QPushButton:pressed {{ background: #16263F; }}
QPushButton:disabled {{
    background: #94A3B8;
    color: #E2E8F0;
}}
#btnEmas {{
    background: {GOLD};
    color: {NAVY};
    font-weight: 700;
}}
#btnEmas:hover {{ background: #D8BC85; }}
#btnEmas:pressed {{ background: {GOLD_TUA}; color: white; }}
#btnBahaya {{
    background: {MERAH_FORMAL};
    color: white;
}}
#btnBahaya:hover {{ background: #B23A32; }}
#btnHijau {{
    background: {HIJAU_FORMAL};
    color: white;
}}
#btnHijau:hover {{ background: #3A7F60; }}
#btnHantu {{
    background: transparent;
    border: 1px solid rgba(255,255,255,0.7);
    color: white;
}}
#btnHantu:hover {{
    background: rgba(255,255,255,0.15);
}}
#btnGaris {{
    background: white;
    border: 1px solid {NAVY};
    color: {NAVY};
}}
#btnGaris:hover {{ background: {NAVY_MUDA}; }}

/* ---------- GroupBox ---------- */
QGroupBox {{
    background: #F8FAFC;
    border: 1px solid {GARIS};
    border-radius: 10px;
    margin-top: 14px;
    padding-top: 12px;
    font-weight: 700;
    color: {NAVY};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    background: {GOLD};
    color: {NAVY};
    border-radius: 4px;
}}

/* ---------- Tabel ---------- */
QTableWidget {{
    background: white;
    alternate-background-color: #F4F6F9;
    gridline-color: {GARIS};
    border: 1px solid {GARIS};
    border-radius: 8px;
    selection-background-color: {NAVY};
    selection-color: white;
}}
QHeaderView::section {{
    background: {NAVY};
    color: white;
    padding: 8px;
    border: none;
    font-weight: 700;
}}

/* ---------- Laporan ---------- */
QTextBrowser {{
    background: #0F1E33;
    color: #E8EEF5;
    border: 1px solid {NAVY};
    border-radius: 8px;
    padding: 8px;
    font-family: Consolas, "Courier New", monospace;
    font-size: 9.5pt;
}}
#panelTips {{
    background: {NAVY_MUDA};
    border: 1px solid {GARIS};
    border-radius: 10px;
}}
#teksTips {{
    color: {NAVY};
    font-size: 9pt;
}}
#statusBar {{
    background: white;
    border: 1px solid {GARIS};
    border-radius: 8px;
    padding: 6px 12px;
    color: {TEKS_MUDA};
}}
#badgeShift {{
    background: {NAVY_MUDA};
    border: 1px solid {NAVY};
    color: {NAVY};
    border-radius: 6px;
    padding: 2px 10px;
    font-weight: 700;
}}
"""


def parse_gaji(teks):
    """Salinan cara tanya_angka() di kafe.py: koma jadi titik, harus angka positif."""
    s = teks.strip().replace(",", ".")
    titik = s.replace(".", "", 1)
    if len(s) > 0 and titik.isdigit():
        return float(s)
    return -1


def format_rupiah(nominal):
    """Format formal Indonesia: 3000000 -> Rp 3.000.000."""
    try:
        n = int(float(nominal))
    except Exception:
        return str(nominal)
    s = f"{n:,}".replace(",", ".")
    return "Rp " + s


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
        self.setWindowTitle("Belbel Cafe — Sistem Manajemen Karyawan (Formal)")
        self.resize(1080, 720)
        self.setMinimumSize(980, 640)

        pusat = QWidget()
        self.setCentralWidget(pusat)
        layout_utama = QVBoxLayout()
        layout_utama.setContentsMargins(14, 14, 14, 14)
        layout_utama.setSpacing(10)
        pusat.setLayout(layout_utama)

        layout_utama.addWidget(self._buat_header())
        layout_utama.addLayout(self._buat_statistik())

        self.tab = QTabWidget()
        layout_utama.addWidget(self.tab, 1)

        self.buat_tab_data()
        self.buat_tab_tambah()
        self.buat_tab_evaluasi()
        self.buat_tab_shift_ops()
        self.buat_tab_gaji()

        layout_utama.addWidget(self._buat_statusbar())
        self.refresh_semua()

    # ================= Header formal =================
    def _buat_header(self):
        header = QFrame()
        header.setObjectName("header")
        h = QHBoxLayout()
        h.setContentsMargins(16, 14, 16, 14)
        h.setSpacing(14)
        header.setLayout(h)

        logo = QLabel("BC")
        logo.setObjectName("logoBadge")
        logo.setFixedSize(52, 52)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h.addWidget(logo)

        box_judul = QVBoxLayout()
        box_judul.setSpacing(2)
        judul = QLabel("BELBEL CAFE")
        judul.setObjectName("headerJudul")
        sub = QLabel("Sistem Manajemen Karyawan  •  Tertib  •  Transparan  •  Formal")
        sub.setObjectName("headerSub")
        garis = QFrame()
        garis.setObjectName("garisEmas")
        garis.setFixedHeight(3)
        garis.setFixedWidth(260)
        box_judul.addWidget(judul)
        box_judul.addWidget(garis)
        box_judul.addWidget(sub)
        h.addLayout(box_judul, 1)

        box_info = QVBoxLayout()
        box_info.setSpacing(6)
        info = QLabel(f"Manager: {self.manager.nama}   •   Data: {self.db.path}")
        info.setObjectName("headerInfo")
        box_info.addWidget(info, alignment=Qt.AlignmentFlag.AlignRight)

        baris_btn = QHBoxLayout()
        baris_btn.setSpacing(8)
        self.btn_simpan = QPushButton("💾  SIMPAN (Menu 7)")
        self.btn_simpan.setObjectName("btnEmas")
        self.btn_muat = QPushButton("↻  MUAT ULANG")
        self.btn_muat.setObjectName("btnHantu")
        self.btn_simpan.clicked.connect(self.simpan)
        self.btn_muat.clicked.connect(self.muat_ulang)
        baris_btn.addWidget(self.btn_simpan)
        baris_btn.addWidget(self.btn_muat)
        box_info.addLayout(baris_btn)
        h.addLayout(box_info)
        return header

    def _kartu_stat(self, label, nilai_awal="0", aksen_navy=False):
        kartu = QFrame()
        kartu.setObjectName("statCardNavy" if aksen_navy else "statCard")
        v = QVBoxLayout()
        v.setContentsMargins(14, 10, 14, 10)
        v.setSpacing(2)
        angka = QLabel(nilai_awal)
        angka.setObjectName("statAngka")
        ket = QLabel(label.upper())
        ket.setObjectName("statLabel")
        v.addWidget(angka)
        v.addWidget(ket)
        kartu.setLayout(v)
        return kartu, angka

    def _buat_statistik(self):
        baris = QHBoxLayout()
        baris.setSpacing(10)
        self.kartu_total, self.stat_total = self._kartu_stat("Total Pegawai Aktif")
        self.kartu_shift, self.stat_shift = self._kartu_stat("Shift Aktif", aksen_navy=True)
        self.kartu_gaji, self.stat_gaji = self._kartu_stat("Rata-rata Gaji")
        self.kartu_pecat, self.stat_pecat = self._kartu_stat("Riwayat Pecat", aksen_navy=True)
        for k in (self.kartu_total, self.kartu_shift, self.kartu_gaji, self.kartu_pecat):
            baris.addWidget(k, 1)
        return baris

    def _buat_statusbar(self):
        self.status = QLabel("Siap.")
        self.status.setObjectName("statusBar")
        return self.status

    def _panel_tips(self, judul, isi):
        panel = QFrame()
        panel.setObjectName("panelTips")
        v = QVBoxLayout()
        v.setContentsMargins(14, 14, 14, 14)
        j = QLabel(judul)
        j.setProperty("class", "judulSekksi")
        j.setStyleSheet("font-size: 11pt; font-weight: 700; color: #1B2F4B;")
        t = QLabel(isi)
        t.setObjectName("teksTips")
        t.setWordWrap(True)
        v.addWidget(j)
        v.addWidget(t)
        v.addStretch()
        panel.setLayout(v)
        return panel

    def _set_status(self, teks):
        self.status.setText(teks)

    # ---------- Tab 1: Data / Laporan (menu 2) ----------
    def buat_tab_data(self):
        w = QWidget()
        v = QVBoxLayout()
        v.setContentsMargins(14, 14, 14, 14)
        v.setSpacing(8)
        w.setLayout(v)

        j = QLabel("Data & Laporan Pegawai  —  setara Menu 2 (cafe.laporan)")
        j.setStyleSheet("font-size: 11pt; font-weight: 700; color: #1B2F4B;")
        s = QLabel("Filter berdasarkan shift atau cari nama / ID. Tabel hanya-baca, sumber tetap dari objek ShiftKerja.")
        s.setProperty("class", "subSekksi")
        s.setStyleSheet("color:#64748B;")
        v.addWidget(j)
        v.addWidget(s)

        baris = QHBoxLayout()
        baris.setSpacing(8)
        baris.addWidget(QLabel("Filter shift:"))
        self.combo_filter_shift = QComboBox()
        self.combo_filter_shift.setMinimumWidth(160)
        self.combo_filter_shift.currentTextChanged.connect(self.refresh_tabel)
        baris.addWidget(self.combo_filter_shift)
        baris.addWidget(QLabel("Cari:"))
        self.in_cari = QLineEdit()
        self.in_cari.setPlaceholderText("nama atau ID, misal Andi / W01")
        self.in_cari.textChanged.connect(self.refresh_tabel)
        baris.addWidget(self.in_cari, 1)
        self.label_jumlah = QLabel("")
        self.label_jumlah.setObjectName("badgeShift")
        baris.addWidget(self.label_jumlah)
        btn_refresh = QPushButton("Refresh")
        btn_refresh.setObjectName("btnGaris")
        btn_refresh.clicked.connect(self.refresh_semua)
        baris.addWidget(btn_refresh)
        v.addLayout(baris)

        self.tabel = QTableWidget(0, 8)
        self.tabel.setHorizontalHeaderLabels(
            ["Nama", "ID", "Peran", "Shift", "Gaji", "Poin", "Aktivitas", "Layanan"]
        )
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabel.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabel.setAlternatingRowColors(True)
        self.tabel.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabel.verticalHeader().setVisible(False)
        v.addWidget(self.tabel, 2)

        v.addWidget(QLabel("Laporan resmi + riwayat pecat (memanggil cafe.laporan() asli):"))
        self.teks_laporan = QTextBrowser()
        v.addWidget(self.teks_laporan, 1)

        self.tab.addTab(w, "1. Data / Laporan")

    # ---------- Tab 2: Tambah (menu 1) ----------
    def buat_tab_tambah(self):
        w = QWidget()
        h = QHBoxLayout()
        h.setContentsMargins(14, 14, 14, 14)
        h.setSpacing(12)
        w.setLayout(h)

        kiri = QGroupBox("Formulir Pegawai Baru  —  Menu 1")
        f = QFormLayout()
        f.setSpacing(8)
        kiri.setLayout(f)

        self.in_nama = QLineEdit()
        self.in_nama.setPlaceholderText("misal: Eka")
        self.in_id = QLineEdit()
        self.in_id.setPlaceholderText("ID unik, misal: W02")
        self.in_gaji = QLineEdit()
        self.in_gaji.setPlaceholderText("angka positif, misal: 3000000")
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

        btn = QPushButton("＋  Tambah Pegawai")
        btn.setObjectName("btnHijau")
        btn.clicked.connect(self.tambah_pegawai)
        f.addRow(btn)
        h.addWidget(kiri, 3)

        tips = self._panel_tips(
            "Tata Tertib Pengisian",
            "1. Nama & ID wajib diisi, ID tidak boleh ganda.\n"
            "2. Gaji wajib angka positif (contoh: 3200000).\n"
            "3. Baker default spesialisasi \u201cPastry\u201d, Barista \u201cMenyeduh Kopi\u201d.\n"
            "4. Kosongkan \u201cShift baru\u201d bila memakai shift yang ada.\n"
            "5. Shift baru otomatis dibuat bila nama belum terdaftar.",
        )
        h.addWidget(tips, 2)
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
        h = QHBoxLayout()
        h.setContentsMargins(14, 14, 14, 14)
        h.setSpacing(12)
        w.setLayout(h)

        kiri = QVBoxLayout()
        box_cari = QGroupBox("Cari pegawai")
        hc = QHBoxLayout()
        self.in_eval_id = QLineEdit()
        self.in_eval_id.setPlaceholderText("ID dinilai, misal W01")
        btn_cari = QPushButton("Cari")
        btn_cari.setObjectName("btnGaris")
        btn_cari.clicked.connect(self.cari_eval)
        hc.addWidget(self.in_eval_id, 1)
        hc.addWidget(btn_cari)
        box_cari.setLayout(hc)
        kiri.addWidget(box_cari)

        self.label_eval_info = QLabel("Belum ada pegawai dipilih.")
        self.label_eval_info.setWordWrap(True)
        self.label_eval_info.setStyleSheet(
            "background:white; border:1px solid #CBD5E1; border-radius:8px; padding:10px;"
        )
        kiri.addWidget(self.label_eval_info)

        self.btn_nilai = QPushButton("★  Nilai +25  (StoreManager.evaluasi)")
        self.btn_nilai.setObjectName("btnEmas")
        self.btn_nilai.clicked.connect(self.nilai_pegawai)
        kiri.addWidget(self.btn_nilai)

        box_pecat = QGroupBox("Pecat bila poin = 100")
        h2 = QHBoxLayout()
        self.in_tanggal = QLineEdit()
        self.in_tanggal.setPlaceholderText("Tanggal pecat, misal 07-10-2026")
        self.btn_pecat = QPushButton("Pecat")
        self.btn_pecat.setObjectName("btnBahaya")
        self.btn_pecat.clicked.connect(self.pecat_pegawai)
        h2.addWidget(self.in_tanggal, 1)
        h2.addWidget(self.btn_pecat)
        box_pecat.setLayout(h2)
        kiri.addWidget(box_pecat)
        kiri.addStretch()

        kolom_kiri = QWidget()
        kolom_kiri.setLayout(kiri)
        h.addWidget(kolom_kiri, 3)

        tips = self._panel_tips(
            "Aturan Penilaian Formal",
            "• Setiap evaluasi menaikkan poin +25 (0 → 25 → 50 → 75 → 100).\n"
            "• Poin 100 berarti DIPECAT: pegawai dihapus dari shift\n"
            "  dan masuk arsip riwayat pemecatan.\n"
            "• Wajib isi tanggal pemecatan sebagai dokumen resmi.\n"
            "• Gunakan tombol Cari dulu untuk memastikan ID valid.",
        )
        h.addWidget(tips, 2)
        self.tab.addTab(w, "3. Evaluasi + Pecat")

    # ---------- Tab 4: Shift + Operasional (menu 4-5) ----------
    def buat_tab_shift_ops(self):
        w = QWidget()
        h = QHBoxLayout()
        h.setContentsMargins(14, 14, 14, 14)
        h.setSpacing(12)
        w.setLayout(h)

        box_shift = QGroupBox("Kelola shift  —  Menu 5")
        fs = QFormLayout()
        fs.setSpacing(8)
        self.in_shift_nama = QLineEdit()
        self.in_shift_nama.setPlaceholderText("misal: Malam")
        self.in_hapus_shift = QLineEdit()
        self.in_hapus_shift.setPlaceholderText("nama shift kosong yg dihapus")
        self.in_pindah_id = QLineEdit()
        self.in_pindah_id.setPlaceholderText("misal: W01")
        self.in_pindah_tujuan = QLineEdit()
        self.in_pindah_tujuan.setPlaceholderText("tujuan, misal: Sore")
        btn_buat = QPushButton("Buat shift baru")
        btn_buat.clicked.connect(self.buat_shift)
        btn_hapus = QPushButton("Hapus shift kosong")
        btn_hapus.setObjectName("btnBahaya")
        btn_hapus.clicked.connect(self.hapus_shift)
        btn_pindah = QPushButton("Pindahkan pegawai")
        btn_pindah.setObjectName("btnEmas")
        btn_pindah.clicked.connect(self.pindah_pegawai)
        fs.addRow("Nama shift baru:", self.in_shift_nama)
        fs.addRow(btn_buat)
        fs.addRow("Nama shift dihapus:", self.in_hapus_shift)
        fs.addRow(btn_hapus)
        fs.addRow("ID pegawai dipindah:", self.in_pindah_id)
        fs.addRow("Pindah ke shift:", self.in_pindah_tujuan)
        fs.addRow(btn_pindah)
        box_shift.setLayout(fs)
        h.addWidget(box_shift, 2)

        kanan = QVBoxLayout()
        lab = QLabel("Operasional harian  —  Menu 4 (cafe.operasional asli)")
        lab.setStyleSheet("font-weight:700; color:#1B2F4B;")
        kanan.addWidget(lab)
        self.teks_ops = QTextBrowser()
        kanan.addWidget(self.teks_ops, 1)
        kolom_kanan = QWidget()
        kolom_kanan.setLayout(kanan)
        h.addWidget(kolom_kanan, 3)

        self.tab.addTab(w, "4. Shift + Operasional")

    # ---------- Tab 5: Gaji (menu 6) ----------
    def buat_tab_gaji(self):
        w = QWidget()
        h = QHBoxLayout()
        h.setContentsMargins(14, 14, 14, 14)
        h.setSpacing(12)
        w.setLayout(h)

        kiri = QGroupBox("Penyesuaian Gaji  —  Menu 6 (set_gaji)")
        f = QFormLayout()
        f.setSpacing(8)
        kiri.setLayout(f)
        self.in_gaji_id = QLineEdit()
        self.in_gaji_id.setPlaceholderText("misal: K01")
        self.label_gaji_skr = QLabel("-")
        self.label_gaji_skr.setStyleSheet(
            "background:white; border:1px solid #CBD5E1; border-radius:6px; padding:7px;"
        )
        self.in_gaji_baru = QLineEdit()
        self.in_gaji_baru.setPlaceholderText("angka positif baru")
        btn_cek = QPushButton("Cek gaji sekarang")
        btn_cek.setObjectName("btnGaris")
        btn_cek.clicked.connect(self.cek_gaji)
        btn_ubah = QPushButton("Ubah gaji (set_gaji)")
        btn_ubah.clicked.connect(self.ubah_gaji)
        f.addRow("ID:", self.in_gaji_id)
        f.addRow(btn_cek)
        f.addRow("Gaji sekarang:", self.label_gaji_skr)
        f.addRow("Gaji baru:", self.in_gaji_baru)
        f.addRow(btn_ubah)
        h.addWidget(kiri, 3)

        tips = self._panel_tips(
            "Ketentuan Gaji",
            "• Gaji bersifat privat, diubah hanya via set_gaji().\n"
            "• Nominal harus angka positif, selain itu ditolak.\n"
            "• Klik \u201cCek gaji sekarang\u201d sebelum mengubah.\n"
            "• Perubahan tercatat otomatis di tabel Data.",
        )
        h.addWidget(tips, 2)
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
        self.perbarui_statistik()
        # Panggil fungsi asli tanpa mengubah logika, tampilkan outputnya.
        self.teks_laporan.setText(tangkap_cetak(self.cafe.laporan))
        self.teks_ops.setText(tangkap_cetak(self.cafe.operasional))

    def perbarui_statistik(self):
        total = sum(len(s.daftar) for s in self.cafe.jadwal)
        n_shift = len(self.cafe.jadwal)
        semua_gaji = [p.get_gaji() for s in self.cafe.jadwal for p in s.daftar]
        rata = sum(semua_gaji) / len(semua_gaji) if semua_gaji else 0
        n_pecat = len(self.cafe.riwayat_pecat)
        self.stat_total.setText(str(total))
        self.stat_shift.setText(str(n_shift))
        self.stat_gaji.setText(format_rupiah(rata) if rata else "-")
        self.stat_pecat.setText(str(n_pecat))

    def refresh_tabel(self):
        pilih = self.combo_filter_shift.currentText() if hasattr(self, "combo_filter_shift") else "Semua"
        kunci = self.in_cari.text().strip().lower() if hasattr(self, "in_cari") else ""
        baris = []
        for s in self.cafe.jadwal:
            if pilih not in ("", "Semua") and s.nama_shift != pilih:
                continue
            for p in s.daftar:
                if kunci and kunci not in p.nama.lower() and kunci not in p.id_pegawai.lower():
                    continue
                baris.append((s.nama_shift, p))
        self.tabel.setRowCount(len(baris))
        for i, (nama_shift, p) in enumerate(baris):
            self.tabel.setItem(i, 0, QTableWidgetItem(p.nama))
            self.tabel.setItem(i, 1, QTableWidgetItem(p.id_pegawai))
            self.tabel.setItem(i, 2, QTableWidgetItem(p.__class__.__name__))
            self.tabel.setItem(i, 3, QTableWidgetItem(nama_shift))
            self.tabel.setItem(i, 4, QTableWidgetItem(format_rupiah(p.get_gaji())))
            item_poin = QTableWidgetItem(str(p.get_poin()))
            item_poin.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            poin = p.get_poin()
            if poin >= 100:
                item_poin.setBackground(QColor("#F8D7D5"))
                item_poin.setForeground(QColor("#9E2B25"))
            elif poin >= 50:
                item_poin.setBackground(QColor("#F7EACD"))
                item_poin.setForeground(QColor("#7A5B1E"))
            else:
                item_poin.setBackground(QColor("#D9EAD9"))
                item_poin.setForeground(QColor("#2F6B4F"))
            self.tabel.setItem(i, 5, item_poin)
            self.tabel.setItem(i, 6, QTableWidgetItem(str(p.aktivitas())))
            self.tabel.setItem(i, 7, QTableWidgetItem(p.layani()))
        self.label_jumlah.setText(f"  {len(baris)} pegawai  ")
        if hasattr(self, "stat_total"):
            self.perbarui_statistik()

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
        self._set_status(f"Pegawai {nama} ({ide}) ditambahkan ke shift {s.nama_shift}.")
        self.refresh_semua()

    # ---------- Aksi: evaluasi (menu 3) ----------
    def cari_eval(self):
        ide = self.in_eval_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            self.label_eval_info.setText("Tidak ketemu (mungkin sudah dipecat).")
            return
        self.label_eval_info.setText(
            f"<b>{orang.nama}</b> ({orang.id_pegawai}) — {orang.__class__.__name__}<br>"
            f"Aktivitas: {orang.aktivitas()}<br>"
            f"Gaji: {format_rupiah(orang.get_gaji())} &nbsp;•&nbsp; Poin: <b>{orang.get_poin()}</b>"
        )

    def nilai_pegawai(self):
        ide = self.in_eval_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            QMessageBox.warning(self, "Gagal", "Tidak ketemu (mungkin sudah dipecat).")
            return
        hasil = self.manager.evaluasi(orang)
        QMessageBox.information(self, "Evaluasi", hasil)
        self.cari_eval()
        if orang.get_poin() >= 100:
            QMessageBox.information(
                self, "Poin 100",
                "Poin sudah 100. Isi tanggal lalu tekan Pecat.")
        self._set_status("Evaluasi: " + hasil)
        self.refresh_semua()
        self.cari_eval()

    def pecat_pegawai(self):
        ide = self.in_eval_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            QMessageBox.warning(self, "Gagal", "ID tidak ketemu.")
            return
        tgl = self.in_tanggal.text().strip() or "tanpa-tanggal"
        hasil = self.manager.pecat(self.cafe, ide, tgl)
        QMessageBox.information(self, "Pecat", hasil)
        self._set_status("Pemecatan: " + hasil)
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
        self._set_status(f"Shift {ns} dibuat.")
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
        self._set_status(f"Shift {ns} dihapus.")
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
        self._set_status(f"{orang.nama} pindah {asal.nama_shift} -> {tujuan.nama_shift}.")
        self.refresh_semua()

    # ---------- Aksi: gaji (menu 6) ----------
    def cek_gaji(self):
        ide = self.in_gaji_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            QMessageBox.warning(self, "Gagal", "Tidak ketemu.")
            return
        self.label_gaji_skr.setText(format_rupiah(orang.get_gaji()))

    def ubah_gaji(self):
        ide = self.in_gaji_id.text().strip()
        orang = self.cafe.cari_pegawai(ide)
        if orang is None:
            QMessageBox.warning(self, "Gagal", "Tidak ketemu.")
            return
        gaji = parse_gaji(self.in_gaji_baru.text())
        if orang.set_gaji(gaji):
            QMessageBox.information(self, "Berhasil", "Gaji baru: " + format_rupiah(orang.get_gaji()))
        else:
            QMessageBox.warning(self, "Ditolak", "Ditolak, harus angka positif.")
            return
        self.label_gaji_skr.setText(format_rupiah(orang.get_gaji()))
        self._set_status(f"Gaji {orang.nama} diubah menjadi {format_rupiah(orang.get_gaji())}.")
        self.refresh_semua()

    # ---------- Aksi: simpan / muat (menu 7) ----------
    def simpan(self):
        self.db.simpan(self.cafe)
        self._set_status("Tersimpan di " + self.db.path)
        QMessageBox.information(self, "Simpan", "Tersimpan di " + self.db.path)

    def muat_ulang(self):
        ok = self.db.muat(self.cafe)
        if not ok:
            QMessageBox.warning(self, "Gagal", "File tidak ada / rusak.")
            return
        self.refresh_semua()
        self._set_status("Dimuat dari " + self.db.path)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
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
