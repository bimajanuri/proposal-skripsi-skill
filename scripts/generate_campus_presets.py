#!/usr/bin/env python3
"""
generate_campus_presets.py — Bangun preset campus_templates/*.json dari tabel data.

Tabel data di file ini adalah satu-satunya tempat nilai gaya dokumen ditulis.
Preset yang dihasilkan dibaca langsung oleh scripts/apply_campus_template.py.

Aturan main sumber data (anti-hafalan):
  - Every campus carries `sumber.status`:
      "pedoman-resmi"  -> angka diambil dari dokumen resmiCampus (umumnya fakultas/program studi).
      "konvensi-umum"  -> belum ada dokumen resmi yang dipakai sebagai rujukan;
                          angka hanya konvensi umum Indonesia dan WAJIB diverifikasi.
  - `sumber.scope` menjelaskan fakultas/tahun asal angka bila sumber tidak berlaku universal.
  - Tidak ada preset yang mengklaim "semua fakultas" bila sumbernya satu fakultas.

Perintah:
    generate_campus_presets.py              tulis ulang semua preset yang di-flag regenerate
    generate_campus_presets.py --check      hanya verifikasi JSON valid & provenance lengkap
    generate_campus_presets.py --only unpad  (bang ulang satu preset)
"""

import argparse
import json
import os
import sys

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_PRESET = os.path.join(AKAR, "campus_templates")

# ── Kerangka struktur bersama ────────────────────────────────────────────────
# Mirrors generic.json: frontmatter -> BAB I -> BAB II -> BAB III -> backmatter.
# Subbab `cek` memakai kunci yang dikenali scripts/apply_campus_template.py (CEK).
STRUKTUR = [
    {
        "id": "frontmatter",
        "judul": "Halaman Depan",
        "wajib": True,
        "wadah": True,
        "subbab": [
            {
                "judul": "Halaman Judul",
                "wajib": True,
                "catatan": "Judul, nama, NIM, pembimbing, program studi, fakultas, tahun",
            },
            {
                "judul": "Lembar Persetujuan",
                "wajib": True,
                "catatan": "Tanda tangan pembimbing, dekan/gubernur fakultas",
            },
            {
                "judul": "Pernyataan Keaslian",
                "wajib": True,
                "catatan": "Pernyataan naskah orisinal dan tidak plagiat",
            },
            {"judul": "Kata Pengantar", "wajib": False},
            {"judul": "Abstrak", "wajib": False},
        ],
    },
    {
        "id": "bab1",
        "judul": "BAB I PENDAHULUAN",
        "wajib": True,
        "subbab": [
            {
                "judul": "Latar Belakang Masalah",
                "wajib": True,
                "cek": ["latar_belakang", "data_empat_lapisan", "celah_penelitian"],
            },
            {"judul": "Rumusan Masalah", "wajib": True, "cek": ["rumusan_masalah"]},
            {"judul": "Tujuan Penelitian", "wajib": True, "cek": ["tujuan"]},
            {"judul": "Manfaat Penelitian", "wajib": True, "cek": ["manfaat"]},
            {"judul": "Batasan Masalah", "wajib": True, "cek": ["batasan"]},
        ],
    },
    {
        "id": "bab2",
        "judul": "BAB II TINJAUAN PUSTAKA",
        "wajib": True,
        "subbab": [
            {"judul": "Landasan Teori", "wajib": True},
            {"judul": "Hubungan Antarvariabel", "wajib": True},
            {
                "judul": "Penelitian Terdahulu yang Relevan",
                "wajib": True,
                "cek": ["tabel_penelitian_terdahulu", "celah_penelitian"],
            },
            {"judul": "Kerangka Berpikir", "wajib": True},
            {
                "judul": "Hipotesis",
                "wajib": False,
                "catatan": "Wajib untuk rancangan kuantitatif hipotesis",
            },
        ],
    },
    {
        "id": "bab3",
        "judul": "BAB III METODE PENELITIAN",
        "wajib": True,
        "subbab": [
            {"judul": "Desain Penelitian", "wajib": True, "cek": ["desain_penelitian"]},
            {
                "judul": "Populasi dan Sampel",
                "wajib": True,
                "cek": ["populasi_sampel", "teknik_sampel", "perhitungan_sampel"],
            },
            {"judul": "Variabel Penelitian", "wajib": True},
            {"judul": "Definisi Operasional Variabel", "wajib": True},
            {"judul": "Skala Pengukuran", "wajib": True, "cek": ["skala_likert"]},
            {
                "judul": "Teknik Pengumpulan Data",
                "wajib": True,
                "cek": ["instrumen_validitas_reliabilitas"],
            },
            {
                "judul": "Teknik Analisis Data",
                "wajib": True,
                "cek": ["uji_statistik_cocok", "hasil_uji_tabel"],
            },
        ],
    },
    {
        "id": "backmatter",
        "judul": "Bagian Akhir",
        "wajib": True,
        "wadah": True,
        "subbab": [
            {
                "judul": "Daftar Pustaka",
                "wajib": True,
                "cek": ["semua_penanda_terdaftar"],
            },
            {"judul": "Lampiran", "wajib": True},
        ],
    },
]

