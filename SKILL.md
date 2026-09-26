---
name: proposal-skripsi
description: |
  Menyusun **proposal penelitian dalam Bahasa Indonesia** untuk **skripsi, thesis (magister), atau disertasi** — dipilih pengguna. Sumber data & bukti diambil dari **kumpulan file lokal** (PDF, DOCX, MD, TXT, CSV, XLSX, JSON) di folder yang ditunjuk, ditambah pencarian online pelengkap bila literatur lokal minim. Pipeline menghasilkan **BAB I Pendahuluan, BAB II Tinjauan Pustaka, BAB III Metode Penelitian** lengkap, plus halaman judul, kerangka berpikir, rancangan analisis statistik dari dataset, daftar isi, dan ekspor **Markdown + DOCX (pandoc)**. Trigger: "proposal skripsi", "proposal tesis", "proposal disertasi", "bikin proposal", "susun bab 1", "tulis bab 2", "bab 3 metode", "rumusan masalah", "tujuan penelitian", "manfaat penelitian", "latar belakang", "kerangka teori", "tinjauan pustaka", "landasan teori", "hipotesis", "variabel penelitian", "desain penelitian", "metode penelitian", "sampling", "teknik pengumpulan data", "instrumen", "uji statistik", "rancangan analisis", "analisis dataset", "dari folder ini", "proposal dari data csv", "research proposal", "thesis proposal", "dissertation proposal", "make a proposal from my folder". Mode input: Folder (wajib) / Folder+Online. Semua angka statistik wajib berasal dari file dataset nyata, bukan karangan.
---

# Proposal Skripsi — Penyusun Proposal Penelitian (Bahasa Indonesia)

Skill ini menyusun **proposal penelitian berbahasa Indonesia** untuk tiga jenjang —
**skripsi (S1)**, **thesis (S2)**, dan **disertasi (S3)** — sesuai pilihan pengguna. Seluruh
bukti (literatur, data, statistik) disumberkan dari **kumpulan file lokal** yang ditunjuk user
(PDF/DOCX/MD/TXT/CSV/XLSX/JSON), dengan **pencarian online sebagai pelengkap** bila folder
minim literatur.

Mandat utama skill ini: **menghasilkan proposal yang siap dibawa ke pembimbing** — bukan
ringkasan, bukan kerangka kosong. Setiap klaim empiris memiliki sumber file, dan setiap
unsur proposal punya justifikasi, dan jenjang menentukan tingkat kedalaman.

> Skill ini **berkumpulan dengan** dua skill lain (bukan duplikat):
> - **`paper-review`** → tabel review literatur (synthesis matrix) bila user butuh matriks
>   evidence lengkap per paper. Skill ini достаikan **ringkasan** matriks saja.
> - **`academic-writing`** → protocol penulisan paper (English). **Tidak dipakai di sini**;
>   output skill ini wajib **Bahasa Indonesia**.

---

## Jenjang (Wajib Dipilih User — GATE 0)

| Aspek | **Skripsi (S1)** | **Thesis (S2)** | **Disertasi (S3)** |
|-------|------------------|-----------------|---------------------|
| Panjang proposal | 20–30 halaman (±3.500–5.000 kata) | 40–60 halaman (±8.000–12.000 kata) | 70–120 halaman (±15.000–25.000 kata) |
| Kontribusi utama | **Penerapan/pengujian** teori pada konteks lokal | **Pengembangan/ekspansi** kerangka konseptual | **Kontribusi teoretis orisinal** (model/kerangka baru) |
| Desain dominan | Kuantitatif eksplanatif atau deskriptif, penelitian lapangan, eksploratif kualitatif | Kualitatif (studi kasus, grounded theory) / mixed-methods | Mixed-methods, multi-situs, validasi model, replikasi |
| Landasan teori | 1-2 teori utama + teori pendukung | 2-4 teori, elaborasi hubungan antarteori | 3-5 teori + posisi teoretis (positioning) eksplisit |
| Pengujian | Uji statistik baku (regresi, t-test, ANOVA, SEM) | Uji kualitatif (coding, validitas, reliabilitas) + uji statistik bila kuantitatif | Uji empiris berlapis + **threat to validity** eksplisit |
| Wajib tambahan | Persetujuan etik, rencana kuota dan waktu | Kerangka konseptual, strategi generalisasi | Statement of contribution, gagasan orisinal, rencana publikasi (3-4 artikel) |
| Luas sub-bab BAB II | 5–7 sub-bab | 6–9 sub-bab | 7–10 sub-bab |

