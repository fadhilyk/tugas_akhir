"""
Module untuk ReportService.

Service ini menangani pembuatan berbagai laporan perpustakaan.
"""

from typing import Any
from ..models import Buku, Anggota, Peminjaman
from .library_service import LibraryService


class ReportService:
    """
    Service untuk generate berbagai laporan perpustakaan.
    
    Attributes:
        _library_service: Instance LibraryService untuk mengakses data
    """
    
    def __init__(self, library_service: LibraryService) -> None:
        """
        Inisialisasi ReportService.
        
        Args:
            library_service: Instance LibraryService
        """
        self._library_service = library_service
    
    def laporan_semua_buku(self) -> list[dict[str, Any]]:
        """
        Generate laporan semua buku dalam perpustakaan.
        
        Returns:
            List dictionary berisi informasi semua buku
        """
        buku_list = self._library_service.daftar_buku()
        
        laporan = []
        for buku in buku_list:
            laporan.append({
                "id": buku.id,
                "judul": buku.judul,
                "penulis": buku.penulis,
                "penerbit": buku.penerbit,
                "tahun": buku.tahun,
                "kategori": buku.kategori,
                "stok": buku.stok,
                "status": "Tersedia" if buku.tersedia() else "Habis"
            })
        
        return laporan
    
    def laporan_buku_tersedia(self) -> list[dict[str, Any]]:
        """
        Generate laporan buku yang tersedia (stok > 0).
        
        Returns:
            List dictionary berisi informasi buku yang tersedia
        """
        buku_list = self._library_service.daftar_buku()
        
        laporan = []
        for buku in buku_list:
            if buku.tersedia():
                laporan.append({
                    "id": buku.id,
                    "judul": buku.judul,
                    "penulis": buku.penulis,
                    "penerbit": buku.penerbit,
                    "tahun": buku.tahun,
                    "kategori": buku.kategori,
                    "stok": buku.stok
                })
        
        return laporan
    
    def laporan_buku_dipinjam(self) -> list[dict[str, Any]]:
        """
        Generate laporan buku yang sedang dipinjam (stok = 0 atau ada peminjaman aktif).
        
        Returns:
            List dictionary berisi informasi buku yang sedang dipinjam
        """
        buku_list = self._library_service.daftar_buku()
        peminjaman_aktif = self._library_service.daftar_peminjaman(status="aktif")
        
        buku_dipinjam_ids = set()
        for peminjaman in peminjaman_aktif:
            buku_dipinjam_ids.add(peminjaman.buku_id)
        
        laporan = []
        for buku in buku_list:
            if buku.id in buku_dipinjam_ids:
                jumlah_dipinjam = sum(1 for p in peminjaman_aktif if p.buku_id == buku.id)
                laporan.append({
                    "id": buku.id,
                    "judul": buku.judul,
                    "penulis": buku.penulis,
                    "stok_tersisa": buku.stok,
                    "jumlah_dipinjam": jumlah_dipinjam
                })
        
        return laporan
    
    def laporan_anggota(self) -> list[dict[str, Any]]:
        """
        Generate laporan semua anggota perpustakaan.
        
        Returns:
            List dictionary berisi informasi semua anggota
        """
        anggota_list = self._library_service.daftar_anggota()
        
        laporan = []
        for anggota in anggota_list:
            laporan.append({
                "id": anggota.id,
                "nama": anggota.nama,
                "kontak": anggota.kontak,
                "alamat": anggota.alamat,
                "jumlah_pinjaman_aktif": anggota.jumlah_pinjaman()
            })
        
        return laporan
    
    def laporan_transaksi(self, status: str = None) -> list[dict[str, Any]]:
        """
        Generate laporan transaksi peminjaman.
        
        Args:
            status: Filter berdasarkan status ('aktif', 'selesai', atau None untuk semua)
            
        Returns:
            List dictionary berisi informasi transaksi
        """
        peminjaman_list = self._library_service.daftar_peminjaman(status=status)
        
        laporan = []
        for peminjaman in peminjaman_list:
            anggota = self._library_service._find_anggota_by_id(peminjaman.anggota_id)
            buku = self._library_service._find_buku_by_id(peminjaman.buku_id)
            
            laporan.append({
                "id": peminjaman.id,
                "anggota_id": peminjaman.anggota_id,
                "anggota_nama": anggota.nama if anggota else "Tidak Ditemukan",
                "buku_id": peminjaman.buku_id,
                "buku_judul": buku.judul if buku else "Tidak Ditemukan",
                "tanggal_pinjam": peminjaman.tanggal_pinjam.strftime("%Y-%m-%d %H:%M:%S"),
                "jatuh_tempo": peminjaman.jatuh_tempo.strftime("%Y-%m-%d %H:%M:%S"),
                "tanggal_kembali": peminjaman.tanggal_kembali.strftime("%Y-%m-%d %H:%M:%S") if peminjaman.tanggal_kembali else None,
                "status": peminjaman.status,
                "hari_terlambat": peminjaman.terlambat(),
                "denda": peminjaman.denda.nominal
            })
        
        return laporan
    
    def laporan_denda(self) -> list[dict[str, Any]]:
        """
        Generate laporan denda dari semua peminjaman.
        
        Returns:
            List dictionary berisi informasi denda
        """
        peminjaman_list = self._library_service.daftar_peminjaman()
        
        laporan = []
        for peminjaman in peminjaman_list:
            hari_terlambat = peminjaman.terlambat()
            
            if hari_terlambat > 0 or peminjaman.denda.nominal > 0:
                anggota = self._library_service._find_anggota_by_id(peminjaman.anggota_id)
                buku = self._library_service._find_buku_by_id(peminjaman.buku_id)
                
                laporan.append({
                    "peminjaman_id": peminjaman.id,
                    "anggota_id": peminjaman.anggota_id,
                    "anggota_nama": anggota.nama if anggota else "Tidak Ditemukan",
                    "buku_judul": buku.judul if buku else "Tidak Ditemukan",
                    "hari_terlambat": hari_terlambat,
                    "nominal_denda": peminjaman.denda.nominal,
                    "status_pembayaran": "Lunas" if peminjaman.denda.status_pembayaran else "Belum Lunas",
                    "tanggal_jatuh_tempo": peminjaman.jatuh_tempo.strftime("%Y-%m-%d"),
                    "status_peminjaman": peminjaman.status
                })
        
        return laporan
    
    def statistik_perpustakaan(self) -> dict[str, Any]:
        """
        Generate statistik umum perpustakaan.
        
        Returns:
            Dictionary berisi statistik perpustakaan
        """
        buku_list = self._library_service.daftar_buku()
        anggota_list = self._library_service.daftar_anggota()
        peminjaman_aktif = self._library_service.daftar_peminjaman(status="aktif")
        peminjaman_selesai = self._library_service.daftar_peminjaman(status="selesai")
        
        total_stok = sum(buku.stok for buku in buku_list)
        total_denda = sum(p.denda.nominal for p in self._library_service.daftar_peminjaman())
        
        return {
            "total_buku": len(buku_list),
            "total_stok": total_stok,
            "total_anggota": len(anggota_list),
            "total_peminjaman_aktif": len(peminjaman_aktif),
            "total_peminjaman_selesai": len(peminjaman_selesai),
            "total_peminjaman": len(peminjaman_aktif) + len(peminjaman_selesai),
            "total_denda": total_denda
        }
