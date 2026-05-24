# AI_AGENT_RULES.md

Dokumen ini berisi pedoman ketat bagi AI Agent yang memodifikasi codebase backend ini.

## Batasan Tanggung Jawab

- **API Layer**: Endpoint dan schema berada di `api/`. Fokusnya validasi HTTP, bukan business logic.
- **Workflow Layer**: Orchestration use case berada di `workflows/`.
- **Service Layer**: Integrasi provider AI berada di `services/`.
- **Storage Layer**: Persistensi file lokal hanya melalui `storage/local_storage.py`.

## Larangan

1. **DILARANG** meletakkan business logic berat di `api/routes.py`.
2. **DILARANG** membaca atau menulis `storage/history.json` langsung di luar `storage/local_storage.py`.
3. **DILARANG** menanam prompt besar langsung di workflow atau router. Gunakan `prompts/`.
4. **DILARANG** membuat coupling langsung workflow ke provider spesifik jika facade/router provider sudah tersedia.
5. **DILARANG** mengubah kontrak response API secara diam-diam tanpa menyesuaikan dokumentasi dan history.

## Aturan Keamanan & Stabilitas

- **Schema Safety**: Request dan response HTTP wajib tervalidasi dengan Pydantic.
- **Error Contract Safety**: Pertahankan format `success/error/code/message` untuk response error publik.
- **Provider Safety**: Jika menambah provider baru, daftarkan secara resmi di registry/router/config.
- **Storage Safety**: Operasi baca/tulis history harus tetap lewat `LocalStorage`.
- **Compatibility Safety**: Jaga endpoint legacy yang masih dipertahankan agar client existing tidak langsung patah.

## Filosofi Pengembangan

- Gunakan Bahasa Inggris untuk nama fungsi, class, variabel, dan enum.
- Gunakan Bahasa Indonesia untuk komentar edukatif jika memang membantu pembaca repo ini.
- Utamakan perubahan kecil, jelas, dan mudah ditelusuri.
- Selalu analisa dampak lintas `api -> workflows -> services -> storage` sebelum refactor.

## Aturan Penamaan

- Workflow class: `Issue{Name}Workflow`
- Response model: `{Name}Response`
- Provider adapter: `{Provider}Provider`
- Prompt template: `prompts/issue/{feature}.txt`
