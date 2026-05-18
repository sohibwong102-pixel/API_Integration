# =====================================================================
# SYSTEM COMPONENT: PROMPT TEMPLATE LOADER (PENGURUS PROMPT TEMPLATE)
# =====================================================================
# Deskripsi:
# Berkas ini bertugas membaca berkas instruksi AI (.txt) dari disk/folder.
#
# Mengapa Prompt Dipisahkan dari Kode Python? (Konsep bagi Pemula):
# Menulis perintah AI (Prompt) langsung di dalam string Python membuat kode menjadi kotor
# dan sulit dibaca. Dengan memisahkannya ke file `.txt` eksternal:
# 1. Prompt Engineer / Product Manager bisa mengubah gaya bahasa AI dengan mudah tanpa 
#    menyentuh kode backend sama sekali.
# 2. Mencegah error sintaksis Python saat mengedit instruksi yang panjang.
# =====================================================================

import os
from pathlib import Path

# Mendapatkan base directory dari folder prompts secara absolut
PROMPTS_DIR = Path(__file__).resolve().parent

def load_prompt_template(filename: str) -> str:
    """
    Membaca berkas prompt template (.txt) dari folder prompts.
    
    Args:
        filename (str): Nama file prompt, misalnya 'issue_summary.txt'
        
    Returns:
        str: Isi template mentah (raw template)
    """
    file_path = PROMPTS_DIR / filename
    
    # 🛡️ PENGAMAN RUNTIME: Validasi apakah file ada sebelum dibaca
    # Jika filenya tidak sengaja terhapus atau typo, program akan melempar 
    # FileNotFoundError yang informatif alih-alih crash diam-diam.
    if not file_path.exists():
        raise FileNotFoundError(
            f"Prompt template '{filename}' tidak ditemukan di lokasi: {file_path}"
        )
        
    # Membaca berkas teks dengan encoding utf-8 agar karakter spesial terbaca aman
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def format_prompt(template: str, **variables) -> str:
    """
    Memformat template prompt mentah dengan menyisipkan variabel dinamis.
    
    Cara Kerja:
    Jika template berisi teks: "Halo {nama}, bagaimana kabar di {kota}?"
    Lalu dipanggil: format_prompt(template, nama="Budi", kota="Jakarta")
    Hasilnya: "Halo Budi, bagaimana kabar di Jakarta?"
    
    Args:
        template (str): Konten template prompt mentah dengan placeholder {}
        **variables: Variabel dinamis yang ingin dimasukkan (keyword arguments)
        
    Returns:
        str: Prompt matang yang siap dikirim langsung ke AI Service
    """
    try:
        # Menggunakan built-in method .format() milik string Python
        return template.format(**variables)
    except KeyError as e:
        # Menangkap error jika di template ada placeholder `{sesuatu}` 
        # tetapi kita lupa menyediakannya saat memanggil fungsi ini.
        raise ValueError(f"Gagal memformat prompt. Variabel wajib '{e}' tidak disediakan.")

