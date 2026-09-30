#!/usr/bin/env bash
# Smoke test untuk skill proposal-skripsi.
# Jalankan: bash tests/run_tests.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
S="$ROOT/scripts"
T="$ROOT/tests"
TMP="$(mktemp -d)"
PASS=0
FAIL=0

ok()   { PASS=$((PASS+1)); printf '  PASS  %s\n' "$1"; }
bad()  { FAIL=$((FAIL+1)); printf '  FAIL  %s\n' "$1"; }
have() { command -v "$1" >/dev/null 2>&1; }
head2() { printf '\n== %s ==\n' "$1"; }

head2 "1. ingest_sources.sh"
mkdir -p "$TMP/sumber"
bash "$S/ingest_sources.sh" "$TMP/sumber" --out "$TMP/cache" --json >/dev/null 2>&1
[ -f "$TMP/cache/sumber_inventaris.json" ] && ok "sumber_inventaris.json dibuat" || bad "inventaris JSON"
have pdftotext && printf '  INFO  pdftotext tersedia\n' || printf '  SKIP  pdftotext tidak terpasang\n'

head2 "2. profile_dataset.py"
python3 "$S/profile_dataset.py" "$T/sample_dataset.csv" --out "$TMP/profil" >/dev/null 2>&1
[ -f "$TMP/profil.md" ] && ok "profil.md dibuat" || bad "profil.md"
python3 "$S/profile_dataset.py" "$T/sample_dataset.csv" --json-only >/dev/null 2>&1 \
  && ok "mode --json-only" || bad "--json-only"

head2 "3. stats_tests.py"
run_stat() {
  desc="$1"; shift
  python3 "$S/stats_tests.py" "$T/sample_dataset.csv" "$@" --out "$TMP/st" >/dev/null 2>&1
  if [ -s "$TMP/st.md" ] && [ -s "$TMP/st.json" ]; then ok "$desc"; else bad "$desc"; fi
}
run_stat "--auto"            --auto
run_stat "regresi berganda"  --regresi "DV=Y_Kinerja_1,X=X1_Motivasi_1;X2_Kompetensi_1;Masa_Kerja_Tahun"
run_stat "t-test independen" --ttest-independen "DV=Y_Kinerja_1" --grup Divisi
run_stat "t-test berpasangan" --ttest-paired "DV1=Y_Kinerja_1,DV2=X1_Motivasi_1"
run_stat "anova"             --anova "DV=Y_Kinerja_1" --grup Divisi
run_stat "chi-square"        --chi2 "v1=Divisi,v2=Masa_Kerja_Tahun"
run_stat "pearson"           --korelasi "v1=X1_Motivasi_1,v2=Y_Kinerja_1"
run_stat "spearman"          --korelasi "v1=X1_Motivasi_1,v2=Y_Kinerja_1" --metode spearman
run_stat "cronbach"          --cronbach "a=Y_Kinerja_1,Y_Kinerja_2,Y_Kinerja_3,Y_Kinerja_4"
run_stat "alpha kustom"      --auto --alpha 0.01

head2 "3b. guard karakter non-Latin"
if grep -rlP '[\x{0400}-\x{04FF}\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' \
     "$ROOT" --include='*.md' --include='*.py' --include='*.sh' --include='*.json' \
     --exclude-dir=.git >/dev/null 2>&1; then
  bad "ditemukan karakter non-Latin yang tidak disengaja"
  grep -rlP '[\x{0400}-\x{04FF}\x{4E00}-\x{9FFF}\x{0600}-\x{06FF}]' \
     "$ROOT" --include='*.md' --include='*.py' --include='*.sh' --include='*.json' \
     --exclude-dir=.git | sed 's/^/        /'
else
  ok "tidak ada karakter non-Latin"
fi

head2 "4. nilai kritis (validasi internal)"
python3 - <<'PY' || exit 1
import sys
sys.path.insert(0, "scripts")
from stats_tests import t_sf_two_sided, f_sf, chi2_sf
checks = [
    ("t(10)=2.228 -> 0.050", t_sf_two_sided(2.228, 10), 0.050, 0.002),
    ("chi2(1)=3.841 -> 0.050", chi2_sf(3.841, 1), 0.050, 0.002),
    ("chi2(9)=16.919 -> 0.050", chi2_sf(16.919, 9), 0.050, 0.002),
    ("F(3,26)=18.70 -> 1.1e-6", f_sf(18.70, 3, 26), 1.13e-6, 2e-7),
]
bad = 0
for name, got, want, tol in checks:
    if abs(got - want) <= tol:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name} (peroleh {got:.6g})")
        bad += 1
