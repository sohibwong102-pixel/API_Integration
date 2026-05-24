# =====================================================================
#  ____  ____  ____  ____   __  ____  ____  __   __ _   __   _     
# /  _ \(  _ \(  __)(  _ \ / _\(_  _)(_  _)/  \ (  ( \ / _\ ( \    
# (  <_> )   / ) _)  )   //    \ )(    )( (  O )/    //    \/ \_   
#  \____/(__\_)(____)(__\_)\_/\_/(__)  (__) \__/ \_)__)\_/\_/\____/
#
# OPERATIONAL WORKFLOW API (V1) - ENTRY POINT UTAMA
# =====================================================================
# Halo pemula! Selamat datang di kode sumber project ini. 
# Berkas `main.py` ini adalah "Pintu Gerbang" utama aplikasi kita.
# Di sinilah server web (Uvicorn) dinyalakan dan semua modul dihubungkan.
#
# =====================================================================
# 🗺️ PETA PERJALANAN REQUEST (ALUR LOGIK UTAMA)
# =====================================================================
# Ketika pengguna mengirim request (misal: mengirim keluhan server error):
#
#   [Langkah 1: main.py] 
#        │  Menerima request pertama kali dan mengarahkannya ke Router /api.
#        ▼
#   [Langkah 2: api/routes.py] 
#        │  Memvalidasi data input JSON menggunakan Pydantic. Jika valid,
#        │  mengirim data teks tersebut ke modul Workflow.
#        ▼
#   [Langkah 3: workflows/issue_summary.py]
#        │  Ini adalah "Dirigen" bisnis logik kita. Workflow melakukan koordinasi:
#        │  a. Mengambil template prompt khusus dari `/prompts`.
#        │  b. Memasukkan teks keluhan ke dalam template tersebut.
#        │  c. Memanggil AI Service untuk meringkas.
#        │  d. Menyimpan log kejadian ke Database File JSON di `/storage`.
#        ▼
#   [Langkah 4: prompts/loader.py] & [services/ai_service.py] & [storage/local_storage.py]
#        │  Menangani tugas spesifik (baca file, hubungi AI Mock, simpan JSON).
#        ▼
#   [Langkah 5: Kembali ke api/routes.py]
#           Memformat hasil akhir menjadi JSON dan mengirimkannya balik ke user!
# =====================================================================

import uvicorn
import logging
import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
from core import settings, register_error_handlers

logger = logging.getLogger("app.request")

# 🛡️ VALIDASI STARTUP KRITIS (Fail Fast)
# Memastikan semua variabel lingkungan yang wajib untuk provider aktif telah dikonfigurasi dengan benar.
settings.validate()

# 🚀 INGERT-POINT: Inisialisasi Aplikasi FastAPI
# FastAPI adalah framework Python modern, cepat (high-performance), untuk membuat API.
# Di sini kita memberi judul, penjelasan, dan menentukan URL dokumentasi otomatis.
app = FastAPI(
    title="Operational Workflow API",
    description=(
        "API Backend modular berorientasi workflow untuk memproses "
        "dan merangkum keluhan operasional sistem secara otomatis menggunakan AI."
    ),
    version="1.0.0",
    docs_url="/docs",      # URL untuk mengakses Swagger UI (Dokumentasi API interaktif)
    redoc_url="/redoc"     # URL untuk mengakses ReDoc UI (Format alternatif dokumen API)
)

# Registrasi Centralized Error Handlers
register_error_handlers(app)

# =====================================================================
# 🌐 MIDDLEWARE CORS (Cross-Origin Resource Sharing)
# =====================================================================
# Penjelasan untuk Pemula:
# Secara default, browser melarang website dari domain A memanggil API di domain B.
# Ini disebut kebijakan Same-Origin Policy untuk keamanan.
# CORS Middleware di bawah ini dipasang agar jika suatu saat Anda membuat frontend
# (misalnya dengan React/Vue/HTML biasa) yang berjalan di port berbeda, frontend tersebut
# tetap diizinkan untuk mengambil data dari backend FastAPI ini.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mengizinkan semua domain ("*") untuk kemudahan belajar di komputer lokal
    allow_credentials=True,
    allow_methods=["*"], # Mengizinkan semua metode HTTP (GET, POST, PUT, DELETE, dll)
    allow_headers=["*"], # Mengizinkan semua header HTTP kustom
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    # Gunakan request_id dari client jika ada; jika tidak, generate di API boundary.
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    request.state.request_id = request_id

    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)

    # Expose request id secara konsisten untuk correlation di sisi client.
    response.headers["X-Request-ID"] = request_id

    # Structured access log ringan untuk tracing & observability.
    logger.info(
        "request_completed",
        extra={
            "event": "request_completed",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response

# =====================================================================
# 🔀 REGISTRASI ROUTER MODULAR
# =====================================================================
# Kita memecah rute API ke berkas terpisah (`api/routes.py`) agar kode tidak menumpuk.
# Dengan `app.include_router(api_router, prefix="/api")`, semua rute yang didefinisikan
# di dalam `api/routes.py` secara otomatis akan diawali dengan `/api`.
# Contoh: rute `/issue-summary` menjadi `/api/issue-summary`.
app.include_router(api_router, prefix="/api")


# =====================================================================
# 🏠 RUTE ROOT (Halaman Utama / Selamat Datang)
# =====================================================================
@app.get("/", tags=["General"])
def read_root():
    """
    Rute root (/) ini sangat berguna untuk memverifikasi apakah server backend 
    sudah hidup atau mati. Jika diakses lewat browser di http://localhost:8000/,
    ia akan mengembalikan data JSON status 'online'.
    """
    return {
        "status": "online",
        "message": "Selamat datang di Operational Workflow API (V1)",
        "docs_swagger": "/docs",
        "docs_redoc": "/redoc",
        "available_endpoints": {
            "POST": "/api/issue-summary (Untuk meringkas keluhan)",
            "GET": "/api/history (Untuk melihat riwayat keluhan)"
        }
    }


# =====================================================================
# 🏃 PROGRAM UTAMA (MENJALANKAN SERVER)
# =====================================================================
# Blok kode di bawah ini memastikan bahwa berkas ini dapat dijalankan langsung
# menggunakan perintah: `python main.py` di terminal Anda.
# Tanpa blok ini, Anda harus mengetik perintah manual: `uvicorn main:app --reload`.
if __name__ == "__main__":
    print("---------------------------------------------------------")
    print("Memulai server Operational Workflow API V1...")
    print(f"Silakan buka browser dan akses http://{settings.APP_HOST}:{settings.APP_PORT}/docs")
    print("---------------------------------------------------------")
    
    uvicorn.run(
        "main:app", 
        host=settings.APP_HOST, 
        port=settings.APP_PORT, 
        reload=settings.APP_ENV == "development"  # reload otomatis aktif jika di mode development
    )