**Jika jenjang tidak disebut user → TANYAKAN (via `question` tool). Jangan menebak.**

---

## Pipeline

```text
STEP 0: KLARIFIKASI  → jenjang, bidang, topik, jenis penelitian, folder sumber, mode, format ekspor
STEP 1: INVENTARIS   → scan folder → klasifikasi (literatur/data/pedoman/format) → inventaris.json
STEP 2: EVIDENSI     → matriks ringkas + gap (TAS) + online search pelengkap bila perlu
STEP 3: FORMULASI    → latar belakang → rumusan masalah → tujuan → manfaat → pertanyaan → hipotesis → variabel → batasan
STEP 4: RANCANGAN    → desain metode + instrumen + sampling + teknik analisis + analisis dataset nyata
STEP 5: DRAFT        → halaman judul + daftar isi + BAB I–III (Markdown)
STEP 6: GATE+EXPORT  → quality gate → referensi → revisi → MD + DOCX (pandoc) + lampiran
```

Setiap tahap punya **quality gate**; konfirmasi user hanya diminta **satu kali di awal** (Step 0)
dan **satu kali sebelum export** (Step 6). Jangan konfirmasi per-bagian.

---

## STEP 0 — Klarifikasi

Kumpulkan parameter berikut (cukup seperlunya bila konteks sudah jelas dari brief user):

| Parameter | Opsi | Default |
|-----------|------|---------|
| **Jenjang** | Skripsi / Thesis / Disertasi | **wajib ditanya** |
| Bidang ilmu / program studi | teks bebas | — |
| Topik penelitian | teks bebas | dari brief user |
| Jenis penelitian | Kuantitatif / Kualitatif / Mixed-methods / R&D / Studi Kasus / Penelitian Tindakan | dataset ada → cenderung kuantitatif; tidak ada → kualitatif |
| **Folder sumber** | path | **wajib ditanya bila tidak disebut** |
| Mode input | Folder / Folder + Online | Folder (+Online bila literatur lokal < 10) |
| Luas proposal | Pendahuluan saja / BAB I–II / **BAB I–III lengkap** | BAB I–III |
| Template kampus | Ada file pedoman/format? path | tanpa template → pakai `templates/proposal_template.md` |
| Gaya sitasi | APA 7 / Chicago / Harvard / Vancouver / IEEE | APA 7 (standar kebanyakan kampus) |
| Ekspor | MD saja / **MD + DOCX (pandoc)** / + LaTeX | MD + DOCX |
| Nama/NIM dan institution | teks | `[isi ...]` bila tidak ada (jangan dikarang) |

> **Jangan pernah mengarang** nama fakultas/jurusan, nama dosen, NIM, atau nama responden.
> Tidak diketahui → tulis `[isi nama fakultas/jurusan]`, `[isi NIM]`, dsb.

Simpan hasil klarifikasi ke `kontrak_proposal.json` (kontrak kerja) sebelum lanjut.

---

## STEP 1 — Inventarisasi Sumber File

> Load `references/data-sources.md` untuk detail klasifikasi & ekstraksi.
> Script: `scripts/ingest_sources.sh <folder> [--out <cache>]`

1. Scan folder **rekursif**. Klasifikasikan tiap file:

| Kategori | Ekstensi | Pemanfaatan |
|----------|----------|--------------|
| **Literatur** | `pdf`, `docx`, `md`, `txt`, `tex`, `epub` (lewati) | BAB II + latar belakang + argumen gap |
| **Data kuantitatif** | `csv`, `tsv`, `xlsx`, `xls`, `json` (array of objects), `sav` | BAB III: rancangan analisis + profil data |
| **Pedoman/format** | `docx`, `pdf` bernama pedoman/skripsi/format/…)
| Aturan/Ethics | `*.md` | versi bab, pedoman sitasi |
| **Lainnya** | gambar, `pptx`, `zip`, kode | catat di inventaris, jangan dipaksa |

2. Ekstrak teks PDF: `scripts/ingest_sources.sh` memakai `pdftotext -layout` (poppler).
   PDF hasil scan → kosong → tandai `PERLU_OCR`, jangan dippeduli diam-diam.