sys.exit(1 if bad else 0)
PY
[ $? -eq 0 ] && PASS=$((PASS+4)) || FAIL=$((FAIL+1))

head2 "5. id_language_check.py"
if [ -f "$S/id_language_check.py" ]; then
  python3 "$S/id_language_check.py" "$T/contoh_bab1.md" >/dev/null 2>&1 \
    && ok "menjalankan tanpa galat" || bad "menjalankan"
else
  printf '  SKIP  belum ada\n'
fi

head2 "6. proposal_doctor.py"
if [ -f "$S/proposal_doctor.py" ]; then
  python3 "$S/proposal_doctor.py" "$T/contoh_proposal_lengkap.md" \
      --dataset "$T/sample_dataset.csv" --hasil-uji "$TMP/auto.json" \
      --json "$TMP/doctor.json" >/dev/null 2>&1
  if python3 -c "import json,sys;d=json.load(open('$TMP/doctor.json'));sys.exit(1 if d['galat'] else 0)" 2>/dev/null; then
    ok "proposal lengkap: 0 galat"
  else
    bad "proposal lengkap menghasilkan galat"
  fi
  python3 "$S/proposal_doctor.py" "$T/contoh_bab1.md" --strict >/dev/null 2>&1 \
    && bad "naskah cacat seharusnya gagal dengan --strict" || ok "naskah cacat terdeteksi (--strict)"
else
  printf '  SKIP  belum ada\n'
fi

head2 "7. build_docx.sh"
if have pandoc; then
  cp "$T/contoh_proposal_lengkap.md" "$TMP/proposal.md"
  bash "$S/build_docx.sh" "$TMP/proposal.md" --out-dir "$TMP/docx" --toc --clean >/dev/null 2>&1
  [ -s "$TMP/docx/proposal.docx" ] && ok "DOCX dibuat" || bad "DOCX"
  python3 "$S/proposal_doctor.py" "$TMP/proposal.md" --docx "$TMP/docx/proposal.docx" \
      >/dev/null 2>&1 && ok "dokumen lolos pemeriksaan" || bad "dokumen gagal pemeriksaan"
else
  printf '  SKIP  pandoc tidak terpasang\n'
fi

head2 "8. apply_campus_template.py"
python3 "$S/apply_campus_template.py" list >/dev/null 2>&1 && ok "list" || bad "list"
for preset in ugm ui uny itb generic custom; do
  python3 -c "import json,sys;json.load(open('$ROOT/campus_templates/$preset.json'))" 2>/dev/null \
    && ok "JSON $preset valid" || bad "JSON $preset"
done
python3 "$S/apply_campus_template.py" init generic -o "$TMP/krangka.md" \
    --judul "Uji" --nama "Uji" --nim "1" --pembimbing "Uji" --tahun 2026 >/dev/null 2>&1 \
    && [ -s "$TMP/krangka.md" ] && ok "init membuat kerangka" || bad "init"
python3 "$S/apply_campus_template.py" check ugm "$T/contoh_proposal_lengkap.md" >/dev/null 2>&1 \
    && ok "proposal lengkap lolos preset ugm" || bad "proposal lengkap gagal di preset ugm"
python3 "$S/apply_campus_template.py" check ugm "$T/contoh_bab1.md" >/dev/null 2>&1 \
    && bad "naskah cacat seharusnya gagal" || ok "naskah cacat terdeteksi"

head2 "9. code_interview.py"
python3 "$S/code_interview.py" apply "$T/codebook_contoh.csv" \
    --transkrip "$T/transkrip_contoh.md" --out "$TMP/koding" >/dev/null 2>&1
[ -s "$TMP/koding.md" ] && [ -s "$TMP/koding.json" ] && ok "pengodean menghasilkan md+json" || bad "pengodean"
python3 -c "
import json,sys
d=json.load(open('$TMP/koding.json'))
ada=[t['kode'] for t in d['tabel'] if t['jumlah_unit']>0]
sys.exit(0 if len(ada)>=3 else 1)" 2>/dev/null \
    && ok "kode aktif terdeteksi" || bad "kode aktif"
