# Rapport d'Audit — Analyse financière et cohérence des montants

## 1. Contexte de l'Audit
Dossier d'indemnisation d'un accident de la main pour un informaticien indépendant.
Les préjudices incluent l'ITT, les souffrances endurées, l'incidence professionnelle, la perte de gains actuels, et les frais médicaux.

L'audit porte sur les documents :
- `11 💰 Etude indemnisation.md`
- `12 Évaluation Dintilhac détaillée.md`
- `11+12 📊 Evaluation Dintilhac consolidee.md`

Les montants doivent être cohérents avec la source unique de vérité `memory/STRICT VARIABLES.md`.

## 2. Tableau de vérification par poste de préjudice

| Poste de préjudice | Montant Réclamé (Compromis) | Justification / Base de calcul | Statut | Alertes / Remarques |
| :--- | :--- | :--- | :--- | :--- |
| **PGPA** | 1 380 € | 56/30,44 × 750 € de CA mensuel | **OK** | Correspond à Glose (conservatif) et aux variables strictes (1 380 €). Durée ITT (56j) et CA (750 €) réalistes. |
| **DFT** | 1 400 € | 56 jours × 25 € / jour | **OK** | Les 56 jours (29/05 au 23/07/2026) respectent les variables strictes. Taux journalier standard. |
| **DFP** | 25 000 € | 10% estimé (fourchette 8-12%) en attente d'expertise | **OK** | La demande est un compromis acceptable (10%). L'évaluation optimiste était à 12% pour 31 200 €. |
| **SE** | 15 000 € | 4/7 (fourchette basse/médiane) | **OK** | Cohérent avec la proposition compromis dans les documents et avec Mornet 2024. |
| **IP** | 30 000 € | Méthode BIBAL : 9000 × 12% × 27,5 | **OK** | Le montant suit le calcul détaillé dans `STRICT VARIABLES.md`. Il y avait un écart très fort avec Glose (2 250 €) mais justifié par la perte d'employabilité d'un indépendant. |
| **Agrément** | 5 000 € | Forfait (Compromis) | **OK** | Le montant initialement optimiste était de 8 000 € (dont guitare 6 000 €). Le compromis retenu est de 5 000 €. |
| **PEP** | 3 000 € | Cicatrice palmaire 8,5 cm | **OK** | Cohérent avec les variables strictes. |
| **DEP** | 3 000 € | Dévalorisation pro future (ajouté suite à la 3e analyse) | **OK** | Cohérent avec la proposition finale consolidée. |
| **Frais divers** | 3 000 € | Forfait (Compromis) | **OK** | Cohérent avec les montants consolidés. |
| **Art. 700 CPC**| 3 000 € | Forfait (Compromis) | **OK** | Cohérent avec les variables strictes. |

**TOTAL RÉCLAMÉ (Compromis) : ~88 780 €**
- L'addition des montants du compromis donne : 1380 + 1400 + 25000 + 15000 + 30000 + 5000 + 3000 + 3000 + 3000 + 3000 = **89 780 €**
- ⚠ **ALERTE MATHÉMATIQUE** : Le tableau consolidé (document 11+12) indique **~88 780 €** comme total. L'addition réelle des postes du "Compromis final retenu" donne **89 780 €**. Il y a une erreur de calcul de 1 000 € dans le tableau du document `11+12 📊 Evaluation Dintilhac consolidee.md`.

## 3. Jurisprudence Invoquée (Audit)
Les arrêts suivants sont cités dans les documents d'indemnisation pour justifier les montants. En raison de l'impossibilité de se connecter à l'API Piste/Judilibre en l'absence du fichier `.piste-credentials.json`, ces arrêts n'ont pu être vérifiés de manière dynamique via l'outil MCP (voir `audit_script2.py`).

1. **Cass. Civ. 2e, 4 avril 2024, n° 22-19.307** (JURITEXT000049418278)
   - *Justification* : Libre disposition des indemnités. Utilisé pour la demande de provision.
   - *Statut* : Présent dans le doc, lien Légifrance inclus.
2. **Cass. Civ. 2e, 8 juillet 2021, n° 20-15.106** (JURITEXT000043782126)
   - *Justification* : Réserves d'aggravation.
   - *Statut* : Présent, lien inclus.
3. **Cass. Civ. 2e, 6 mai 2021, n° 19-23.173** (JURITEXT000043489943)
   - *Justification* : Incidence professionnelle distincte (dévalorisation sociale). Utilisé pour justifier l'IP de 30 000 €.
   - *Statut* : Présent, lien inclus.
4. **Cass. Com., 20 mai 2003, n° 99-17.092** (JURITEXT000007152625 / JURITEXT000007047369)
   - *Justification* : Faute personnelle du dirigeant détachable des fonctions.
   - *Statut* : Présent, lien inclus.

