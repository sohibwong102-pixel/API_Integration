# 📝 RIWAYAT IMPLEMENTASI: PROMPT CONTRACT ALIGNMENT (SUMMARY ONLY)

## 📅 Tanggal: 24 Mei 2026

## 🛠️ Status: SELESAI

## 🎯 Ringkasan singkat:

Melakukan penyelarasan prompt output agar sepenuhnya sinkron dengan kontrak endpoint (`summary: str`) dan menghilangkan potensi pseudo-structured output yang menyebabkan ambiguity pada consumer.

---

## 🔍 Perubahan yang dilakukan

- Mengubah objective prompt agar eksplisit: output dipakai langsung sebagai nilai `summary` response API.
- Menegaskan aturan output:
  - hanya `one plain-text summary string`
  - tepat satu kalimat
  - tanpa heading/label/bullet/markdown/JSON
  - tanpa multi-section block
- Menghapus instruksi yang berpotensi memicu format semu/multi-bagian.
- Menyederhanakan instruksi agar lebih tegas dan tidak overlap.
- Mengetatkan guardrail panjang output:
  - dari maksimal 30 kata menjadi maksimal 25 kata.

---

## 📁 Berkas terpengaruh

- `prompts/issue_summary.txt`

---

## ✅ Dampak terhadap kontrak API

- Output AI sekarang diarahkan menjadi **1 response, 1 summary, 1 contract**.
- Mengurangi risiko mismatch bentuk output terhadap skema endpoint.
- Mengurangi dependency implisit terhadap parser format khusus.

---

## 🔁 Update tambahan: 24 Mei 2026 (Language Contract Consistency)

- Menyelaraskan fallback output saat informasi tidak cukup menjadi full English:
  - dari: `informasi tidak cukup`
  - menjadi: `not enough information`
- Tujuan: menjaga konsistensi dengan aturan output `Bahasa Inggris` dan mengurangi variasi lintas provider.

---

## 🔁 Update tambahan: 24 Mei 2026 (Mock Provider Alignment)

- Menyelaraskan `MockProvider` agar tidak melakukan parsing struktur internal prompt.
- Pendekatan baru: mengembalikan fixture summary deterministik (dapat dioverride via env `MOCK_SUMMARY_FIXTURE`).
- Tujuan: mencegah drift saat template prompt berubah dan menjaga kestabilan test/development offline.

---

## ✍️ Implementor

- BACKEND_EXECUTOR (otomatis)