3. **Batas baca yang wajib dihormati** (hemat konteks):
   - Literatur: **Abstract → Pendahuluan/Intro → Metode → Hasil → Kesimpulan** (cukup).
   - Bab II **tidak** menyalin isi paper; ia **membangun sintesis** (lihat Step 3).
4. Deteksi cepat: file apa pun yang menyebut "data responden", "jawaban", "skor", "Likert",
   "n = " → kemungkinan dataset; masukkan kategori Data.

### Output Step 1
```
kontrak_proposal.json        # hasil klarifikasi Step 0
sumber_inventaris.json       # master inventaris: path, kategori, ukuran, status ekstraksi, ringkasan
sumber_inventaris.md         # tabel inventaris + catatan kelengkapan
.cache_ekstrak/              # teks hasil ekstraksi PDF (file .txt), boleh dihapus setelah draft
```

### Quality Gate 1
- [ ] Semua file terklasifikasi; tidak ada file "misterius" tanpa penjelasan
- [ ] Setiap literatur punya minimal judul + tahun (dari metadata file atau halaman judul)
- [ ] Setiap dataset punya nama file + jumlah baris/kolom terverifikasi (lihat Step 4)
- [ ] File tidak terbaca (scan/gambar) ditandai eksplisit, bukan diabaikan

---

## STEP 2 — Bukti & Research Gap

### 2.1 Matriks bukti (ringkas — versi lengkap: pakai skill `paper-review`)

Untuk setiap literatur lokal, buat **1 baris ringkas** di `matriks_evidence.md` dengan kolom:

| Sumber | Tahun | Populasi/Sampel | Metode | Temuan Utama | Keterbatasan | Gap yang Tersisa |
|--------|-------|------------------|--------|--------------|--------------|------------------|

> Bila user minta tabel review lengkap per-paper (12 kolom, provenance `[M-2]`, ekspor
> CSV/XLSX/BIB/RIS) → **delegasikan ke skill `paper-review`**, jangan diulang di sini.

### 2.2 Pencarian online pelengkap (opsional)

Aktifkan bila: literatur lokal < 10, atau gap belum tertutup, atau user memintanya.
Load `references/online-search.md`. Ringkas saja: 5-10 paper terkuat dengan skor relevansi minimal 7,
DOI wajib dapat di-resolve. Hasil search **tidak boleh mendominasi** proposal bila data lokal
sudah kaya — literatur lokal lebih relevan (konteks Indonesia/lokal).

### 2.3 Menyusun Gap (metode TAS / Berwald-Daellenbach)

Template ringkas — **3 pertanyaan pemandu**, bukan paragraf panjang:

1. **Theoretical Advance** — apakah temuan mengubah/memperluas teori atau hanya mengkonfirmasi?
2. **Problem/Context** — apakah masalah nyata hanya terkonfirmasi, atau tetap ada karena data kontekstual?
3. **Practical Consequences** — apakah implikasi manajerial/policy baru, atau hanya mengulang praktik lama?

> Format lengkap: `references/problem-formulation.md` §1. Setiap klaim **wajib** diberi penanda
> sumber: `[L-3]` (literatur ke-3 pada matriks), `[D:kolom]`, `[U]` (dari brief user),
> `(inferensi)` untuk penalaran agent sendiri.

### Output Step 2
```
matriks_evidence.md   — matriks ringkas + daftar gap
catatan_gap.md        — argumen gap (TAS) + posisi penelitian ini (positioning)
```

### Quality Gate 2
- [ ] Setiap **paper/sumber** punya DOI **atau** file lokal yang dibaca (anti-hallucination)
- [ ] Setiap referensi tidak dipakai sebagai "bantalan" — minimal 1 sumber jadi argumen gap
- [ ] Tidak ada nama penelitian/penulis yang tidak ada di sumber (JANGAN mengarang)
- [ ] Gap bukan sekadar "belum diteliti di lokasi X" — ada justifikasi mengapa itu penting

---

## STEP 3 — Formulasi Masalah Penelitian

> Load `references/problem-formulation.md` (rumusan masalah, tujuan, manfaat, pertanyaan,
> hipotesis, variabel, definisi istilah, batasan) + `templates/bab1_pendahuluan.md`.

Urutan penulisan **wajib** (menjaga koherensi argumen):

1. **Latar belakang** — fenomena nyata (umumnya dari data lokal) → fakta yang mengganjal →
   perbandingan dengan temuan penelitian terdahulu → celah → posisi penelitian ini.