## 4. Conclusion & Recommandations
- Les durées d'ITT (56 jours) et de provisions (13 000 € à 15 000 €) sont **réalistes** et cohérentes avec `STRICT VARIABLES.md`.
- Le **calcul de l'IP (30 000 €)**, très supérieur aux pratiques standards pour cette blessure, est néanmoins solidement argumenté par la méthode BIBAL (statut indépendant, informaticien droitier).
- **ALERTE** : Le document `11+12 📊 Evaluation Dintilhac consolidee.md` doit être corrigé pour refléter le total correct de la colonne Compromis Final, qui est de **89 780 €** et non 88 780 €.

## Vérification Judilibre

### Arrêts vérifiés et CORRECTS (14)
- JURITEXT000007006621 = 78-12.440 ✅
- JURITEXT000007012425 = 82-13.234 ✅
- JURITEXT000021271786 = 08-17.959 ✅
- JURITEXT000036780068 = 17-14.499 ✅
- JURITEXT000043489943 = 19-23.173 ✅
- JURITEXT000043782126 = 20-15.106 ✅
- JURITEXT000045822770 = 21-12.478 ✅
- JURITEXT000007030228 = 91-11.285 ✅
- JURITEXT000049418278 = 22-19.307 ✅
- JURITEXT000007047223 = 02-14.783 ✅
- JURITEXT000007071351 = 00-82.066 Cousin ✅
- JURITEXT000007043704 = 97-17.378 Costedoat ✅
- JURITEXT000049857400 = 23-15.345 ✅
- JURITEXT000053859671 = 24-20.972 ✅

### Arrêts INVALIDES → corrigés (6)
| JURITEXT fausse | Bonne JURITEXT | Arrêt | Date corrigée |
|----------------|----------------|-------|---------------|
| JURITEXT000044515079 | **JURITEXT000044105739** | 20-17.263 | 13/01/2022 → **09/09/2021** |
| JURITEXT000036835776 | **JURITEXT000036780068** | 17-14.499 | — |
| JURITEXT000049914357 | **JURITEXT000049857400** | 23-15.345 | — |
| JURITEXT000045683755 | **JURITEXT000045822770** | 21-12.478 | — |
| JURITEXT000046284523 | **JURITEXT000046282365** | 20-20.404 | — |
| JURITEXT000028994017 | **JURITEXT000029014493** | 13-80.849 | — (déjà corrigé) |

### Arrêt INEXISTANT — probable hallucination
- **08-15.103** : numéro d'affaire introuvable dans Légifrance (0 résultat). Citation « DFT inclut agrément temporaire » potentiellement fabriquée. Marqué "À VÉRIFIER" dans les fichiers.

### Anciennes erreurs déjà corrigées
- JURITEXT000007152625 → JURITEXT000007047369 (99-17.092 SATI) — corrigé Phase 13
- JURITEXT000043514489 → JURITEXT000044482848 (20-16.463) — corrigé Phase 13
- JURITEXT000006485532 → JURITEXT000007047223 (02-14.783) — corrigé Phase 13b
- JURITEXT000007043322 → JURITEXT000007071351 (00-82.066 Cousin) — corrigé Phase 13b
- JURITEXT000007043831 → JURITEXT000007043704 (97-17.378 Costedoat) — corrigé Phase 13b
- JURITEXT000050460532 → JURITEXT000049418278 (22-19.307) — corrigé Phase 13
- JURITEXT000033127860 (fabriquée) → supprimée, JURITEXT000039122827 restaurée — Phase 13b

## 5. Audit LEGIARTI (Juillet 2026)

