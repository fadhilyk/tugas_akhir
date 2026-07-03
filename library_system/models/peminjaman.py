"""
Module untuk class Peminjaman.

Class ini merepresentasikan transaksi peminjaman buku.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from .denda import Denda, DENDA_PER_HARI

LAMA_PINJAM = 7


@dataclass
class Peminjaman:
    """
    Class untuk transaksi peminjaman buku.
    
    Attributes:
        id: Unique identifier untuk peminjaman
        anggota_id: ID anggota yang meminjam
        buku_id: ID buku yang dipinjam
        tanggal_pinjam: Tanggal peminjaman
        jatuh_tempo: Tanggal jatuh tempo pengembalian
        tanggal_kembali: Tanggal pengembalian aktual (None jika belum dikembalikan)
        status: Status peminjaman (aktif/selesai)
        denda: Object Denda untuk keterlambatan
    """
    
    id: str
    anggota_id: str
    buku_id: str
    tanggal_pinjam: datetime
    jatuh_tempo: datetime
    tanggal_kembali: Optional[datetime] = None
    status: str = "aktif"
    denda: Denda = field(default_factory=Denda)
    
    def __post_init__(self) -> None:
        """
        Validasi dan set default values setelah inisialisasi.
        
        Raises:
            ValueError: Jika tanggal tidak valid
        """
        if self.jatuh_tempo <= self.tanggal_pinjam:
            raise ValueError("Jatuh tempo harus setelah tanggal pinjam")
        
        if self.tanggal_kembali and self.tanggal_kembali < self.tanggal_pinjam:
            raise ValueError("Tanggal kembali tidak boleh sebelum tanggal pinjam")
    
    @staticmethod
    def buat_peminjaman(id: str, anggota_id: str, buku_id: str, 
                        tanggal_pinjam: Optional[datetime] = None) -> "Peminjaman":
        """
        Factory method untuk membuat peminjaman baru dengan jatuh tempo otomatis.
        
        Args:
            id: ID peminjaman
            anggota_id: ID anggota
            buku_id: ID buku
            tanggal_pinjam: Tanggal pinjam (default: sekarang)
            
        Returns:
            Instance Peminjaman baru
        """
        if tanggal_pinjam is None:
            tanggal_pinjam = datetime.now()
        
        jatuh_tempo = tanggal_pinjam + timedelta(days=LAMA_PINJAM)
        
        return Peminjaman(
            id=id,
            anggota_id=anggota_id,
            buku_id=buku_id,
            tanggal_pinjam=tanggal_pinjam,
            jatuh_tempo=jatuh_tempo
        )
    
    def terlambat(self) -> int:
        """
        Menghitung jumlah hari keterlambatan.
        
        Returns:
            Jumlah hari keterlambat (0 jika tidak terlambat)
        """
        tanggal_acuan = self.tanggal_kembali if self.tanggal_kembali else datetime.now()
        
        if tanggal_acuan <= self.jatuh_tempo:
            return 0
        
        selisih = tanggal_acuan - self.jatuh_tempo
        return selisih.days
    
    def hitung_denda(self) -> int:
        """
        Menghitung denda keterlambatan.
        
        Returns:
            Nominal denda yang harus dibayar
        """
        hari_terlambat = self.terlambat()
        return self.denda.hitung(hari_terlambat)
    
    def tandai_dikembalikan(self, tanggal_kembali: Optional[datetime] = None) -> None:
        """
        Menandai buku sudah dikembalikan dan menghitung denda jika terlambat.
        
        Args:
            tanggal_kembali: Tanggal pengembalian (default: sekarang)
            
        Raises:
            ValueError: Jika peminjaman sudah selesai
        """
        if self.status == "selesai":
            raise ValueError("Peminjaman sudah selesai")
        
        if tanggal_kembali is None:
            tanggal_kembali = datetime.now()
        
        if tanggal_kembali < self.tanggal_pinjam:
            raise ValueError("Tanggal kembali tidak boleh sebelum tanggal pinjam")
        
        self.tanggal_kembali = tanggal_kembali
        self.status = "selesai"
        self.hitung_denda()
