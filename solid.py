# ============================================================
# SOLID PRINCIPLES
# Sistem Manajemen Inventori Gudang
# ============================================================


# ============================================================
# 1. SRP - SINGLE RESPONSIBILITY PRINCIPLE
# ============================================================

class LaporanInventori:

    def buat_laporan(self, barang):
        return {
            "Nama Barang": barang.nama_barang,
            "Kategori": barang.kategori,
            "Stok": barang.stok,
            "Stok Minimum": barang.stok_minimum
        }


# ============================================================
# 2. OCP - OPEN/CLOSED PRINCIPLE
# ============================================================

class Notifikasi:

    def kirim(self, pesan):
        raise NotImplementedError


class NotifikasiStokRendah(Notifikasi):

    def kirim(self, pesan):
        return f"Peringatan: {pesan}"


class NotifikasiStokAman(Notifikasi):

    def kirim(self, pesan):
        return f"Stok aman: {pesan}"


def proses_notifikasi(notifikasi, pesan):
    return notifikasi.kirim(pesan)


# ============================================================
# 3. DIP - DEPENDENCY INVERSION PRINCIPLE
# ============================================================

class Penyimpanan:

    def simpan(self, data):
        raise NotImplementedError


class PenyimpananDatabase(Penyimpanan):

    def simpan(self, data):
        return f"Data berhasil disimpan: {data}"


class SistemInventori:

    def __init__(self, penyimpanan):
        self.penyimpanan = penyimpanan

    def simpan_data(self, data):
        return self.penyimpanan.simpan(data)