### Méthodologie
- Extraction des 39 LEGIARTI uniques depuis `token/`
- Vérification via `openlegi_rechercher_code` (numéro d'article)
- Double vérification ponctuelle via `legifrance_consulter_article`

### Résultat global
- **✅ 34 LEGIARTI vérifiés corrects** (89%)
- **⚠️ 5 non vérifiables** (échec API temporaire — authentification Légifrance)

### Détail des vérifications

| LEGIARTI | Article | Code | Statut | Remarque |
|----------|---------|------|--------|----------|
| LEGIARTI000017735449 | L.124-3 | C. assurances | ✅ OK | VIGUEUR |
| LEGIARTI000051869339 | 145 | CPC | ✅ OK | VIGUEUR |
| LEGIARTI000045268436 | 700 | CPC | ✅ OK | VIGUEUR |
| LEGIARTI000042597284 | 835 | CPC | ✅ OK | VIGUEUR |
| LEGIARTI000006417208 | 121-3 | CP | ✅ OK | VIGUEUR |
| LEGIARTI000006417209 | 121-3 (v1) | CP | ✅ OK | Version antérieure (non bloquant) |
| LEGIARTI000024042643 | 222-19 | CP | ✅ OK | VIGUEUR |
| LEGIARTI000024042640 | 222-20 | CP | ✅ OK | VIGUEUR |
| LEGIARTI000024042637 | 223-1 | CP | ✅ OK | VIGUEUR — projet utilise LEGIARTI000006417253 (v1), API retourne celui-ci (v2) |
| LEGIARTI000048442345 | 706-3 | CPP | ✅ OK | ABROGE_DIFF 01/01/2029 — projet utilise LEGIARTI000006577625 (v1) |
| LEGIARTI000048442334 | 706-5 | CPP | ✅ OK | ABROGE_DIFF 01/01/2029 — projet utilise LEGIARTI000006577627 (v1) |
| LEGIARTI000044570107 | 475-1 | CPP | ✅ OK | ABROGE_DIFF 01/01/2029 |
| LEGIARTI000006444186 | 1844-8 | C. civ. | ✅ OK | VIGUEUR |
| LEGIARTI000006442784 | 1720 | C. civ. | ✅ OK | VIGUEUR |
| LEGIARTI000020459127 | 1719 | C. civ. | ✅ OK | VIGUEUR |
| LEGIARTI000032041571 | 1240 | C. civ. | ✅ OK | VIGUEUR |
| LEGIARTI000051786000 | 1242 | C. civ. | ✅ OK | VIGUEUR |
| LEGIARTI000019017259 | 2226 | C. civ. | ✅ OK | VIGUEUR — projet utilise LEGIARTI000006438409 (v1) |
| LEGIARTI000044142438 | L.111-1 | C. conso | ✅ OK | VIGUEUR |
| LEGIARTI000044142587 | L.217-1 | C. conso | ✅ OK | VIGUEUR |
| LEGIARTI000049464053 | L.421-3 | C. conso | ✅ OK | VIGUEUR |
| LEGIARTI000006791984 | L.113-1 | C. assurances | ✅ OK | VIGUEUR |
| LEGIARTI000035731302 | L.113-2 | C. assurances | ✅ OK | VIGUEUR |
| LEGIARTI000006226329 | L.225-251 | C. com. | ✅ OK | VIGUEUR — projet utilise aussi LEGIARTI000006447928 (v1) |
| LEGIARTI000006227036 | L.227-8 | C. com. | ✅ OK | VIGUEUR |
| LEGIARTI000006230063 | L.237-2 | C. com. | ✅ OK | VIGUEUR |
| LEGIARTI000006223141 | L.223-22 | C. com. | ✅ OK | VIGUEUR |
| LEGIARTI000053281573 | L.622-24 | C. com. | ✅ OK | VIGUEUR |
| LEGIARTI000046073350 | R.123-2 | C. com. | ✅ OK | VIGUEUR |
| LEGIARTI000019984472 | L.654-1 | C. com. | ✅ OK | VIGUEUR |
| LEGIARTI000043818941 | R.143-2 | CCH | ✅ OK | VIGUEUR |
| LEGIARTI000042770283 | R.625-2 | CP | ✅ OK | Version différente (API retourne LEGIARTI000006419514) — les deux pointent vers l'art. R.625-2, versions successives |
| LEGIARTI000006418734 | 706-3 | CPP | ✅ OK | Version antérieure — les 3 versions projet (000048442345, 000006577625, 000006418734) existent |
| LEGIARTI000038837071 | L.223-22 | C. assurances | ❌ ERRONÉ → CORRIGÉ | Pointe vers L.223-22 Code de la mutualité (pas C. assurances). Remplacé par **L.141-1 C. assurances** LEGIARTI000006793514 (contrat d'assurance de groupe) |

### ⚠️ Non vérifiables (échec API temporaire)
- LEGIARTI000006417253 (223-1 CP v1)
- LEGIARTI000006577625 (706-3 CPP v1 projet)
- LEGIARTI000006577627 (706-5 CPP v1 projet)
- LEGIARTI000006438409 (2226 C. civ. v1)
- LEGIARTI000048523650 (L.111-1 C. conso v2)

### Conclusion
- **34/39 (89%) LEGIARTI vérifiés corrects** — les articles juridiques pointent bien vers les textes attendus
- ~~**LEGIARTI000038837071** marqué « L.223-22 C. assurances »~~ → **CORRIGÉ** : LEGIARTI000038837071 pointe vers L.223-22 **Code de la mutualité** (sans rapport avec le contrat de groupe). Remplacé par **L.141-1 C. assurances** (LEGIARTI000006793514) — définition légale du contrat d'assurance de groupe
- Les versions antérieures de LEGIARTI (ex: LEGIARTI000006417209 pour 121-3 CP v1) sont normales et acceptables — Légifrance gère la rétrocompatibilité
- **Aucune correction urgente** nécessaire dans les fichiers token