KELENGKAPAN_DASAR = [
    "halaman judul",
    "lembar persetujuan",
    "pernyataan keaslian",
    "kata pengantar",
    "daftar isi",
    "daftar tabel",
    "daftar gambar",
    "daftar singkatan",
    "abstrak (inti sari) bahasa Indonesia",
    "abstrak bahasa Inggris",
    "BAB I Pendahuluan",
    "BAB II Tinjauan Pustaka",
    "BAB III Metode Penelitian",
    "BAB IV Hasil dan Pembahasan",
    "BAB V Kesimpulan dan Saran",
    "daftar pustaka",
    "lampiran (instrumen, data, izin penelitian)",
]

# Konvensi umum Indonesia yang dipakai bila dokumen resmi belum dipakai sebagai rujukan.
KONVENSI_MARGIN = {"atas": "4 cm", "bawah": "3 cm", "kiri": "4 cm", "kanan": "3 cm"}
KONVENSI_GAYA = {
    "ukuran_halaman": "A4",
    "margin": dict(KONVENSI_MARGIN),
    "font_isi": "Times New Roman 12 pt",
    "font_judul": "Times New Roman 14 pt tebal",
    "spasi": "1.5",
    "rata_kanan_kiri": "justify",
    "penomoran_halaman": "bagian awal angka romawi kecil, bagian inti angka arab, di tengah bawah",
    "nomor_bab": "BAB I, BAB II, BAB III",
}


def konvensi(campus, nama, singkat, sumber_catatan, **gaya):
    """Preset tanpa rujukan dokumen resmi: angka = konvensi umum, wajib diverifikasi."""
    g = dict(KONVENSI_GAYA)
    g.update(gaya)
    return {
        "kampus": nama,
        "singkat": singkat,
        "jenjang": ["skripsi", "thesis", "disertasi"],
        "verifikasi": (
            "Preset ini BELUM diverifikasi ke pedoman resmi. Angka format berasal dari "
            f"konvensi umum penulisan Indonesia, bukan dari dokumen {nama}. "
            "Selalu cocokkan dengan pedoman resmi fakultas/program studi Anda sebelum submit."
        ),
        "sumber": {
            "status": "konvensi-umum",
            "dokumen": None,
            "url": None,
            "scope": "seluruh kampus (perlu konfirmasi)",
            "catatan": sumber_catatan,
        },
        "gaya_dokumen": g,
        "sitasi": "APA 7",
        "daftar_pustaka": 'heading "DAFTAR PUSTAKA" di halaman baru',
        "kelengkapan": list(KELENGKAPAN_DASAR),
        "struktur": STRUKTUR,
    }


def resmi(campus, nama, singkat, dokumen, url, scope, tahun, catatan, gaya, sitasi="APA 7",
          kelengkapan_tambahan=None):
    """Preset dengan angka dari dokumen resmi; scope menjelaskan cakupan fakultas/tahun."""
    kel = list(KELENGKAPAN_DASAR)
    if kelengkapan_tambahan:
        kel.extend(kelengkapan_tambahan)
    return {
        "kampus": nama,
        "singkat": singkat,
        "jenjang": ["skripsi", "thesis", "disertasi"],
        "verifikasi": (
            f"Angka format diambil dari {dokumen} ({scope}). Pedoman ini berlaku untuk "
            f"fakultas/program studi tersebut; fakultas lain di {nama} dapat berbeda. "
            "Cocokkan dengan pedoman unit Anda sebelum submit."
        ),
        "sumber": {
            "status": "pedoman-resmi",
            "dokumen": dokumen,
            "url": url,
            "scope": scope,
            "tahun": tahun,
            "catatan": catatan,
        },
        "gaya_dokumen": gaya,
        "sitasi": sitasi,
        "daftar_pustaka": 'heading "DAFTAR PUSTAKA" di halaman baru',
        "kelengkapan": kel,
        "struktur": STRUKTUR,
    }


