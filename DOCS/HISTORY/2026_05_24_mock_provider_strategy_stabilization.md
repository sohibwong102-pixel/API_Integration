# 📝 RIWAYAT IMPLEMENTASI: MOCKPROVIDER STRATEGY STABILIZATION

## 📅 Tanggal: 24 Mei 2026

## 🛠️ Status: SELESAI

## 🎯 Ringkasan singkat

Melakukan evaluasi nilai arsitektural `MockProvider` dan menstabilkan implementasi agar tidak menjadi sumber architecture drift jangka panjang akibat ketergantungan parsing prompt internal.

---

## 🔍 Architecture Assessment

Keputusan: **simplify + isolate MockProvider** (bukan retain-as-is, bukan remove total).

Alasan utama:
- `MockProvider` masih memiliki nilai nyata untuk:
  - offline development/testing
  - deterministic provider fallback development
  - isolated orchestration validation tanpa dependency network/API key
- Namun implementasi lama (regex parsing prompt section) memiliki biaya maintenance tinggi dan menimbulkan coupling ke format prompt.

Kesimpulan value vs cost:
- **value tetap ada**, tetapi hanya jika implementasi dibuat deterministic dan tidak parsing prompt internal.

---

## 📉 Drift Analysis

1. Parsing brittleness:
- Sebelumnya menggunakan regex extraction yang sensitif marker/section/wording.
- Perubahan kecil template prompt berpotensi langsung menggeser perilaku mock.

2. Provider behavior divergence:
- Provider real (`openai/gemini/ollama`) tidak parsing struktur internal prompt.
- Mock lama justru parsing section internal, sehingga divergence tinggi.

3. Prompt coupling:
- Mock lama ikut "terikat" pada evolusi prompt format.
- Menghambat prompt refactor karena harus sinkronisasi fake parser.

4. Maintenance burden:
- Menambah beban sinkronisasi yang tidak memberi nilai arsitektur langsung.
- Risiko menjadi long-term drift source jika dibiarkan.

---

## 🧩 Perubahan Implementasi

1. `services/ai/providers/mock_provider.py`
- Menghapus regex parsing dan manual section extraction sepenuhnya.
- Mengubah strategi ke deterministic fixture response.
- Menambahkan opsi env `MOCK_SUMMARY_FIXTURE` untuk override output testing tanpa ubah kode.

2. `.env.example`
- Menambahkan dokumentasi konfigurasi opsional `MOCK_SUMMARY_FIXTURE`.

---

## 🚦 Risk Categorization

- LOW:
  - Risiko mismatch format prompt di mock berkurang signifikan.
  - Contract output summary string menjadi lebih stabil.

- MEDIUM:
  - Realisme semantik mock menurun karena tidak lagi melakukan keyword simulation.

- HIGH:
  - Jika tim mengandalkan mock untuk menilai kualitas semantik model, hasil bisa misleading.

- CRITICAL:
  - Tidak ditemukan risiko critical baru setelah simplifikasi.

---

## ✅ Recommendation

Rekomendasi final: **simplify MockProvider** + **isolate purpose**.

Bukan:
- retain regex-heavy parser
- fake format-sensitive simulation

---

## 🧭 Alternative Strategy (jika suatu saat removal dipilih)

1. Replacement testing strategy:
- contract-based testing di level workflow/API response (`summary` string only)
- provider interface validation test (`BaseProvider.generate` contract)

2. TEST_EVIDENCE direction:
- simpan bukti uji per kategori (seperti pola `*_TEST/2026_05.md`)
- fokus pada response contract dan orchestration behavior, bukan prompt parser internals

3. Provider validation strategy:
- validasi fallback flow, error isolation, dan response sanitization
- bukan validasi parsing section prompt pada mock

4. Orchestration testing direction:
- uji routing primary/fallback menggunakan fixture deterministic
- jaga deterministic behavior untuk CI/offline

---

## ✍️ Implementor

- BACKEND_EXECUTOR (otomatis)
