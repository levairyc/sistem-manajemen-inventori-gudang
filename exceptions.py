class InventoriException(Exception):
    """Exception dasar untuk sistem inventori."""
    pass


class StokTidakCukupException(InventoriException):
    """Exception ketika stok tidak mencukupi."""
    pass


class BarangTidakDitemukanException(InventoriException):
    """Exception ketika barang tidak ditemukan."""
    pass


class GudangTidakDitemukanException(InventoriException):
    """Exception ketika gudang tidak ditemukan."""
    pass