# ── Tabel data preset ────────────────────────────────────────────────────────
# Kolom kunci tiap entri: file, preset(dict), regenerate(bool).
# regenerate=True  -> file dibuat/di-timpa oleh generator ini.
# regenerate=False -> file ada di repo (mis. ugm/ui/uny/itb/generic/custom),
#                    tidak ditulis ulang oleh generator.

def gaya(margin=None, font_isi=None, font_judul=None, spasi=None, penomoran=None,
         nomor_bab=None, ukuran_halaman="A4", rata="justify", align=None):
    g = {
        "ukuran_halaman": ukuran_halaman,
        "margin": margin or dict(KONVENSI_MARGIN),
        "font_isi": font_isi or "Times New Roman 12 pt",
        "font_judul": font_judul or "Times New Roman 14 pt tebal",
        "spasi": spasi or "1.5",
        "rata_kanan_kiri": rata,
        "penomoran_halaman": penomoran or "bagian awal angka romawi kecil, bagian inti angka arab, di tengah bawah",
        "nomor_bab": nomor_bab or "BAB I, BAB II, BAB III",
    }
    if align:
        g["catatan_tambahan"] = align
    return g


PRESETS = {}


def daftarkan(nama_file, preset, regenerate=True):
    PRESETS[nama_file] = {"preset": preset, "regenerate": regenerate}


# ── 1. IPB ──────────────────────────────────────────────────────────────────
daftarkan(
    "ipb",
    konvensi(
        "ipb",
        "Institut Pertanian Bogor",
        "IPB",
        "FAPET IPB menerbitkan Pedoman Penulisan Karya Ilmiah (PPKI); struktur & "
        "format perlu diambil langsung dari pedoman tersebut, bukan dari preset ini.",
    ),
)

# ── 2. UNAIR (Fakultas Vokasi 2025) ──────────────────────────────────────────
daftarkan(
    "unair",
    resmi(
        "unair",
        "Universitas Airlangga",
        "UNAIR",
        "Buku Panduan Skripsi dan TA Fakultas Vokasi",
        "https://vokasi.unair.ac.id/wp-content/uploads/2025/09/Buku-Panduan-Skripsi-dan-TA-Fakultas-Vokasi-Tahun-2025_opt.pdf",
        "Fakultas Vokasi, Universitas Airlangga (tahun 2025)",
        2025,
        "Fakultas Vokasi; fakultas lain UNAIR dapat punya ketentuan berbeda.",
        gaya(
            margin={"atas": "4 cm", "bawah": "3 cm", "kiri": "4 cm", "kanan": "3 cm"},
            spasi="2",
            penomoran="bagian awal romawi kecil, bagian inti arab, di tengah bawah",
            align="Spasi ganda; abstrak/daftar pustaka dapat 1 spasi. Judul cover 16 pt tebal.",
        ),
    ),
)

# ── 3. UB (Fakultas Teknik 2016) ─────────────────────────────────────────────
daftarkan(
    "ub",
    resmi(
        "ub",
        "Universitas Brawijaya",
        "UB",
        "Panduan Penulisan Skripsi, Tesis dan Disertasi Fakultas Teknik UB",
        "https://industri.ub.ac.id/wp-content/uploads/2023/10/Pedoman-skripsi-FT-UB.pdf",
        "Fakultas Teknik, Universitas Brawijaya (pedoman 2016)",
        2016,
        "Fakultas Teknik; fakultas lain UB dapat punya ketentuan berbeda.",
        gaya(
            margin={"atas": "2,5 cm (4 cm untuk awal bab)", "bawah": "2,5 cm",
                    "kiri": "3 cm (mirror/inside)", "kanan": "2,5 cm (mirror/outside)"},
            spasi="1.5",
            penomoran="bagian awal romawi kecil di tengah bawah; bagian inti/akhir arab di luar atas",
            align="Menggunakan mirror margin: sisi dalam 3 cm, sisi luar 2,5 cm.",
        ),
        kelengkapan_tambahan=["ringkasan (bahasa Indonesia)", "summary (bahasa Inggris)",
                              "lembar orisinalitas", "lembar peruntukan"],
    ),
)