python3 "$S/code_interview.py" report "$TMP/koding.json" --out "$TMP/koding2.md" >/dev/null 2>&1 \
    && ok "report ulang" || bad "report"

head2 "10. export_referensi.py"
for gaya in apa vancouver ieee; do
  python3 "$S/export_referensi.py" "$T/matriks_referensi_contoh.csv" \
      --out-dir "$TMP/ref_$gaya" --gaya "$gaya" --quiet >/dev/null 2>&1
  if [ -s "$TMP/ref_$gaya/referensi.bib" ] && [ -s "$TMP/ref_$gaya/referensi.ris" ] \
     && [ -s "$TMP/ref_$gaya/referensi.xml" ] && [ -s "$TMP/ref_$gaya/referensi.txt" ]; then
    ok "ekspor $gaya (bib/ris/xml/txt)"
  else
    bad "ekspor $gaya"
  fi
done
python3 -c "import xml.dom.minidom;xml.dom.minidom.parse('$TMP/ref_apa/referensi.xml')" 2>/dev/null \
    && ok "EndNote XML well-formed" || bad "EndNote XML rusak"
python3 "$S/export_referensi.py" "$T/matriks_referensi_contoh.csv" --periksa >/dev/null 2>&1 \
    && bad "matriks cacat seharusnya dilaporkan" || ok "periksa menandai field kosong"
grep -q "10.1234/jmi.2020.12.3.145" "$TMP/ref_apa/referensi.bib" 2>/dev/null \
    && ok "DOI diteruskan apa adanya" || bad "DOI hilang"

head2 "11. konsistensi dokumentasi"
# 11a. setiap path yang disebut SKILL.md/README.md harus benar-benar ada
BROKEN="$(python3 - "$ROOT" <<'PY'
import os, re, sys
root = sys.argv[1]
docs = ["SKILL.md", "README.md"] + [
    os.path.join(root, "references", f) for f in sorted(os.listdir(os.path.join(root, "references")))
]
pat = re.compile(r"(?:\]\(([^)\s]+)\)|`((?:references|templates|scripts|campus_templates|tests)/[A-Za-z0-9_./-]+)`)")
missing = []
for d in docs:
    p = d if os.path.isabs(d) else os.path.join(root, d)
    if not os.path.isfile(p):
        continue
    for m in pat.finditer(open(p, encoding="utf-8").read()):
        rel = (m.group(1) or m.group(2)).split("#")[0]
        if not rel or rel.startswith(("http://", "https://", "mailto:")):
            continue
        if not os.path.exists(os.path.join(root, rel)):
            missing.append(f"{os.path.relpath(p, root)} -> {rel}")
print("\n".join(sorted(set(missing))))
PY
)"
if [ -z "$BROKEN" ]; then
  ok "semua path di SKILL.md/README.md/references resolve"
else
  bad "path hilang di dokumentasi:"
  printf '        %s\n' $BROKEN
fi

# 11b. setiap script & template harus disebut minimal sekali di SKILL.md
UNWIRED="$(python3 - "$ROOT" <<'PY'
import os, sys
root = sys.argv[1]
skill = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
missing = []
for sub in ("scripts", "templates", "campus_templates"):
    d = os.path.join(root, sub)
    for f in sorted(os.listdir(d)):
        if f.startswith(".") or f == "__pycache__":
            continue
        if not os.path.isfile(os.path.join(d, f)):
            continue
        if f not in skill:
            missing.append(f"{sub}/{f}")
print("\n".join(missing))
PY
)"
if [ -z "$UNWIRED" ]; then
  ok "setiap script/template/preset disebut di SKILL.md"
else
  bad "tak ter-wire di SKILL.md:"
  printf '        %s\n' $UNWIRED
fi

# 11c. tiap script .py harus punya --help yang tidak error
HELPBAD=""
for f in "$S"/*.py; do
  python3 "$f" --help >/dev/null 2>&1 || HELPBAD="$HELPBAD $(basename "$f")"
done
if [ -z "$HELPBAD" ]; then
  ok "semua script .py punya --help yang valid"
else
  bad "--help gagal:$HELPBAD"
fi

printf '\n== RINGKASAN ==\nPASS: %d  FAIL: %d  (log: %s)\n' "$PASS" "$FAIL" "$TMP"
[ "$FAIL" -eq 0 ]
