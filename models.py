from abc import ABC, abstractmethod

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# ============================================================
# CLASS BARANG
# ============================================================

class Barang(Base):
    __tablename__ = "barang"

    id_barang = Column(Integer, primary_key=True, index=True)
    nama_barang = Column(String, nullable=False)
    kategori = Column(String, nullable=False)
    stok = Column(Integer, default=0)
    stok_minimum = Column(Integer, default=0)

    def tambah_stok(self, jumlah):
        self.stok += jumlah

    def kurangi_stok(self, jumlah):
        if jumlah > self.stok:
            raise ValueError("Stok tidak mencukupi")

        self.stok -= jumlah

    def cek_stok(self):
        return self.stok

    def cek_peringatan_stok(self):
        return self.stok <= self.stok_minimum


# ============================================================
# CLASS GUDANG
# ============================================================

class Gudang(Base):
    __tablename__ = "gudang"

    id_gudang = Column(Integer, primary_key=True, index=True)
    nama_gudang = Column(String, nullable=False)
    lokasi = Column(String, nullable=False)


# ============================================================
# CLASS STOK GUDANG
# ============================================================

class StokGudang(Base):
    __tablename__ = "stok_gudang"

    id_stok = Column(Integer, primary_key=True, index=True)

    id_barang = Column(
        Integer,
        ForeignKey("barang.id_barang"),
        nullable=False
    )

    id_gudang = Column(
        Integer,
        ForeignKey("gudang.id_gudang"),
        nullable=False
    )

    stok = Column(Integer, default=0)

    barang = relationship("Barang")
    gudang = relationship("Gudang")


# ============================================================
# ABSTRACT CLASS TRANSAKSI
# ============================================================

class TransaksiBarang(ABC):

    def __init__(self, barang, jumlah):
        self.barang = barang
        self.jumlah = jumlah

    @abstractmethod
    def proses(self):
        pass


# ============================================================
# INHERITANCE: BARANG MASUK
# ============================================================

class BarangMasuk(TransaksiBarang):

    def proses(self):
        self.barang.tambah_stok(self.jumlah)

        return "Barang berhasil diterima"


# ============================================================
# INHERITANCE: BARANG KELUAR
# ============================================================

class BarangKeluar(TransaksiBarang):

    def proses(self):
        self.barang.kurangi_stok(self.jumlah)

        return "Barang berhasil dikeluarkan"