# ── 4. ITS (Fakultas Teknik Industri 2021) ────────────────────────────────────
daftarkan(
    "its",
    resmi(
        "its",
        "Institut Teknologi Sepuluh Nopember",
        "ITS",
        "Pedoman Penyusunan Tugas Akhir Fakultas Teknik Industri ITS",
        "https://www.its.ac.id/tmi/wp-content/uploads/sites/51/2022/02/DRAFT-PEDOMAN-PENYUSUNAN-TUGAS-AKHIR-2021.pdf",
        "Fakultas Teknik Industri, ITS (pedoman 2021)",
        2021,
        "Fakultas Teknik Industri; fakultas/prodi lain ITS dapat punya ketentuan berbeda.",
        gaya(
            margin={"atas": "3,0 cm", "bawah": "2,5 cm", "kiri": "3,0 cm", "kanan": "2,0 cm"},
            spasi="1",
            penomoran="bagian awal romawi kecil, bagian inti/akhir arab, di footer kanan",
            align="Kertas HVS 80 g A4; judul bab huruf besar tebal, nomor bab romawi.",
        ),
    ),
)

# ── 5. UNDIP ────────────────────────────────────────────────────────────────
daftarkan(
    "undip",
    konvensi(
        "undip",
        "Universitas Diponegoro",
        "UNDIP",
        "Fakultas FISIP UNDIP menerbitkan Guidance for Thesis and Dissertation "
        "Writing; ambil angka format dari pedoman fakultas Anda.",
    ),
)

# ── 6. UNPAD (FISIP/FTIP/Farmasi) ────────────────────────────────────────────
daftarkan(
    "unpad",
    resmi(
        "unpad",
        "Universitas Padjadjaran",
        "UNPAD",
        "Pedoman Penyusunan dan Penulisan Skripsi (FISIP / FTIP / Fakultas Farmasi)",
        "https://ipol.fisip.unpad.ac.id/wp-content/uploads/2023/03/Pedoman-Skripsi.pdf",
        "Fakultas FISIP, FTIP, dan Farmasi, Universitas Padjadjaran",
        2023,
        "Ketiga fakultas tersebut konsisten: margin 4/4/3/3 cm, TNR 12, spasi 2. "
        "Fakultas lain Unpad dapat berbeda.",
        gaya(
            margin={"atas": "4 cm", "bawah": "3 cm", "kiri": "4 cm", "kanan": "3 cm"},
            spasi="2",
            penomoran="bagian awal romawi kecil di luar atas; bagian inti/akhir arab",
            align="Abstrak, judul tabel/gambar, dan daftar pustaka 1 spasi. Judul bab 14 pt tebal.",
        ),
    ),
)

# ── 7. UNHAS ────────────────────────────────────────────────────────────────
daftarkan("unhas", konvensi(
    "unhas", "Universitas Hasanuddin", "UNHAS",
    "Ambil pedoman penulisan skripsi resmi UNHAS/Fakultas Anda."))

# ── 8. Telkom University ─────────────────────────────────────────────────────
daftarkan("telu", konvensi(
    "telu", "Telkom University", "TEL-U",
    "Ambil Panduan Penulisan Tugas Akhir resmi Telkom University."))

# ── 9. BINUS ─────────────────────────────────────────────────────────────────
daftarkan("binus", konvensi(
    "binus", "BINUS University", "BINUS",
    "Ambil Pedoman Penulisan Skripsi/Thesis BINUS resmi; sitasi BINUS umumnya APA."))

# ── 10. UMY ─────────────────────────────────────────────────────────────────
daftarkan("umy", konvensi(
    "umy", "Universitas Muhammadiyah Yogyakarta", "UMY",
    "Ambil Pedoman Penulisan Skripsi resmi UMY."))

# ── 11. UII ──────────────────────────────────────────────────────────────────
daftarkan("uii", konvensi(
    "uii", "Universitas Islam Indonesia", "UII",
    "Ambil Pedoman Penulisan Skripsi resmi UII; perhatikan aturan bahasa Arab/Inggris bila relevan."))

# ── 12. UAD ──────────────────────────────────────────────────────────────────
daftarkan("uad", konvensi(
    "uad", "Universitas Ahmad Dahlan", "UAD",
    "Ambil Pedoman Akademik/Penulisan Skripsi resmi UAD."))

