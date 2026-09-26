# Proposal Skripsi Skill

**Skill penyusun proposal penelitian berbahasa Indonesia** untuk AI coding agents (Claude Code,
OpenCode, dan agen berbasis Agent Skills lainnya). Menghasilkan **proposal lengkap BAB I
Pendahuluan, BAB II Tinjauan Pustaka, dan BAB III Metode Penelitian** untuk **skripsi (S1),
thesis (S2), atau disertasi (S3)** — dipilih pengguna.

Sumber bukti diambil dari **kumpulan file lokal** yang ditunjuk user (PDF, DOCX, MD, TXT, CSV,
XLSX, JSON), ditambah **pencarian online pelengkap** bila literatur lokal minim.

Skill ini **berkumpulan** dengan `paper-review` (tabel review literatur lengkap) dan
`academic-writing` (protocol penulisan paper English) — bukan duplikatnya.

## Fitur Utama

- **Tiga jenjang dalam satu skill**: skripsi, thesis, disertasi — dengan perbedaan kedalaman yang
  nyata (panjang, kontribusi, landasan teori, pengujian, threat to validity, statement of
  contribution)
- **Sumber data lokal**: scan folder rekursif, klasifikasi otomatis ke 5 kategori
  (literatur, data, pedoman, aturan/etika, lainnya), ekstraksi teks PDF dan DOCX
- **Analisis dataset nyata**: `profile_dataset.py` memprofilkan CSV/TSV/XLSX/JSON —
  deskriptif, missing, skewness, normalitas, Cronbach's alpha, deteksi skala Likert, dan
  **rekomendasi teknik analisis**. Semua angka di BAB III berasal dari sana, bukan dikarang
- **Rancangan statistik lengkap**: pemetaan hipotesis ke uji, uji asumsi, uji alternatif
  non-parametrik, rumus penentuan sampel (Cochran, Krejcie & Morgan, koreksi populasi hingga)
- **Metode kuantitatif, kualitatif, mixed-methods, R&D, penelitian tindakan, studi kasus** —
  lengkap dengan elemen wajib dan alasan pemilihan
- **Argumen gap TAS/Berwald-Daellenbach**: 3 pertanyaan pemandu agar gap bukan sekadar
  "belum diteliti di lokasi X"
- **Penandaan sumber (provenance)**: `[L-n]` literatur, `[D:kolom]` dataset, `[U]` brief user,
  `[P-n]` pedoman, `(inferensi)` untuk penalaran agent
- **Anti-hallucination ketat**: tidak mengarang data, DOI, identitas, responden, atau hasil uji
- **Ekspor Markdown + DOCX (pandoc)** dengan daftar isi otomatis, pemeriksaan marker, dan
  deteksi placeholder yang belum diisi
- **Gaya bahasa Indonesia akademik**: panduan kalimat, ejaan KBBI, kapitalisasi, istilah asing

## Pipeline

```text
STEP 0: KLARIFIKASI  -> jenjang, bidang, topik, jenis penelitian, folder sumber, format
STEP 1: INVENTARIS   -> scan + klasifikasi file -> sumber_inventaris.json
STEP 2: EVIDENSI     -> matriks evidence ringkas + gap (TAS) + online search pelengkap
STEP 3: FORMULASI    -> latar belakang, rumusan masalah, tujuan, manfaat, hipotesis, variabel
STEP 4: RANCANGAN    -> desain metode, instrumen, sampling, teknik analisis + analisis dataset
STEP 5: DRAFT        -> halaman judul + daftar isi + BAB I-III (Markdown)
STEP 6: GATE+EXPORT  -> quality gate -> daftar pustaka -> MD + DOCX (pandoc)
```

Setiap tahap punya quality gate. Konfirmasi user hanya di Step 0 dan sebelum export.

## Instalasi

### Claude Code

```bash
# Opsi 1 - symlink (kanonik, sekali update)
mkdir -p ~/.agents/skills
ln -s $(pwd) ~/.agents/skills/proposal-skripsi
ln -s ../../.agents/skills/proposal-skripsi ~/.claude/skills/proposal-skripsi

# Opsi 2 - salin langsung
cp -R . ~/.claude/skills/proposal-skripsi
```

### OpenCode

```bash
# Opsi 1 - symlink
ln -s ../../.agents/skills/proposal-skripsi ~/.config/opencode/skills/proposal-skripsi

# Opsi 2 - salin langsung
cp -R . ~/.config/opencode/skills/proposal-skripsi
```

> Rekomendasi: simpan repo ini sebagai kanonik di `~/.agents/skills/proposal-skripsi`, lalu
> **symlink** ke folder skills masing-masing klien. Edit cukup sekali di sumber.

## Penggunaan

Skill aktif otomatis saat user meminta, misalnya:

- "Bikin proposal skripsi dari folder [path] tentang X"
- "Buat proposal tesis mixed-methods, data saya di [path]"
- "Bantu susun Bab III, ada data CSV di sini"
- "Tulis bab 1 dan 2 daripaper-paper folder ini"
- "Cek uji statistik yang cocok untuk data ini"
- "Rancang proposal disertasi dengan kontribusi teoretis baru"
- "Ekspor proposal ke DOCX"

Alur kerja: **Klarifikasi -> Inventaris -> Bukti dan Gap -> Formulasi -> Rancangan -> Draf ->
Quality Gate -> Export.**

