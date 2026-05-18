# =====================================================================
# SYSTEM COMPONENT: LOCAL STORAGE (FILE-BASED / SISTEM FILE JSON)
# =====================================================================
# Deskripsi:
# Berkas ini bertindak sebagai "Mini Database" lokal kita.
# Sesuai target non-goals, kita tidak menggunakan database besar (seperti MySQL/Postgres)
# agar aplikasi tetap ringan, mudah dipelajari, dan langsung jalan tanpa instalasi tambahan.
#
# Cara Kerja:
# Seluruh log keluhan dan hasil AI disimpan ke dalam berkas `storage/history.json`.
# Berkas ini menyediakan fungsi untuk menulis data baru dan membaca semua riwayat.
# =====================================================================

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# 🌐 MENETAPKAN PATH SECARA ABSOLUT
# Penjelasan Pemula:
# Menggunakan string path relatif (seperti "./history.json") bisa memicu bug jika kita
# menjalankan program Python dari folder yang berbeda.
# Di bawah ini, kita memakai `Path(__file__).resolve()` untuk mendeteksi letak berkas 
# `local_storage.py` berada, lalu membuat file `history.json` tepat di folder yang sama.
STORAGE_DIR = Path(__file__).resolve().parent
DB_FILE = STORAGE_DIR / "history.json"

class LocalStorage:
    """
    Kelas Utility untuk mengelola baca-tulis file database JSON.
    Menggunakan static & classmethod agar dapat dipanggil langsung tanpa perlu instansiasi.
    """
    
    @staticmethod
    def _initialize_db():
        """
        Helper Internal: Menginisialisasi Database.
        
        Penjelasan Pemula:
        Sebelum membaca atau menulis, kita harus memastikan foldernya ada dan file
        JSON-nya tidak kosong. Jika file JSON kosong atau belum dibuat, kode kita
        bisa crash saat mencoba membaca JSON. Fungsi ini mengamankannya.
        """
        # 1. Pastikan folder penyimpanan (storage/) sudah dibuat
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        
        # 2. Jika file history.json belum ada di komputer, buat baru berisi list kosong `[]`
        if not DB_FILE.exists():
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    @classmethod
    def save_record(cls, original_text: str, summary: str) -> Dict[str, Any]:
        """
        Menyimpan entri keluhan baru beserta ringkasan AI-nya ke history.json.
        
        Args:
            original_text (str): Keluhan asli dari pengguna.
            summary (str): Rangkuman satu kalimat dari AI.
            
        Returns:
            dict: Objek data utuh yang baru saja disimpan (dilengkapi ID dan Waktu).
        """
        # Pastikan file database siap dipakai
        cls._initialize_db()
        
        # ─── LANGKAH 1: Ambil data lama ───
        # Kita baca dulu daftar keluhan lama agar tidak menumpuk/terhapus.
        records = cls.get_all_records()
        
        # ─── LANGKAH 2: Buat data baru ───
        # Auto-Increment ID: ID baru adalah jumlah data lama ditambah 1.
        record_id = len(records) + 1
        
        new_record = {
            "id": record_id,
            "timestamp": datetime.now().isoformat(), # Tanggal & waktu saat ini dalam format standar ISO
            "original_text": original_text,
            "summary": summary
        }
        
        # ─── LANGKAH 3: Tambahkan data baru dan Tulis ke disk ───
        records.append(new_record)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            # json.dump menulis list objek python ke format teks JSON yang rapi (indent=4)
            json.dump(records, f, indent=4, ensure_ascii=False)
            
        return new_record

    @classmethod
    def get_all_records(cls) -> List[Dict[str, Any]]:
        """
        Membaca seluruh riwayat transaksi dari file JSON database.
        
        Returns:
            list: List of dictionaries berisi seluruh data log keluhan.
        """
        # Pastikan database ada sebelum dibaca
        cls._initialize_db()
        
        try:
            # ─── LANGKAH 1: Buka dan Baca File JSON ───
            with open(DB_FILE, "r", encoding="utf-8") as f:
                # json.load menerjemahkan isi teks file JSON menjadi List di Python
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # ─── LANGKAH PENGAMANAN ───
            # Jika file JSON rusak, terhapus saat dibaca, atau error I/O lainnya,
            # kita tidak ingin aplikasi crash total. Kita kembalikan list kosong [] sebagai penyelamat.
            return []

