import pytest

from models import (
    Barang,
    BarangMasuk,
    BarangKeluar
)

from patterns import TransaksiFactory


# ============================================================
# 1. TEST TAMBAH STOK
# ============================================================

def test_tambah_stok():
    barang = Barang(
        nama_barang="Buku",
        kategori="ATK",
        stok=10,
        stok_minimum=5
    )

    barang.tambah_stok(5)

    assert barang.stok == 15


# ============================================================
# 2. TEST KURANGI STOK
# ============================================================

def test_kurangi_stok():
    barang = Barang(
        nama_barang="Buku",
        kategori="ATK",
        stok=10,
        stok_minimum=5
    )

    barang.kurangi_stok(3)

    assert barang.stok == 7


# ============================================================
# 3. TEST STOK TIDAK MENCUKUPI
# ============================================================

def test_stok_tidak_mencukupi():
    barang = Barang(
        nama_barang="Buku",
        kategori="ATK",
        stok=5,
        stok_minimum=2
    )

    with pytest.raises(ValueError):
        barang.kurangi_stok(10)


# ============================================================
# 4. TEST CEK STOK
# ============================================================

def test_cek_stok():
    barang = Barang(
        nama_barang="Pensil",
        kategori="ATK",
        stok=20,
        stok_minimum=5
    )

    assert barang.cek_stok() == 20


# ============================================================
# 5. TEST PERINGATAN STOK
# ============================================================

def test_peringatan_stok():
    barang = Barang(
        nama_barang="Pulpen",
        kategori="ATK",
        stok=3,
        stok_minimum=5
    )

    assert barang.cek_peringatan_stok() is True


# ============================================================
# 6. TEST BARANG MASUK
# ============================================================

def test_barang_masuk():
    barang = Barang(
        nama_barang="Buku",
        kategori="ATK",
        stok=10,
        stok_minimum=5
    )

    transaksi = BarangMasuk(barang, 5)

    hasil = transaksi.proses()

    assert barang.stok == 15
    assert hasil == "Barang berhasil diterima"


# ============================================================
# 7. TEST BARANG KELUAR
# ============================================================

def test_barang_keluar():
    barang = Barang(
        nama_barang="Buku",
        kategori="ATK",
        stok=10,
        stok_minimum=5
    )

    transaksi = BarangKeluar(barang, 4)

    hasil = transaksi.proses()

    assert barang.stok == 6
    assert hasil == "Barang berhasil dikeluarkan"


# ============================================================
# 8. TEST FACTORY BARANG MASUK
# ============================================================

def test_factory_barang_masuk():
    barang = Barang(
        nama_barang="Buku",
        kategori="ATK",
        stok=10,
        stok_minimum=5
    )

    transaksi = TransaksiFactory.buat_transaksi(
        "masuk",
        barang,
        5
    )

    transaksi.proses()

    assert barang.stok == 15


# ============================================================
# 9. TEST FACTORY BARANG KELUAR
# ============================================================

def test_factory_barang_keluar():
    barang = Barang(
        nama_barang="Buku",
        kategori="ATK",
        stok=10,
        stok_minimum=5
    )

    transaksi = TransaksiFactory.buat_transaksi(
        "keluar",
        barang,
        3
    )

    transaksi.proses()

    assert barang.stok == 7


# ============================================================
# 10. TEST FACTORY JENIS TRANSAKSI SALAH
# ============================================================

def test_factory_transaksi_tidak_valid():
    barang = Barang(
        nama_barang="Buku",
        kategori="ATK",
        stok=10,
        stok_minimum=5
    )

    with pytest.raises(ValueError):
        TransaksiFactory.buat_transaksi(
            "tidak_valid",
            barang,
            5
        )