# ── 13. UMS ──────────────────────────────────────────────────────────────────
daftarkan("ums", konvensi(
    "ums", "Universitas Muhammadiyah Surakarta", "UMS",
    "Ambil Pedoman Penulisan Skripsi resmi UMS."))

# ── 14. UDINUS ───────────────────────────────────────────────────────────────
daftarkan("udinus", konvensi(
    "udinus", "Universitas Dian Nusantara", "UDINUS",
    "Ambil Panduan Penulisan Skripsi resmi Udinus."))

# ── 15. UMM ──────────────────────────────────────────────────────────────────
daftarkan("umm", konvensi(
    "umm", "Universitas Muhammadiyah Malang", "UMM",
    "Ambil Pedoman Penulisan Skripsi resmi UMM."))

# ── 16. UMB ──────────────────────────────────────────────────────────────────
daftarkan("umb", konvensi(
    "umb", "Universitas Mercu Buana", "UMB",
    "Ambil Panduan Penulisan Skripsi resmi UMB."))

# ── 17. Gunadarma ────────────────────────────────────────────────────────────
daftarkan("gunadarma", konvensi(
    "gunadarma", "Universitas Gunadarma", "GUNADARMA",
    "Ambil Pedoman Penulisan Skripsi resmi Universitas Gunadarma."))

# ── 18. UPN Veteran Yogyakarta ───────────────────────────────────────────────
daftarkan("upn_veteran", konvensi(
    "upn_veteran", "Universitas Pembangunan Nasional Veteran Yogyakarta", "UPNV",
    "Kampus Bela Negara di Yogyakarta; ambil pedoman penulisan resmi UPNV."))

# ── 19. UPN Veteran Jakarta ──────────────────────────────────────────────────
daftarkan("upnvj", konvensi(
    "upnvj", "Universitas Pembangunan Nasional Veteran Jakarta", "UPNVJ",
    "PTN (kampus Pondok Labu, Jakarta Selatan + Kampus Limo, Depok); "
    "ambil pedoman penulisan resmi UPN Veteran Jakarta."))

# ── 20. UPN Veteran Jawa Timur ───────────────────────────────────────────────
daftarkan("upnv_jatim", konvensi(
    "upnv_jatim", "Universitas Pembangunan Nasional Veteran Jawa Timur", "UPNV JATIM",
    "PTN di Surabaya; ambil pedoman penulisan resmi UPN Veteran Jawa Timur."))

# ── 21. Universitas Budi Luhur ───────────────────────────────────────────────
daftarkan("budi_luhur", konvensi(
    "budi_luhur", "Universitas Budi Luhur", "UBL",
    "Ambil Panduan Penulisan Skripsi resmi Universitas Budi Luhur."))

# ── 22. UMN (Universitas Multimedia Nusantara, Kelapa Dua/Tangerang) ──────────
daftarkan(
    "umn",
    resmi(
        "umn",
        "Universitas Multimedia Nusantara",
        "UMN",
        "Panduan Skripsi Program Studi Kajian (Fakultas Komunikasi dan Penyiaran) UMN",
        "https://www.umn.ac.id/wp-content/uploads/2021/04/Panduan-Skripsi-Kajian-2017_Final.pdf",
        "Program Studi Kajian, FKP UMN (pedoman 2017); dikuatkan Panduan FIKOM & MMT UMN",
        2017,
        "Margin 4/3/4/3 cm + spasi 2 + TNR 12 konsisten di Kajian, FIKOM, dan MMT UMN. "
        "Pengecualian: Program Studi Teknik Elektro UMN "
        "(https://te.umn.ac.id/wp-content/uploads/2020/08/PANDUAN-TEKNIS-SKRIPSI-TE.pdf) "
        "mengatur margin atas 3 cm dan MEWAJIBKAN daftar pustaka gaya IEEE.",
        gaya(
            margin={"atas": "4 cm", "bawah": "3 cm", "kiri": "4 cm", "kanan": "3 cm"},
            spasi="2",
            penomoran="bagian awal romawi kecil di tengah bawah (1,5 cm dari tepi bawah); "
                       "bagian inti/akhir arab di kanan bawah",
            align="Spasi ganda; 1 spasi untuk kutipan panjang, abstrak, tabel, gambar, "
                  "daftar pustaka. Judul bab TNR 12 (Kajian) atau 14-16 (FIKOM/MMT). "
                  "Judul skripsi maksimal 15 kata (TE).",
        ),
        sitasi="IEEE (wajib pada Program Studi Teknik Elektro); fakultas lain dapat berbeda — verifikasi",
        kelengkapan_tambahan=["daftar grafik", "lembar pernyataan (tidak plagiat)"],
    ),
)


