from models import BarangMasuk, BarangKeluar


# ============================================================
# FACTORY METHOD
# ============================================================

class TransaksiFactory:

    @staticmethod
    def buat_transaksi(jenis, barang, jumlah):

        if jenis == "masuk":
            return BarangMasuk(barang, jumlah)

        elif jenis == "keluar":
            return BarangKeluar(barang, jumlah)

        else:
            raise ValueError("Jenis transaksi tidak valid")


# ============================================================
# STRATEGY PATTERN
# ============================================================

class StrategiStok:

    def proses(self, barang, jumlah):
        raise NotImplementedError


class StrategiTambahStok(StrategiStok):

    def proses(self, barang, jumlah):
        barang.tambah_stok(jumlah)


class StrategiKurangiStok(StrategiStok):

    def proses(self, barang, jumlah):
        barang.kurangi_stok(jumlah)


class PengelolaStok:

    def __init__(self, strategi):
        self.strategi = strategi

    def proses(self, barang, jumlah):
        self.strategi.proses(barang, jumlah)