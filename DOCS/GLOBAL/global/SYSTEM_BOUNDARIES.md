# SYSTEM BOUNDARIES

Dokumen ini mendefinisikan batas architecture project.

Tujuan utama:
- menjaga consistency
- mencegah chaos scaling
- mencegah dangerous refactor
- menjaga maintainability

---

# CORE ARCHITECTURE

Project menggunakan:
- aiogram v3
- modular architecture
- handler separation
- service layer
- reusable keyboards
- simple FSM
- simple-first architecture

---

# FOLDER RESPONSIBILITY

## handlers/
Tugas:
- routing
- interaction flow
- callback handling
- user communication

JANGAN:
- business logic berat
- database logic besar
- AI processing besar

---

## services/
Tugas:
- AI logic
- analytics
- payment
- processing
- reusable business logic

JANGAN:
- kirim UI langsung
- bikin navigation flow

---

## keyboards/
Tugas:
- semua inline keyboard
- reusable menu
- button structure

JANGAN:
- business logic
- AI logic

---

## states/
Tugas:
- FSM states
- conversation state

FSM wajib:
- sederhana
- predictable
- mudah cleanup

---

## utils/
Tugas:
- helper
- reusable utility
- formatter
- cleaner
- safe wrappers

---

# FSM BOUNDARIES

FSM hanya dipakai jika:
- benar-benar perlu state
- multi-step interaction

Hindari:
- nested FSM
- deep FSM chain
- overcomplicated flow

Prioritas:
- callback interaction
- inline action
- stateless UX jika memungkinkan

---

# CALLBACK RULES

Callback wajib:
- clean
- predictable
- scalable
- naming konsisten

Pattern:
feature_action

Contoh:
- tools_open
- premium_buy
- history_clear
- ai_generate

Hindari:
- callback random
- callback ambigu
- callback terlalu panjang

---

# SAFE REFACTOR RULES

Sebelum refactor:
- cek dependency
- cek import impact
- cek handler usage
- cek callback usage
- cek FSM impact

JANGAN:
- rename massal sembarangan
- ubah flow tanpa mapping
- pindah logic tanpa dependency check

---

# UI/UX BOUNDARIES

UX wajib:
- clean
- minimal
- fast
- mobile-first
- inline keyboard oriented

Hindari:
- spam message
- wall of text
- terlalu banyak emoji
- layout noisy

---

# PERFORMANCE PHILOSOPHY

Prioritas:
1. simplicity
2. responsiveness
3. maintainability
4. scalability

Bukan:
- premature optimization
- overengineering

---

# DEBUGGING RULES

Saat debugging:
- cari root cause
- jangan rewrite total
- jangan refactor brutal
- fix seminimal mungkin
- preserve architecture existing

---

# AGENT BEHAVIOR RULES

Jika AI Agent membaca repository ini:
- wajib menghormati architecture existing
- wajib mempertimbangkan retention
- wajib mempertimbangkan UX philosophy
- wajib menghindari overengineering
- wajib menjaga modular consistency

Agent HARUS:
- berpikir sebagai system architect
- berpikir sebelum coding
- menganalisa dependency dulu
- menganalisa impact dulu

---

# ABSOLUTE PROHIBITIONS

JANGAN:
- ubah architecture tanpa alasan kuat
- bikin abstraction tidak perlu
- bikin system terlalu enterprise
- bikin flow ribet
- bikin dependency coupling tinggi

SELALU:
- simple-first
- retention-oriented
- UX-focused
- modular
- maintainable