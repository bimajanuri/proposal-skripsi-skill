# Quality Gates — Rincian Gate per Tahap

Pandu **STEP 1 sampai STEP 6**. Setiap gate adalah daftar periksa yang **wajib dilewati** sebelum
melangkah ke tahap berikutnya. Kegagalan gate berarti berhenti, perbaiki, lalu lanjut.

## Gate 0 — Klarifikasi (Step 0)

- [ ] Jenjang sudah dipilih eksplisit oleh user (skripsi/thesis/disertasi)
- [ ] Topik penelitian dinyatakan jelas dalam satu kalimat
- [ ] Folder sumber ditunjuk (wajib ada)
- [ ] Jenis penelitian diketahui (kuantitatif/kualitatif/mixed)
- [ ] Gaya sitasi dan format ekspor ditentukan
- [ ] `kontrak_proposal.json` tersimpan sebagai kontrak kerja

## Gate 1 — Inventaris (Step 1)

- [ ] Semua file di folder terklasifikasi ke 5 kategori
- [ ] Setiap literatur punya judul dan tahun (atau ditandai `—` karena tidak terbaca)
- [ ] Setiap dataset punya jumlah baris dan kolom terverifikasi
- [ ] File tidak terbaca (scan) ditandai `PERLU_OCR`
- [ ] Marker `[L-n]` dan `[D]` sudah ditetapkan untuk semua sumber
- [ ] Tidak ada file yang "hilang" tanpa penjelasan

## Gate 2 — Bukti dan Gap (Step 2)

- [ ] Setiap sumber punya DOI yang dapat di-resolve atau file lokal yang dibaca
- [ ] DOI gagal resolve ditandai `UNVERIFIED`
- [ ] Hanya ada 3-5 gap, bukan 8 gap remeh
- [ ] Minimal dua dari tiga pertanyaan TAS terjawab "ya"
- [ ] Tidak ada nama penelitian atau penulis yang tidak ada di sumber
- [ ] Kata kunci dan tanggal pencarian tercatat (bila online search dipakai)

## Gate 3 — Formulasi (Step 3)

- [ ] Rumusan masalah 3-5 butir, hierarkis, dapat dijawab data yang ada
- [ ] Tujuan = rumusan masalah 1:1, urutan sama
- [ ] Manfaat spesifik (bukan "berguna bagi masyarakat")
- [ ] Setiap variabel punya definisi konseptual dan operasional
- [ ] Hipotesis punya arah dari teori dan 1:1 dengan uji di BAB III
- [ ] Ruang lingkup 6 batas terisi
- [ ] Tidak ada klaim empiris tanpa marker sumber
- [ ] Untuk S2/S3: ada kontribusi teoretis yang diklaim

## Gate 4 — Rancangan (Step 4)

- [ ] Desain dipilih dengan alasan, bukan sekadar nama
- [ ] Populasi, teknik sampling, dan n tertulis (dengan rumus bila probabilistic)
- [ ] Instrumen dinyatakan asal butirnya (`[L-n]`)
- [ ] Uji validitas dan reliabilitas direncanakan
- [ ] Setiap hipotesis punya tepat satu teknik analisis
- [ ] Uji asumsi ditulis lengkap
- [ ] **Semua angka dataset berasal dari output `profile_dataset.py` atau perhitungan nyata**
- [ ] Etika, izin, dan anonimitas sudah dirancang
- [ ] Untuk S2/S3: batasan rancangan dan mitigasinya ditulis
- [ ] **Bila kualitatif:** lihat Gate 4-Kualitatif di bawah

## Gate 4-Kualitatif — hanya bila desain bukan survei kuantitatif

