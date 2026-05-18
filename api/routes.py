# =====================================================================
# SYSTEM COMPONENT: API ROUTING LAYER (LAPISAN ANTARMUKA / ENDPOINT)
# =====================================================================
# Deskripsi:
# Berkas ini mendefinisikan rute/endpoint API yang bisa diakses oleh client
# (seperti Postman, web frontend, aplikasi mobile, atau layanan pihak ketiga). 
# Lapisan ini bertugas menerima request, memvalidasi datanya, mengoper data 
# tersebut ke "Workflow" untuk diproses, lalu membalas dengan format yang rapi.
#
# Di sini kita menggunakan Pydantic untuk memastikan data input/output aman & tervalidasi.
# =====================================================================

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# Import workflow bisnis dan storage lokal
# Alur: Rute API akan memanggil Workflow, bukan langsung ke AI Service atau Storage.
from workflows import IssueSummaryWorkflow
from storage import LocalStorage

# Inisialisasi APIRouter dari FastAPI
# APIRouter bertindak sebagai "pengelompok rute". Ini membuat kode kita rapi
# karena rute-rute terkait dikelompokkan ke file tersendiri.
router = APIRouter()

# =====================================================================
# 📋 SKEMA PYDANTIC (SISTEM VALIDASI DATA OTOMATIS)
# =====================================================================
# Penjelasan untuk Pemula:
# Pydantic adalah library Python untuk validasi tipe data.
# Saat client mengirim data JSON ke API kita, Pydantic memastikan:
# 1. Apakah field yang wajib (required) sudah dikirim?
# 2. Apakah tipe datanya cocok (misal string, integer)?
# Jika tidak cocok, Pydantic otomatis membalas dengan error 422 (Unprocessable Entity).

class IssueRequest(BaseModel):
    """
    Skema data input untuk POST /api/issue-summary.
    Client wajib mengirim JSON dengan format:
    {
       "text": "isi keluhan di sini..."
    }
    """
    text: str = Field(
        ..., # Simbol '...' (ellipsis) menandakan field ini WAJIB diisi, tidak boleh absen
        description="Deskripsi teks keluhan/laporan isu sistem yang ingin dirangkum.",
        examples=["backend deploy gagal setelah update auth middleware"]
    )


class IssueResponse(BaseModel):
    """
    Skema data output untuk response POST /api/issue-summary.
    Menjamin client hanya akan menerima JSON dengan format terstruktur:
    {
       "summary": "Ringkasan hasil AI dalam satu kalimat..."
    }
    """
    summary: str = Field(
        ..., 
        description="Hasil ringkasan satu kalimat bahasa Inggris dari AI.",
        examples=["Deployment issue related to auth middleware conflict."]
    )


class HistoryRecordResponse(BaseModel):
    """
    Skema data output untuk tiap entri data riwayat pada GET /api/history.
    Mendefinisikan tipe data yang akan dikembalikan untuk setiap catatan log di database.
    """
    id: int = Field(..., description="ID unik dari riwayat keluhan (auto-increment)")
    timestamp: str = Field(..., description="Waktu kapan isu ini diproses (Format ISO)")
    original_text: str = Field(..., description="Teks keluhan asli dari pengguna")
    summary: str = Field(..., description="Hasil ringkasan dari AI")


# =====================================================================
# 🛠️ POST ENDPOINT: /issue-summary
# =====================================================================
@router.post(
    "/issue-summary", 
    response_model=IssueResponse, 
    status_code=status.HTTP_200_OK,
    summary="Ringkas laporan keluhan sistem",
    description="Endpoint ini menerima teks deskripsi issue, menjalankannya melalui workflow, dan mengembalikan summary satu kalimat."
)
def create_issue_summary(payload: IssueRequest):
    """
    Fungsi penanganan utama saat user memanggil POST /api/issue-summary.
    
    [ALUR LOGIKA POST REQUEST]:
    1. User mengirim JSON -> Pydantic `payload` (IssueRequest) memvalidasi strukturnya.
    2. Program memeriksa apakah teks kosong/hanya spasi.
    3. Program memanggil `IssueSummaryWorkflow.execute` (Otak Alur Bisnis).
    4. Workflow memproses dan mengembalikan kamus (dictionary) hasil.
    5. Program mengembalikan hasil tersebut dibungkus skema `IssueResponse`.
    """
    
    # ─── LANGKAH 1: Validasi manual tambahan ───
    # Jika user mengirim string kosong, spasi banyak saja ("   "), kita tolak.
    if not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Teks issue tidak boleh kosong atau hanya berupa spasi."
        )
        
    try:
        # ─── LANGKAH 2: Eksekusi Alur Kerja (Workflow) ───
        # Di sinilah integrasi terjadi. Kita melempar beban kerja ke workflow.
        # Perhatikan: Router TIDAK tahu bagaimana AI memprosesnya, Router hanya tahu memanggil execute().
        result = IssueSummaryWorkflow.execute(payload.text)
        
        # ─── LANGKAH 3: Kembalikan Response ke Client ───
        # Data diambil dari dictionary hasil workflow, lalu dimasukkan ke skema Pydantic.
        return IssueResponse(summary=result["summary"])
        
    except ValueError as ve:
        # Menangkap error bisnis yang sengaja kita lempar dari workflow (misal validasi internal)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        # Pengaman terakhir (Safe Guard) jika ada error server tak terduga (misal file database error/hilang)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kegagalan server internal: {str(e)}"
        )


# =====================================================================
# 📖 GET ENDPOINT: /history
# =====================================================================
@router.get(
    "/history", 
    response_model=List[HistoryRecordResponse],
    status_code=status.HTTP_200_OK,
    summary="Dapatkan riwayat ringkasan isu",
    description="Endpoint ini membaca seluruh database log JSON lokal dan mengembalikan daftar riwayat isu yang sudah diproses."
)
def get_issue_history():
    """
    Fungsi penanganan utama saat user memanggil GET /api/history.
    
    [ALUR LOGIKA GET REQUEST]:
    1. User meminta data riwayat.
    2. Program memanggil LocalStorage untuk mengambil list dari berkas `history.json`.
    3. List data JSON tersebut dikembalikan dan divalidasi otomatis oleh List[HistoryRecordResponse].
    """
    try:
        # Membaca data langsung dari layer LocalStorage
        records = LocalStorage.get_all_records()
        return records
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal membaca data riwayat: {str(e)}"
        )