2. **Rumusan masalah** — 3–6 pertanyaan turunan, hierarkis (umum → khusus). **Rumusan harus
   TURUNAN dari latar belakang**, bukan tempelan.
3. **Tujuan** — cerminan 1:1 dari rumusan masalah (jumlah & urutan selaras).
4. **Manfaat** — teoritis / praktis (kebijakan/manajerial) / bagi peneliti lanjutan.
5. **Pertanyaan penelitian** (opsional, bila metode kualitatif) — terbuka, tidak mengasumsikan jawaban.
6. **Hipotesis** (wajib bila kuantitatif) — H0/H1 per variabel, mengikuti teknik analisis terpilih.
7. **Definisi operasional** — tiap variabel: definisi konseptual (sumber) + indikator + skala.
8. **Ruang lingkup** — lokasi, waktu, populasi dan sampel, variabel, data, teknik analisis; batas yang APAKAN.
9. **Definisi istilah** — hanya istilah kunci yang berpotensi ambigu.

### Aturan Penulisan
- **Jangan** menulis klaim empiris tanpa sumber. Dilarang menulis "berdasarkan penelitian terdahulu menunjukkan
  meningkatkan kinerja" tanpa `[L-n]`.
- Angka dari data lokal → tulis **[D:kolom]** agar jelas berasal dari dataset, bukan literatur.
- Hipotesis harus **menguji arah hubungan**, bukan mengulang tujuan.
- Untuk jenjang S3: tambahkan **statement of contribution** (kontribusi orisinal apa yang diklaim).

### Output Step 3
```
draft_bab1.md   — kerangka BAB I (sub-bab + poin + penanda sumber, belum narasi penuh)
```

---

## STEP 4 — Rancangan Metode Penelitian

> Load `references/methodology.md` (desain, pendekatan, teknik sampling, instrumen, teknik analisis,
  ethics, uji asumsi) + `references/dataset-analysis.md` (profil dataset & pemilihan uji).

### 4.1 Desain penelitian

Isi **field wajib** untuk setiap desain yang dipilih (lihat `references/methodology.md` §1):