> Panduan lengkap: `references/qualitative-analysis.md`. Gate ini **mengganti**
> bagian Gate 4 yang bersifat kuantitatif (rumus bilabersifat probabilistik,
> Cronbach's alpha, tabel hipotesis → uji), bukan menambahkannya.

- [ ] Desain kualitatif dipilih satu saja (studi kasus / fenomenologi / grounded
      theory / analisis tematik / deskriptif) dengan alasan
- [ ] Paradigma dan pendekatan dinyatakan, bukan hanya nama desain
- [ ] Informan: kriteria inklusi **dan** eksklusi, teknik purposive/snowball,
      serta **alasan penghentian pengumpulan data** (saturasi) — bukan sekadar
      "sampai jenuh"
- [ ] Instrumen: pedoman wawancara ada di Lampiran (`templates/pedoman_wawancara.md`)
      dan lembar persetujuan ada (`templates/informed_consent.md`)
- [ ] Tahapan analisis tertulis berurutan (transkripsi → koding terbuka →
      kategorikal → tematik), bukan hanya menyebut "analisis tematik"
- [ ] Validitas: member checking dan/atau triangulasi direncanakan
- [ ] Penanda kutipan memakai `[K-n]` (bukan `[L-n]`) dan sumbernya jelas
- [ ] Tidak ada kutipan, kode, tema, atau jumlah peserta yang tidak ada di transkrip
- [ ] Batasan penelitian dinyatakan jujur (transferabel, bukan generalizable)

## Gate 5 — Draf (Step 5)

- [ ] Semua sub-bab terisi naratif, bukan bullet
- [ ] Alur antar sub-bab koheren
- [ ] Kerangka berpikir ada di BAB II
- [ ] Setiap tabel punya judul dan sumber
- [ ] Tidak ada catatan internal agent yang bocor ke naskah
- [ ] Tidak ada kalimat terpotong

## Gate 6 — Akhir (Step 6)

- [ ] Judul dan identitas konsisten dengan kontrak
- [ ] Semua `[L-n]` punya entri di daftar pustaka
- [ ] Semua entri dikutip minimal sekali
- [ ] Angka dataset di naskah cocok dengan `profil_dataset.md` (spot-check 5 angka)
- [ ] Tidak ada placeholder `[isi ...]` yang tersisa tanpa catatan
- [ ] Struktur sesuai pedoman kampus (bila ada)
- [ ] Ejaan bahasa Indonesia benar (KBBI)
- [ ] Ekspor berhasil: `.md` dan `.docx` keduanya ada
- [ ] User menyatakan setuju dengan draf

### Gate 6 otomatis — wajib dijalankan, bukan Reading Mata

Tiga pemeriksa menutupi bagian gate yang mustahil Dicek mata pada naskah panjang:

```bash
# gaya bahasa Indonesia + struktur BAB I
python3 scripts/id_language_check.py outputs/proposal.md --struktur --strict

# penanda menggantung, placeholder, angka tanpa sumber, sinkronisasi DOCX
python3 scripts/proposal_doctor.py outputs/proposal.md \
    --dataset data/responden.csv --hasil-uji outputs/hasil_uji.json \
    --docx outputs/proposal.docx --strict

# kesesuaian struktur dengan pedoman kampus
python3 scripts/apply_campus_template.py check <preset> outputs/proposal.md --lengkap
```

Temuan **`--strict` = kode keluar 1** berarti gate gagal: perbaiki, jangan diabaikan.
Temuan kategori selain `galat` (warning) boleh tetap ada bila punya alasan naratif.

## Penalti (bila gate gagal)

| Gejala | Tindakan |
|--------|----------|
| Angka dataset tidak cocok dengan profil | hitung ulang, jangan dipaksa |
| DOI tidak resolve | tandai UNVERIFIED atau keluarkan dari daftar pustaka |
| Tujuan tidak 1:1 dengan rumusan masalah | selaraskan sebelum lanjut |
| `[isi ...]` terlalu banyak | tanya user sekali, isi sekaligus |
| Struktur bab tidak sesuai pedoman | Ikuti pedoman kampus, bukan versi default skill |
| Bahasa naskah membingungkan | tulis ulang sub-bab tersebut, jangan tambal kata |
| Kutipan kode tidak ada di transkrip | hapus kutipan; jangan menulis ulang/menafsirkan ulang |
| Persentase "sebagian besar" tanpa dihitung | hitung penyebutnya dari transkrip, atau ganti dengan deskriptif |

## Gate khusus Anti-Hallucination (berlaku di semua tahap)

- [ ] Tidak ada data/referensi yang tidak berasal dari file atau sumber terverifikasi
- [ ] Tidak ada identitas yang dikarang (NIM, fakultas, dosen, responden)
- [ ] Setiap klaim empiris punya marker
- [ ] Setiap inferensi agent ditandai `(inferensi)`
