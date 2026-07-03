"""
Module untuk class Buku.

Class ini merepresentasikan buku dalam perpustakaan.
"""

from dataclasses import dataclass


@dataclass
class Buku:
    """
    Class untuk buku dalam perpustakaan.
    
    Attributes:
        id: Unique identifier untuk buku
        judul: Judul buku
        penulis: Nama penulis buku
        penerbit: Nama penerbit buku
        tahun: Tahun terbit buku
        kategori: Kategori/genre buku
        stok: Jumlah stok buku yang tersedia
    """
    
    id: str
    judul: str
    penulis: str
    penerbit: str
    tahun: int
    kategori: str
    stok: int
    
    def __post_init__(self) -> None:
        """
        Validasi data setelah inisialisasi.
        
        Raises:
            ValueError: Jika validasi gagal
        """
        if not self.judul or not self.judul.strip():
            raise ValueError("Judul tidak boleh kosong")
        
        if not self.penulis or not self.penulis.strip():
            raise ValueError("Penulis tidak boleh kosong")
        
        if not isinstance(self.tahun, int):
            raise ValueError("Tahun harus berupa integer")
        
        if self.stok < 0:
            raise ValueError("Stok tidak boleh negatif")
    
    def tersedia(self) -> bool:
        """
        Mengecek apakah buku tersedia untuk dipinjam.
        
        Returns:
            True jika stok > 0, False jika tidak
        """
        return self.stok > 0
    
    def kurangi_stok(self, jumlah: int = 1) -> None:
        """
        Mengurangi stok buku.
        
        Args:
            jumlah: Jumlah stok yang akan dikurangi (default 1)
            
        Raises:
            ValueError: Jika stok tidak mencukupi
        """
        if self.stok < jumlah:
            raise ValueError("Stok buku tidak mencukupi")
        
        self.stok -= jumlah
    
    def tambah_stok(self, jumlah: int = 1) -> None:
        """
        Menambah stok buku.
        
        Args:
            jumlah: Jumlah stok yang akan ditambah (default 1)
            
        Raises:
            ValueError: Jika jumlah negatif
        """
        if jumlah < 0:
            raise ValueError("Jumlah penambahan stok tidak boleh negatif")
        
        self.stok += jumlah