## Contoh Pemakaian Script

```bash
# 1. Inventarisasi + ekstraksi teks PDF
scripts/ingest_sources.sh ./folder-sumber --json

# 2. Profil dataset (tidak butuh pandas; XLSX butuh openpyxl)
python3 scripts/profile_dataset.py data/responden.csv --out profil

# 3. Konversi naskah ke DOCX
scripts/build_docx.sh proposal_skripsi.md --out-dir . --title "Judul" --toc --clean
```

## Struktur Repo

```text
proposal-skripsi/
├── SKILL.md                             # Pintu masuk & orchestrator
├── references/
│   ├── data-sources.md                  # Klasifikasi & ekstraksi file lokal
│   ├── problem-formulation.md           # Gap (TAS), rumusan masalah, tujuan, hipotesis
│   ├── methodology.md                   # Desain, sampling, instrumen, uji asumsi, etika
│   ├── dataset-analysis.md              # Profil dataset & pemilihan uji statistik
│   ├── online-search.md                 # Pencarian online pelengkap (OpenAlex/S2)
│   ├── document-assembly.md             # Struktur BAB, gaya bahasa Indonesia, kerangka berpikir
│   ├── citation-styles.md               # Daftar pustaka (APA 7/Chicago/Harvard/Vancouver/IEEE)
│   └── quality-gates.md                 # Gate per tahap + checklist akhir
├── templates/
│   ├── proposal_template.md             # Template dokumen penuh (judul -> BAB I-III)
│   ├── bab1_pendahuluan.md
│   ├── bab2_tinjauan_pustaka.md
│   ├── bab3_metode.md
│   └── tabel_uji_statistik.md           # Pemetaan hipotesis -> uji
├── scripts/
│   ├── ingest_sources.sh                # Scan & ekstrak file lokal -> inventaris
│   ├── profile_dataset.py               # Profil CSV/XLSX/TSV/JSON + rekomendasi uji
│   └── build_docx.sh                    # Markdown -> DOCX (pandoc) + daftar isi
├── tests/
│   └── sample_dataset.csv               # Dataset contoh untuk uji script
└── README.md
```

## Prasyarat Opsional

| Tool | Kebutuhan | Instalasi |
|------|-----------|-----------|
| `pdftotext` (poppler) | ekstraksi teks PDF | `brew install poppler` |
| `pandoc` | ekspor DOCX | `brew install pandoc` |
| `openpyxl` | baca file `.xlsx` | `pip3 install openpyxl` |
| `scipy` | uji normalitas parametrik (Shapiro-Wilk) | `pip3 install scipy` |

Tanpa dependensi apa pun, skill tetap bisa berjalan: hanya membaca MD/TXT, hanya menulis Markdown,
dan uji normalitas memakai pendekatan skewness-kurtosis.

## Aturan Penting

1. **Output utama = proposal naratif lengkap (BAB I-III)**, bukan kerangka atau bullet.
2. **Jangan mengarang data** — angka dari `profile_dataset.py` atau perhitungan nyata; bila data
   belum dianalisis, tulis `(data belum dianalisis)`.
3. **Jangan mengarang literatur, penulis, atau DOI** — setiap `[L-n]` terverifikasi (DOI resolve
   atau file lokal dibaca). Sumber lokal tanpa DOI ditandai `(dokumen lokal)`.
4. **Jangan mengarang identitas** — NIM, fakultas, dosen, nama responden ditulis `[isi ...]`.
5. **Jenjang menentukan kedalaman** — S1 penerapan, S2 pengembangan kerangka, S3 kontribusi
   teoretis orisinal.
6. **Tujuan = 1:1 rumusan masalah.**
7. **Setiap klaim empiris ber-marker sumber.**
8. **Human-in-the-loop** — konfirmasi di awal dan sebelum export, tidak per-bagian.
9. **Simpan artefak sebagai file**, bukan hanya di chat.
10. **Ejaan KBBI**, output selalu Bahasa Indonesia kecuali diminta lain.

## Integrasi Skill

| Kebutuhan | Skill |
|------------|-------|
| Tabel review literatur lengkap (12 kolom, provenance, ekspor CSV/XLSX/BIB/RIS) | `paper-review` |
| Protocol penulisan paper jurnal (English) | `academic-writing` |
| Slide defence atau sidang | `pptx` |
| **Proposal skripsi/tesis/disertasi (Bahasa Indonesia)** | **`proposal-skripsi`** |

## Atribusi

Struktur pipeline dan protokol anti-hallucination mengikuti **bimajanuri/academic-writing-skill**
dan **bimajanuri/paper-review-skill**. Kerangka proposal (rumusan masalah -> tujuan -> metode ->
manfaat), metode gap **TAS/Berwald-Daellenbach**, dan pola "sintesis literatur -> kerangka
berpikir" mengikuti praktik metodologi penelitian standar. Rujukan metodologis yang
direferensikan tanpa mengutip teks: **Creswell & Creswell** (desain mixed-methods), **Field**
(analisis statistik), **Kumar** (penelitian tindakan dan R&D), **Sugiyono** (desain dan statistik
Indonesia), **Braun & Clarke** (analisis tematik), **Miles, Huberman & Saldaña** (kualitatif),
**Kline** (multikolinearitas), **Cochran** dan **Krejcie & Morgan** (penentuan sampel).

## Lisensi

Rilis di bawah **[MIT License](LICENSE)**.