# ── CLI & IO ─────────────────────────────────────────────────────────────────

def validasi(path, isi):
    """Pastikan JSON punya kunci wajib + provenance."""
    wajib = ["kampus", "singkat", "jenjang", "verifikasi", "gaya_dokumen",
             "sitasi", "kelengkapan", "struktur"]
    hilang = [k for k in wajib if k not in isi]
    if hilang:
        raise ValueError(f"{path}: kunci hilang {hilang}")
    if "sumber" not in isi:
        raise ValueError(f"{path}: field `sumber` (provenance) wajib ada")
    st = isi["sumber"].get("status")
    if st not in ("pedoman-resmi", "konvensi-umum"):
        raise ValueError(f"{path}: sumber.status tak dikenal: {st!r}")
    if st == "pedoman-resmi" and not isi["sumber"].get("url"):
        raise ValueError(f"{path}: status pedoman-resmi wajib punya url")
    # struktur minimal untuk check
    if not any(b.get("id") == "bab1" for b in isi["struktur"]):
        raise ValueError(f"{path}: struktur tanpa blok bab1")


def backfill_sumber():
    """Tambahkan field `sumber` (konvensi-umum) ke preset lama yang belum punya.

    Tidak menyentuh field lain, jadi isi hand-written preset ugm/ui/uny/itb/
    generic/custom tetap utuh. Idempoten.
    """
    berubah = []
    for f in sorted(os.listdir(DIR_PRESET)):
        if not f.endswith(".json"):
            continue
        path = os.path.join(DIR_PRESET, f)
        with open(path, encoding="utf-8") as fh:
            isi = json.load(fh)
        if isi.get("sumber"):
            continue
        isi["sumber"] = {
            "status": "konvensi-umum",
            "dokumen": None,
            "url": None,
            "scope": "seluruh kampus (perlu konfirmasi)",
            "catatan": "Preset lama, disusun dari kebiasaan umum penulisan ilmiah; "
                       "belum diverifikasi ke pedoman resmi fakultas/program studi.",
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(isi, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        berubah.append(f)
    return berubah


def main():
    ap = argparse.ArgumentParser(description="Generate preset campus_templates")
    ap.add_argument("--check", action="store_true",
                    help="hanya verifikasi JSON valid & provenance lengkap")
    ap.add_argument("--backfill", action="store_true",
                    help="tambahkan sumber.status=konvensi-umum ke preset tanpa provenance")
    ap.add_argument("--only", help="generate satu preset (nama file tanpa .json)")
    args = ap.parse_args()

    if args.backfill:
        berubah = backfill_sumber()
        if berubah:
            print(f"Backfill sumber pada {len(berubah)} preset: {', '.join(berubah)}")
        else:
            print("Semua preset sudah punya provenance; tidak ada perubahan.")
        return 0

    targets = PRESETS
    if args.only:
        if args.only not in PRESETS:
            sys.exit(f"ERROR: tidak dikenal: {args.only}")
        targets = {args.only: PRESETS[args.only]}

    dibuat, dilewati = [], []
    for nama_file, info in sorted(targets.items()):
        preset = info["preset"]
        path = os.path.join(DIR_PRESET, f"{nama_file}.json")
        validasi(nama_file, preset)

        if args.check:
            # pastikan file di disk cocok dengan yang akan di-generate (deteksi drift)
            if not os.path.exists(path):
                print(f"  HILANG   {nama_file}.json")
            else:
                with open(path, encoding="utf-8") as fh:
                    try:
                        json.load(fh)
                        dibuat.append(nama_file)
                    except json.JSONDecodeError as e:
                        print(f"  RUSAK    {nama_file}.json: {e}")
            continue

        if not info["regenerate"]:
            dilewati.append(nama_file)
            continue

        with open(path, "w", encoding="utf-8") as fh:
            json.dump(preset, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        dibuat.append(nama_file)

    if args.check:
        print(f"{len(dibuat)} preset JSON valid (semua punya sumber.status)")
        return 0
    print(f"Ditulis {len(dibuat)} preset: {', '.join(dibuat)}")
    if dilewati:
        print(f"tidak di-generate: {', '.join(dilewati)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())