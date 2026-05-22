# AI_AGENT_RULES.md - Aturan untuk AI Coding Agents

Dokumen ini berisi pedoman ketat bagi AI Agent yang akan melakukan modifikasi pada codebase ini.

## 🧱 Batasan Tanggung Jawab
- **Frontend/UX**: Tombol dan pesan berada di `keyboards/` dan `handlers/`. Gunakan HTML tag (`<b>`, `<i>`, `<blockquote>`) untuk konsistensi visual.
- **Backend/Logic**: Logika berat harus berada di `services/`. Handler hanya bertugas mengatur aliran data (routing).

## 🚫 Larangan (Forbidden)
1. **DILARANG** mengakses `user_data.json` menggunakan library `json` secara langsung di dalam handler. Gunakan fungsi dari `utils/helpers.py`.
2. **DILARANG** menghapus pemanggilan fungsi `safe_delete_message` di dalam handler kecuali ada alasan UX yang sangat kuat.
3. **DILARANG** mengubah struktur kunci dalam dictionary `user_data` tanpa melakukan migrasi data pada user yang sudah ada.
4. **DILARANG** menambahkan library baru ke `requirements.txt` tanpa memastikan library tersebut bersifat *asynchronous*.

## 🛡️ Aturan Keamanan & Stabilitas
- **Callback Safety**: Pastikan `callback_data` tidak melebihi 64 bytes (Batasan Telegram). Gunakan singkatan jika perlu.
- **Refactor Safety**: Jika mengubah logika di `ai_service.py`, pastikan prompt tetap mempertahankan instruksi agar AI tidak memberikan kalimat basa-basi.
- **Database Safety**: Selalu gunakan `try-except` saat melakukan operasi file I/O pada `user_data.json` untuk mencegah bot mati total jika file terkunci atau korup.

## 🎨 Filosofi UX & Retensi
- **Clean Chat**: Chat history harus selalu bersih. Pesan lama yang sudah tidak relevan (seperti menu yang sudah ditinggalkan) harus di-edit atau di-delete.
- **Instant Response**: AI harus langsung menjawab pada poin utama. User tidak suka menunggu AI menyapa "Tentu, ini hasil tulisannya...".
- **Naming Consistency**: Gunakan bahasa Inggris untuk nama fungsi/variabel, namun gunakan Bahasa Indonesia untuk teks yang ditampilkan ke user.

## 📝 Aturan Penamaan
- Fungsi Keyboard: `get_{nama}_keyboard()`
- Fungsi Handler: `process_{action}()` atau `cmd_{command}()`
- Konstanta: `UPPER_CASE_WITH_UNDERSCORES`
- State: `StateName.waiting_for_{input_type}`
