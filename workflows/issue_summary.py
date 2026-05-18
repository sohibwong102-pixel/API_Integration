# =====================================================================
# SYSTEM COMPONENT: WORKFLOW (ALUR BISNIS / UTAMA KOORDINASI)
# =====================================================================
# Deskripsi:
# Berkas ini mendefinisikan Workflow (alur kerja/bisnis logika) untuk meringkas issue.
# Alur bisnis ini berfungsi sebagai "Dirigen" (Conductor) yang mengatur orkestrasi
# antar berbagai komponen sistem. 
#
# Ingat prinsip Loose Coupling: kelas ini tidak tahu detil bagaimana file dibaca,
# bagaimana AI bekerja, atau bagaimana JSON ditulis. Dia hanya mengoordinasikan!
#
# Peta Orkestrasi yang Dijalankan:
# API Router ──► [Workflow] 
#                  ├─► 1. Baca berkas template (.txt) di prompts/
#                  ├─► 2. Sisipkan teks issue ke template prompt
#                  ├─► 3. Panggil AI Service (Mock/Gemini/OpenAI) -> Dapatkan summary
#                  ├─► 4. Simpan riwayat ke file JSON di storage/
#                  └─► 5. Kembalikan data hasil ke API Router
# =====================================================================

from typing import Dict, Any
from prompts import load_prompt_template, format_prompt
from services import get_ai_service
from storage import LocalStorage

class IssueSummaryWorkflow:
    """
    Kelas koordinasi utama untuk memproses isu.
    Mengikuti prinsip Single Responsibility, kelas ini hanya fokus mengatur alur.
    """
    
    @classmethod
    def execute(cls, text: str) -> Dict[str, Any]:
        """
        Mengeksekusi alur pemrosesan isu dari awal hingga selesai.
        
        Args:
            text (str): Teks keluhan sistem (misal: "Database mati mendadak")
            
        Returns:
            dict: Berisi ringkasan serta log penyimpanan transaksi yang sukses.
        """
        # 🛡️ VALIDASI AWAL: Mencegah parameter kosong lolos ke dalam alur pemrosesan.
        if not text or not text.strip():
            raise ValueError("Input text tidak boleh kosong.")
            
        # =====================================================================
        # 📥 LANGKAH 1: BACA TEMPLATE PROMPT (.txt)
        # =====================================================================
        # Penjelasan: Kita memisahkan teks instruksi LLM (prompt) ke file txt terpisah
        # di folder `/prompts/` agar mudah dimodifikasi tanpa mengganggu kode Python kita.
        # Di sini kita memanggil helper untuk membaca file "issue_summary.txt".
        template = load_prompt_template("issue_summary.txt")
        
        # =====================================================================
        # ✏️ LANGKAH 2: SISIPKAN TEKS KELUHAN KE TEMPLATE
        # =====================================================================
        # Penjelasan: Template mentah dibaca dari disk, lalu kita gunakan helper
        # format_prompt untuk menaruh variabel `text` milik user ke dalam placeholder `{text}`.
        formatted_prompt = format_prompt(template, text=text)
        
        # =====================================================================
        # 🤖 LANGKAH 3: AMBIL SERVICE AI & GENERATE RINGKASAN
        # =====================================================================
        # Penjelasan: 
        # a. Kita memanggil get_ai_service() untuk meminta "siapapun AI yang aktif saat ini".
        #    Fungsi factory ini mengembalikan objek yang mengimplementasikan BaseAIService.
        # b. Kita mengirim prompt yang sudah terformat ke method `generate_summary`.
        ai_service = get_ai_service()
        summary = ai_service.generate_summary(formatted_prompt)
        
        # =====================================================================
        # 💾 LANGKAH 4: SIMPAN HASIL TRANSAKSI KE DATABASE JSON LOKAL
        # =====================================================================
        # Penjelasan: Untuk keperluan audit dan menu history, kita menyimpan teks asli
        # dari user berserta teks rangkuman buatan AI ke database file JSON lokal.
        saved_record = LocalStorage.save_record(original_text=text, summary=summary)
        
        # =====================================================================
        # 📤 LANGKAH 5: BALIKKAN DATA DENGAN STRUKTUR RAPI
        # =====================================================================
        # Penjelasan: Hasil akhir dikemas dalam dictionary dan dikirim kembali ke
        # api/routes.py agar bisa dikirim sebagai JSON ke pengguna.
        return {
            "summary": summary,
            "record": saved_record  # Menyertakan info record untuk kebutuhan visualisasi di frontend/client
        }