| Elemen | Isi minimal |
|--------|-------------|
| Pendekatan & desain | Kuantitatif eksplanatif / deskriptif / kualitatif / mixed / R&D / studi kasus / action research — + **alasan pemilihan** + `[L-n]` bila berbasis teori |
| Lokasi & waktu | Tempat + alasan pemilihan lokasi; rentang waktu mulai–selesai |
| Populasi & sampel | Populasi, teknik sampling (acak, proporsional, purposive, snowball), **n dan rumus**, kriteria inklusi/eksklusi |
| Instrumen | Kuesioner, pedoman observasi, atau pedoman wawancara; asal butir; skala (Likert 1–5 atau 1–7); **uji validitas dan reliabilitas** (Cronbach's alpha, CFI) |
| Teknik analisis | Uji yang dipilih per hipotesis beserta **alasan**, uji asumsi, software (SPSS 26, R 4.x, Python, SmartPLS, atau AMOS) |
| Etika & izin | Persetujuan etik, informed consent, anonimitas, izin penelitian |
| Batasan rancangan | Keterbatasan rancangan dan mitigasinya (wajib untuk S2/S3) |

### 4.2 Analisis dataset nyata (WAJIB bila file data ada)

Jangan menulis metode generik bila data ada di tangan — **profilkan data dulu**:

```
python3 scripts/profile_dataset.py <file.csv|file.xlsx> --out profil
```

Hasilnya (`profil_dataset.md` + `profil_dataset.json`) berisi: jumlah baris/kolom, tipe data,
missing per kolom, distribusi/frekuensi, mean–median–SD, skewness, deteksi skala Likert,
**Cronbach's alpha** (bila terdeteksi), uji normalitas, serta **rekomendasi teknik analisis**
(paired t / independent t / one-way ANOVA / Wilcoxon / regresi / korelasi / Spearman).

> **Aturan anti-hallucination data**: angka yang muncul di BAB III (jumlah responden, rentang
> skor, mean, SD) **harus berasal dari output `profile_dataset.py` atau dihitung ulang dari file**.
> Dilarang mengarang angka. Bila data belum tersedia → tulis rancangan analisis *tanpa* angka
> preliminer, dan beri label `(data belum dianalisis)`.

### 4.3 Hipotesis → uji (tabel pemetaan)

Isi `templates/tabel_uji_statistik.md` dan tempelkan di BAB III:

| No | Rumusan Masalah | Hipotesis | Data | Uji Statistik | Keterangan |
|----|-----------------|-----------|------|---------------|------------|
| RM-1 | … | H₀₁ … / H₁₁ … | `[D:kolom]` | Uji X | α = 0,05 |

### Output Step 4
```
draft_bab2.md   — kerangka BAB II (sub-bab + sintesis + penanda sumber)
draft_bab3.md   — kerangka BAB III (desain + analisis + tabel uji)
profil_dataset.md | .json   (bila ada dataset)
```

### Quality Gate 4
- [ ] Desain dipilih dengan **alasan**, bukan sekadar nama
- [ ] Populasi, teknik sampling, dan **n** (dengan rumus bilabersifat probabilistik) tertulis jelas
- [ ] Instrumen dinyatakan asal butirnya (dikembangkan sendiri atau diadaptasi dari `[L-n]`)
- [ ] **Setiap hipotesis kuantitatif punya satu teknik analisis** dan uji asumsi
- [ ] **Semua angka dataset berasal dari `profile_dataset.py`/perhitungan nyata** (wajib, tanpa kecuali)
- [ ] Etika penelitian dan izin penelitian sudah ada di rancangan

---

## STEP 5 — Menulis Draft (BAB I–III)

> Template: `templates/proposal_template.md` (dokumen penuh), `templates/bab1_pendahuluan.md`,
> `templates/bab2_tinjauan_pustaka.md`, `templates/bab3_metode.md`.
> Gaya penulisan dan struktur: `references/document-assembly.md`.

Aturan gaya:

- Bahasa Indonesia **akademik formal**: kalimat aktif & pasif sesuai konteks, tanpa
  kata repetitif dari poin sebelumnya, tanpa "di sini" berlebihan, tanpa terjemahan kaku.
- **Rantai argumen**: setiap sub-bab harus **menjawab pertanyaan** dari sub-bab sebelumnya, lalu
  memunculkan pertanyaan baru. Ini yang membedakan proposal yang *kohesif* dari yang *tempelan*.
- **Jangan menyalin** kalimat dari literatur; parafrase dan beri marker `[L-n]` sebagai bukti.
- **Kerangka Berpikir (BAB II)** wajib ada sebagai sub-bab penutup: hubungan antar variabel
  digambar ASCII/LaTeX atau tabel variabel + panah.
- **Tabel & gambar**: setiap tabel diberi judul di atas, sumber di bawah (`Sumber: analisis
  penulis, 2026` / `Sumber: [L-3]`). Nomor tabel/daftar isi auto oleh pandoc.

### Output Step 5
```
proposal_skripsi.md   # DOKUMEN UTAMA: halaman judul + daftar isi + BAB I + BAB II + BAB III + daftar pustaka
```

> **Jangan berhenti di kerangka.** Yang diserahkan ke user adalah proposal **naratif penuh**,
> bukan bullet/kerangka saja.

---

## STEP 6 — Quality Gate, Referensi, & Export

### 6.1 Daftar pustaka

Semua rujukan yang dikutip di teks **wajib ada** di daftar pustaka, dan sebaliknya (1:1).
Format: APA 7 default (`references/citation-styles.md`). Aturan: 
- artikel: `Penulis, A. A. (Tahun). Judul. *Nama Jurnal*, *vol*(no), hal. DOI`
- buku: `Penulis, A. A. (Tahun). *Judul*. Penerbit.`
- dokumen lokal/pedoman: `Institusi (Tahun). *Judul*.`
- sumber dari file lokal tanpa DOI → **jangan dikarang DOI**; tulis `(dokumen lokal, namafile.pdf)`.

### 6.2 Quality gate akhir (semua wajib)

- [ ] Judul, identitas, dan jenjang konsisten dengan kontrak Step 0
- [ ] **Jumlah tujuan = jumlah rumusan masalah** (atau 1:1 terpetakan)
- [ ] Setiap tabel uji punya hipotesis + teknik analisis + sumber data
- [ ] **Nol angka dataset yang tidak berasal dari file** (spot-check: cocok dengan `profil_dataset.md`)
- [ ] Semua `[L-n]` punya entri di daftar pustaka; semua entri dikutip minimal sekali
- [ ] Tidak ada `[isi ...]` tersisa diam-diam → wajib dikonfirmasi user atau ditandai daftar
- [ ] Struktur bab sesuai pedoman kampus (bila ada template) & jenjang
- [ ] Bahasa: ejaan bahasa Indonesia (KBBI) — hindari "kwalitas", campur "pengaruh" dan "dampak",
  kalimat "yang mana" berlebihan, serta pengulangan "hasil-hasil"
- [ ] User menyetujui draft (gate human-in-the-loop)

### 6.3 Export

```bash
# DOCX (rekomendasi; butuh pandoc)
scripts/build_docx.sh proposal_skripsi.md --out-dir . --title "Judul Proposal" --number-sections

# LaTeX (opsional)
pandoc proposal_skripsi.md -o proposal_skripsi.tex --number-sections
pandoc proposal_skripsi.md -o proposal_skripsi.docx --reference-doc=pedoman_kampus.docx
```

`build_docx.sh` membuat: `.docx` (dengan daftar isi otomatis bila `--toc`), `daftar_isi.md`,
dan `<nama>_ekstrak.md` bila dijalankan dengan `--clean` (naskah tanpa blok instruksi internal).

### Output Step 6
```
📋 OUTPUT UTAMA (wajib):
  proposal_skripsi.md          # proposal lengkap (BAB I–III, Bahasa Indonesia)
  proposal_skripsi.docx        # DOCX siap dibaca dan disunting
  daftar_pustaka.md            # daftar pustaka (juga sudah ada di dalam proposal)
🗂 PENDUKUNG (bila dipakai):
  matriks_evidence.md | catatan_gap.md | sumber_inventaris.md | profil_dataset.md | draft_bab*.md
```

---

## Alur Pemakaian Cepat

| Permintaan | Action |
|-----------|--------|
| "Bikin proposal skripsi dari folder [path] tentang X" | Step 0 tanyakan jenjang → 1 inventaris → 2 bukti → 3–4 formulasi → 5 draft → 6 export |
| "Buat proposal tesis, fokus mixed-methods" | Jenjang Thesis + mode Folder+Online; wajib tulis threat to validity dan strategi generalisasi |
| "Cuma bab 3 metode, data csv sudah ada" | Langsung Step 1 (klasifikasi) → Step 4 (`profile_dataset.py`) → tulis BAB III → export |
| "Review literatur untuk latar belakang dulu" | Step 2 → bila butuh tabel penuh: **pakai skill `paper-review`** |
| "Pakai pedoman kampus ini" | Step 0 set template path → Step 6 verifikasi struktur (daftar isi & nomor bab) |
| "Cek ANOVA atau regresi untuk data ini" | `profile_dataset.py` → baca rekomendasi uji → Bab III tabel uji |
| "Tambah studi terdahulu 5 paper" | Step 2 matriks evidence + `[L-n]` baru; update BAB II + daftar pustaka |
| "Ekspor ke LaTeX" | `pandoc proposal.md -o proposal.tex --number-sections` (opsional) |

---

## Aturan Penting (Selalu Berlaku)

0. **Output utama = proposal naratif lengkap (BAB I–III)**, bukan kerangka/bullet, bukan ringkasan.
   Draft per-bab (draft_bab*.md) hanya working file internal.
1. **Jangan mengarang data.** Angka responden, skor, mean, SD, hasil uji → dari `profile_dataset.py`
   atau file nyata; kalau belum dianalisis → tulis `(data belum dianalisis)`, bukan angka karangan.
2. **Jangan mengarang literatur/penulis/DOI.** Setiap `[L-n]` terverifikasi (DOI resolve atau file
   lokal dibaca). Sumber lokal tanpa DOI → tandai `(dokumen lokal)`.
3. **Jangan mengarang identitas.** NIM, fakultas, dosen, nama responden → `[isi ...]` bila tidak ada.
4. **Jenjang menentukan kedalaman.** S1 = penerapan; S2 = pengembangan kerangka; S3 = kontribusi
   teoretis orisinal. Jangan menulis proposal S1 yang setebal proposal S3 (atau sebaliknya).
5. **Tujuan = 1:1 rumusan masalah.** Ini quality gate, bukan saran.
6. **Setiap klaim empiris ber-marker sumber**: `[L-n]`, `[D:kolom]`, `[U]`, `(inferensi)`.
7. **Human-in-the-loop**: konfirmasi hanya di Step 0 & sebelum export, tidak per-bagian.
8. **Simpan artefak sebagai file** di folder kerja user, bukan hanya di chat.
9. **Eja Indonesia**: KBBI, kapitalisasi kalimat, istilah asing italic pada penyebutan pertama.
10. **Bahasa output selalu Bahasa Indonesia**, kecuali user minta naskah inggris.

## Referensi Internal

| File | Gunakan untuk |
|------|---------------|
| [references/data-sources.md](references/data-sources.md) | Klasifikasi & ekstraksi file lokal (PDF/DOCX/MD/CSV/XLSX/JSON) |
| [references/problem-formulation.md](references/problem-formulation.md) | Rumusan masalah, tujuan, manfaat, gap (TAS), hipotesis, variabel, batasan |
| [references/methodology.md](references/methodology.md) | Desain penelitian, sampling, instrumen, teknik analisis, etika, uji asumsi |
| [references/dataset-analysis.md](references/dataset-analysis.md) | Profil dataset & pemilihan uji statistik, cara membaca `profil_dataset.md` |
| [references/online-search.md](references/online-search.md) | Pencarian online pelengkap (OpenAlex/Semantic Scholar) |
| [references/document-assembly.md](references/document-assembly.md) | Gaya bahasa Indonesia, struktur BAB, kerangka berpikir, tabel dan gambar |
| [references/citation-styles.md](references/citation-styles.md) | Format daftar pustaka (APA 7/Chicago/Harvard/Vancouver/IEEE) |
| [references/quality-gates.md](references/quality-gates.md) | Rincian quality gate per tahap + checklist akhir |
| [templates/proposal_template.md](templates/proposal_template.md) | Template dokumen proposal penuh (judul → daftar isi → BAB I–III) |
| [templates/bab1_pendahuluan.md](templates/bab1_pendahuluan.md) | Template BAB I |
| [templates/bab2_tinjauan_pustaka.md](templates/bab2_tinjauan_pustaka.md) | Template BAB II |
| [templates/bab3_metode.md](templates/bab3_metode.md) | Template BAB III |
| [templates/tabel_uji_statistik.md](templates/tabel_uji_statistik.md) | Tabel pemetaan hipotesis → uji statistik |
| [scripts/ingest_sources.sh](scripts/ingest_sources.sh) | Scan & ekstrak file lokal → inventaris |
| [scripts/profile_dataset.py](scripts/profile_dataset.py) | Profil dataset CSV/XLSX/TSV/JSON + rekomendasi uji |
| [scripts/build_docx.sh](scripts/build_docx.sh) | Markdown → DOCX (pandoc) + daftar isi |
| [tests/sample_dataset.csv](tests/sample_dataset.csv) | Dataset contoh untuk uji script |

## Integrasi Skill

| Kebutuhan | Skill yang dipakai |
|-----------|---------------------|
| Tabel review literatur lengkap (12 kolom, provenance, ekspor CSV/XLSX/BIB/RIS) | `paper-review` |
| Protocol penulisan paper jurnal (English) | `academic-writing` |
| Slide defence/sidang | `pptx` (di luar cakupan skill ini) |
| Penyusun proposal berbahasa Indonesia (skill ini) | `proposal-skripsi` |

## Atribusi

Struktur pipeline dan protokol anti-hallucination mengikuti **bimajanuri/academic-writing-skill**
dan **bimajanuri/paper-review-skill**. Kerangka proposal (rumusan masalah → tujuan → metode →
manfaat), metode gap **TAS/Berwald-Daellenbach**, dan pola "sintesis literatur → kerangka
berpikir" mengikuti praktik metodologi penelitian standar; rujukan metodologis yang direferensikan
tanpa mengutip teks: **Creswell & Creswell** (desain mixed-methods), **Field** (analisis statistik),
**Kumar** (penelitian tindakan/R&D), **Sugiyono** (desain & statistik Indonesia), **Braun &
Clarke** (analisis tematik), **Miles, Huberman & Saldaña** (kualitatif). Detail di README.

## Platform Note

Format Agent Skills (SKILL.md) portabel ke OpenCode (`~/.config/opencode/skills/`),
Claude Code (`~/.claude/skills/`), dan platform lain dengan menyalin folder ini.
