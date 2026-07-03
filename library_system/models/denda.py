"""
Module untuk class Denda.

Class ini merepresentasikan denda keterlambatan pengembalian.
"""

from dataclasses import dataclass

DENDA_PER_HARI = 2000


@dataclass
class Denda:
    """
    Class untuk denda keterlambatan pengembalian buku.
    
    Attributes:
        nominal: Jumlah nominal denda dalam Rupiah
        status_pembayaran: Status pembayaran denda (True jika sudah dibayar)
    """
    
    nominal: int = 0
    status_pembayaran: bool = False
    
    def __post_init__(self) -> None:
        """
        Validasi data setelah inisialisasi.
        
        Raises:
            ValueError: Jika nominal negatif
        """
        if self.nominal < 0:
            raise ValueError("Nominal denda tidak boleh negatif")
    
    def hitung(self, hari_terlambat: int) -> int:
        """
        Menghitung nominal denda berdasarkan hari keterlambatan.
        
        Args:
            hari_terlambat: Jumlah hari keterlambatan
            
        Returns:
            Nominal denda yang harus dibayar
            
        Raises:
            ValueError: Jika hari terlambat negatif
        """
        if hari_terlambat < 0:
            raise ValueError("Hari terlambat tidak boleh negatif")
        
        self.nominal = hari_terlambat * DENDA_PER_HARI
        return self.nominal
    
    def bayar(self) -> None:
        """
        Menandai denda sebagai sudah dibayar.
        
        Raises:
            ValueError: Jika tidak ada denda yang harus dibayar
        """
        if self.nominal == 0:
            raise ValueError("Tidak ada denda yang harus dibayar")
        
        self.status_pembayaran = True
