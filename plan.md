1. **Explore Context and Gather Rules**
   - The user asked to create a report `📊 Rapports/RAPPORT_SECURITE_PREUVES_2026-07-14.md` on the strategy of conservation and securing of evidence.
   - We must adhere to the `CONVENTIONS.md` format (YAML, breadcrumbs, `<hr><hr>`, tokens).
   - Use tokens: `**[La Victime]**`, `**[L'Exploitant du Commerce (La SAS)]**`, `**[Le Préposé de l'Exploitation]**`, `**[Le Président de l'Exploitation]**`, `**[La Directrice Générale de l'Exploitation]**`.
   - The matrix will cross-reference the claim (SAS liability, Director liability, damage claims) with the corresponding evidence.

2. **Verify Articles (Groundedness Rule)**
   - Art. 1353 C. civ (Burden of proof) - Verified
   - Art. 145 CPC (In futurum measures for evidence) - Verified
   - Art. 1369 C. civ (Authentic act) - Verified
   - Art. 1366 C. civ (Electronic evidence equivalent to written) - Verified
   - Art. 434-4 Penal Code (Destruction of evidence) - Verified
   - Art. 41 and 60-1 Penal Procedure Code (Prosecutor's role and evidence requisition) - Verified
   - Art. 1127-1 C. civ (Electronic contract rules, for Wero proof) - Verified

3. **Draft the Report**
   - We will write `📊 Rapports/RAPPORT_SECURITE_PREUVES_2026-07-14.md`.
   - Structure:
     - YAML front matter
     - Breadcrumb
     - `I — VIDÉOSURVEILLANCE (MESURES IN FUTURUM ET RISQUE PÉNAL)`
     - `II — PREUVES MATÉRIELLES (VASQUE ET LIEUX)`
     - `III — PREUVES NUMÉRIQUES (INTERNET ET RÉSEAUX SOCIAUX)`
     - `IV — PREUVES BANCAIRES ET RELATION CONTRACTUELLE`
     - `V — MATRICE PROBATOIRE ET CHEFS DE PRÉTENTION`

4. **Normalize Sections and Verification**
   - Run python scripts for normalization: `python3 .dev/app/normalize_sections.py --apply --token`, `python3 .dev/app/generate_real_versions.py`, `python3 .dev/app/normalize_sections.py --apply --reel`
   - Run `python3 .dev/app/check_consistency.py`

5. **Pre commit instructions**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

6. **Submit Pull Request**
   - Use `submit` to push branch.
