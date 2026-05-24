# SYSTEM_BOUNDARIES.md

Dokumen ini mendefinisikan batas arsitektur backend agar modularitas tetap terjaga saat sistem berkembang.

## Core Architecture

Project menggunakan:
- FastAPI
- modular workflow architecture
- provider-agnostic AI routing
- separated prompt management
- local storage adapter
- simple request lifecycle

## Folder Responsibility

## `api/`
Tugas:
- routing HTTP
- validasi request
- validasi response
- request context boundary

JANGAN:
- business logic berat
- provider routing logic
- storage read/write langsung

## `workflows/`
Tugas:
- orchestration coordination
- prompt loading
- output normalization
- sequence bisnis per use case

JANGAN:
- HTTP transport handling
- raw provider selection logic
- direct file persistence manual

## `services/`
Tugas:
- AI integration
- provider routing
- reusable generation layer

JANGAN:
- workflow coordination
- HTTP response formatting
- business policy acak per endpoint

## `prompts/`
Tugas:
- centralized prompt storage
- reusable prompt templates
- prompt consistency

JANGAN:
- business logic
- storage logic
- routing logic

## `storage/`
Tugas:
- persistence layer
- history storage
- storage abstraction

JANGAN:
- orchestration logic
- provider execution
- API response behavior

## Safe Refactor Rules

Sebelum refactor:
- cek dependency impact ke `api/`, `workflows/`, `services/`, `storage/`
- cek contract request/response
- cek normalisasi output workflow
- cek konsistensi dokumentasi

JANGAN:
- pindahkan business logic ke router
- hard-code provider di workflow
- bypass prompt loader
- bypass storage adapter
- ubah public contract tanpa jejak dokumentasi
