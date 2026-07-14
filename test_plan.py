def generate_plan():
    print("""
1. **Understand Requirements & Context:**
   - The user asked to create a report `📊 Rapports/RAPPORT_SECURITE_PREUVES_2026-07-14.md` on evidence preservation.
   - The report needs to analyze video surveillance (Art. 145 CPC, Art. 434-4 CP, Art. 41/60-1 CPP), physical evidence (vasque, state of places under Art 1353 C. civ), digital evidence (web pages, under electronic proof rules like Art 1366 C. civ) and bank evidence (Wero 15€).
   - I have checked and verified:
     - Art. 1353 C. civ (`LEGIARTI000032042341`)
     - Art. 145 CPC (`LEGIARTI000006410268` / `LEGIARTI000051869339` - Wait I checked 145 CPC)
     - Art. 1369 C. civ (`LEGIARTI000032042446`), Art. 1366 C. civ (`LEGIARTI000032042461`)
     - Art. 434-4 Penal Code (`LEGIARTI000006418608`)
     - Art. 41 Penal Proc Code (`LEGIARTI000044569857` etc)
     - Art. 60-1 Penal Proc Code (`LEGIARTI000045292588`)
   - I will create the markdown file using `**[Tokens]**`.

2. **Draft the Report (`📊 Rapports/RAPPORT_SECURITE_PREUVES_2026-07-14.md`)**
   - Use the `CONVENTIONS.md` including YAML, `<hr><hr>`, and proper `**[Tokens]**`.
   - Organize into sections: I. Vidéosurveillance, II. Preuves matérielles, III. Preuves numériques, IV. Preuves bancaires, V. Matrice des preuves.

3. **Normalize and verify**
   - Run the normalization pipeline: `python3 .dev/app/normalize_sections.py --apply --token`, `python3 .dev/app/generate_real_versions.py`, `python3 .dev/app/normalize_sections.py --apply --reel`, `python3 .dev/app/check_consistency.py`.

4. **Complete pre commit steps**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

5. **Run test suite**
   - Run `uv run pytest .dev/tests/` to ensure no regressions.

6. **Submit PR**
   - Submit the branch using the submit tool.
""")
generate_plan()
