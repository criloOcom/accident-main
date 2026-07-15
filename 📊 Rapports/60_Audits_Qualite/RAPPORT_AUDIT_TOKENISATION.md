---
title: "RAPPORT D'AUDIT DE TOKENISATION"
description: "Date :** 10 juillet 2026"
type: rapport
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports et Analyses](./README.md) › RAPPORT AUDIT TOKENISATION*
<hr>
<!-- /Breadcrumb -->

# RAPPORT D'AUDIT DE TOKENISATION

**Date :** 10 juillet 2026
**Objet :** Audit des fuites de données personnelles dans [⚖️ Actes/🔑 Token](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md)
**Méthode :** Scan regex exhaustif (noms, emails, adresses, SIREN, téléphones, dates brutes) + revue manuelle

---

## Résumé exécutif

**Gravité : CRITIQUE** — 8 fichiers tokenisés contiennent des données personnelles en clair. La TOKEN MAP est incomplète (6 tokens manquants). Le script `generate_real_versions.py` et `batch_anonymize.py` sont désynchronisés.

---

## 1. FUITES CRITIQUES — Données personnelles en clair

### 🔴 FUITE 1 — Identité complète de la Victime (pièce maîtresse)

| Fichier | Ligne | Extrait |
|---|---|---|
| `🗂️ Organisation/22 📋 Modif Email Maire Foix.md` | 44 | `Sébastien GRAZIDE` |
| `🗂️ Organisation/22 📋 Modif Email Maire Foix.md` | 45 | `10 Avenue de Purpan, 31700 Blagnac` |
| `🗂️ Organisation/22 📋 Modif Email Maire Foix.md` | 46 | `sebastien.grazide@gmail.com` |
| `🗂️ Organisation/24 ✅ Checklist Envoi 11-07-2026.md` | 62 | `Sebastien GRAZIDE` |
| `🗂️ Organisation/24 ✅ Checklist Envoi 11-07-2026.md` | 69 | `Sebastien GRAZIDE` |

**Risque :** Le token `**[La Victime]**` est contourné — l'identité réelle apparaît en clair dans deux fichiers du dossier tokenisé.

### 🔴 FUITE 2 — Identité complète des dirigeants de la SAS

| Fichier | Ligne | Extrait |
|---|---|---|
| `📚 Analyses juridiques/18 Note Audit RNE NPAI SAS.md` | 27 | `Sabir MOUNTASSER, né 1992, 108 Cité Aimé Surre, 09000 Foix` |
| `📚 Analyses juridiques/18 Note Audit RNE NPAI SAS.md` | 28 | `Catherine SORROCHE/ANDISSAC, née 1970, 7 Rue Camille Mussat, 31100 Toulouse` |

**Risque :** Les noms complets, dates de naissance et adresses personnelles des dirigeants sont en clair. Cette note est un document d'audit RNE qui documente les identités réelles à côté des tokens — elle n'a pas été anonymisée.

### 🔴 FUITE 3 — Adresse email de l'Adjoint au Maire (Tiers)

| Fichier | Ligne | Extrait |
|---|---|---|
| `✉️ Courriers/34 ✉️ EMAIL Maire Foix - Police Municipale ERP.md` | 7 | `M. Bernard TAVELLA` |
| `✉️ Courriers/34 ✉️ EMAIL Maire Foix - Police Municipale ERP.md` | 13 | `btavella@mairie-foix.fr` |
| `✉️ Courriers/34 ✉️ EMAIL Maire Foix - Police Municipale ERP.md` | 14 | `secretariat@mairie-foix.fr` |

**Risque :** Les emails réels d'un tiers (agent public) sont en clair dans un fichier tokenisé. Le token `**[L'Adjoint au Maire de la Commune]**` existe dans le script mais n'a pas été appliqué ici (le nom `Bernard TAVELLA` apparaît en clair en ligne 7).

### 🔴 FUITE 4 — Adresse email Mairie de Foix (suggestion)

| Fichier | Ligne | Extrait |
|---|---|---|
| `🗂️ Organisation/21 📋 Plan Constat Police Foix.md` | 37 | `mairie@mairie-foix.fr` |

### 🔴 FUITE 5 — SIREN en clair (identifiant société)

| Fichier | Ligne | Extrait |
|---|---|---|
| `📚 Analyses juridiques/18 Note Audit RNE NPAI SAS.md` | 23 | `938 033 222` |
| `✉️ Courriers/35 ✉️ Courrier President TJ Foix.md` | 94 | `(938 033 222)` |
| `✉️ Courriers/19 ✉️ Courrier FGTI.md` | 142 | `(938 033 222)` |
| `✉️ Courriers/14 ✉️ Courrier CODAF.md` | 102 | `(938 033 222)` |
| `✉️ Courriers/12 ✉️ Courrier URSSAF.md` | 99 | `(938 033 222)` |

**Risque :** Le SIREN `938 033 222` apparaît en clair dans 5 fichiers différents, bien qu'un token `**[SIREN de l'Exploitation]**` existe dans le script. L'anonymisation par lots n'a pas traité ces fichiers, ou le token n'a pas été utilisé lors de la rédaction.

### 🔴 FUITE 6 — Adresses en clair dans plusieurs fichiers

| Fichier | Ligne | Extrait |
|---|---|---|
| `📚 Analyses juridiques/18 Note Audit RNE NPAI SAS.md` | 25 | `22 Rue Lafaurie, 09000 Foix` |
| `📚 Analyses juridiques/18 Note Audit RNE NPAI SAS.md` | 30 | `22 Rue Lafaurie` |
| `🗂️ Organisation/21 📋 Plan Constat Police Foix.md` | 40, 46 | `22 rue Lafaurie`, `22 Rue Lafaurie à Foix` |
| `🗂️ Organisation/22 📋 Modif Email Maire Foix.md` | 21, 25, 29 | `22 Rue Lafaurie` (3 occurrences) |

### 🔴 FUITE 7 — Nom de la SAS en clair

| Fichier | Ligne | Extrait |
|---|---|---|
| `🗂️ Organisation/21 📋 Plan Constat Police Foix.md` | 48 | `SAS LES MAUVAIS GARCONS` |
| `🗂️ Organisation/22 📋 Modif Email Maire Foix.md` | 29 | `SAS LES MAUVAIS GARCONS` |
| `🗂️ Organisation/24 ✅ Checklist Envoi 11-07-2026.md` | 31, 37 | `SAS LES MAUVAIS GARCONS` |

### 🟡 FUITE 8 — Nom médical en clair

| Fichier | Ligne | Extrait |
|---|---|---|
| `🗂️ Organisation/06 📋 Synthese des Actions et Audits.md` | 20 | `Dr DJERBI` |

### 🟡 FUITE 9 — Dates brutes non tokenisées

| Fichier | Ligne | Extrait |
|---|---|---|
| `⚖️ Actes proceduraux/05 🎯 Conclusions Refere.md` | 42 | `29 mai 2026` |
| `⚖️ Actes proceduraux/15 ⚖️ Réquisitoire introductif.md` | 40, 42 | `29 mai 2026`, `30 mai 2026` |
| `✉️ Courriers/31 ✉️ Courrier INPI Opposition.md` | 37 | `29 mai 2026` |
| `✉️ Courriers/33 ✉️ Requete Constat Huissier 145 CPC.md` | 55 | `30 mai 2026` |
| `✉️ Courriers/34 ✉️ EMAIL Maire Foix - Police Municipale ERP.md` | 22, 24 | `29 mai 2026`, `1er juin 2026` |
| `✉️ Courriers/35 ✉️ Courrier President TJ Foix.md` | 35 | `29 mai 2026` |
| `🗂️ Organisation/21 📋 Plan Constat Police Foix.md` | 46 | `29 mai 2026` |
| `🗂️ Organisation/22 📋 Modif Email Maire Foix.md` | 25 | `29 mai 2026` |

**Risque :** Les dates clés de l'accident sont en clair. Les tokens `**[J+0 Accident]**`, `**[J+1 Chirurgie]**` etc. existent mais n'ont pas été utilisés dans ces fichiers.

---

## 2. TOKEN MAP — État des lieux

### ✅ Tokens présents dans la TOKEN MAP

| Catégorie | Nombre | Exemples |
|---|---|---|
| Personnes physiques | 8 | `**[La Victime]**`, `**[Le Président...]**`, etc. |
| Personnes morales | 2 | `**[L'Exploitant du Commerce (La SAS)]**`, `**[L'Établissement SOS Main]**` |
| Adresses/villes | 8 | `**[L'Adresse de la Victime]**`, `**[La Ville de l'Accident]**`, etc. |
| Identifiants | 5 | `**[L'Email de la Victime]**`, `**[L'Identifiant Professionnel...]**`, etc. |

### ❌ Tokens MANQUANTS dans la TOKEN MAP (présents dans le script ou les fichiers)

| Token | Valeur réelle (script) | Utilisé dans |
|---|---|---|
| `**[L'Adjoint au Maire de la Commune]**` | Monsieur TAVELLA | `✉️ Courriers/09`, `✉️ Courriers/08` |
| `**[L'Email de l'Adjoint au Maire]**` | *manquant* | `🗄️ Archives/🧠 STRATEGIE Contentieux Penal.md` |
| `**[Agent PJ, dépôt de plainte]**` | Jordy RODRIGUEZ CAPARROS | `⚖️ Actes proceduraux/04`, `📂 Preuves officielles/01` |
| `**[SMUR local]**` | SMUR 09 | `⚖️ Actes proceduraux/01`, `⚖️ Actes proceduraux/03`, `🗄️ Archives/📚 ANALYSE` |
| `**[Le Téléphone de la Victime]**` | 06 30 51 67 75 | *(défini dans script, non vérifié dans fichiers)* |
| `**[SIREN de l'Exploitation]**` | 938 033 222 | `✉️ Courriers/14, 12, 19, 35`, `01_⚖️ Actes/33` |
| `**[SIRET de l'Exploitation]**` | 938 033 222 00010 | *(défini dans script)* |
| `**[N° LRAR Exploitant]**` + 4 variantes | 87001424863012T etc. | *(défini dans script)* |
| `**[N° Transaction Wero]**` | IPR000297029234 | *(défini dans script)* |
| `**[Adresse du Commerce]**` | 22 Rue Lafaurie, 09000 Foix | `✉️ Courriers/08` |
| `**[Centre de soins immédiats]**` | Centre Ariégeois de Soins Immédiats | *(défini dans script)* |

---

## 3. Script `generate_real_versions.py` — Incohérences

### Problèmes détectés

1. **TOKEN MAP ≠ REVERSE_MAP** — La REVERSE_MAP contient 60+ entrées, la TOKEN MAP en contient ~20. Toute entrée dans la REVERSE_MAP devrait avoir sa contrepartie dans la TOKEN MAP.

2. **Tokens en double dans REVERSE_MAP** — Lignes 6-7 et 17-18 dupliquées : `**[La Victime]**`, `**[Le Président...]**`, `**[La Directrice...]**`, `**[Le Préposé...]**`. Idem lignes 9-11 et 23-25 pour `**[Le Propriétaire...]**`.

3. **Variantes accentuées/non accentuées** incomplètes : `**[Le President de l'Exploitation]**` (sans accent) est présent, mais `**[Le Chirurgien...]**` n'a pas sa variante sans accent.

4. **Fallback `[N° PV Police]`** (sans gras) présent ligne 96 mais TOKEN MAP n'a que la version avec `**`.

5. **Ordre des remplacements** : Le remplacement des tokens longs (ex: `**[L'Adresse de la Victime]**`) se fait ligne 118 avant les tokens plus courts. Mais `replace_header_block()` (ligne 117-120) fait un regex qui pourrait échouer si le format exact du bloc n'est pas respecté.

6. **Adresses personnelles des dirigeants manquantes** : `108 Cité Aimé Surre, 09000 Foix` et `7 Rue Camille Mussat, 31100 Toulouse` ne sont ni dans la TOKEN MAP ni dans la REVERSE_MAP.

---

## 4. Script `batch_anonymize.py` — Incohérences

1. **Anciens tokens sans `**`** : `batch_anonymize.py` utilise `[token]` sans double astérisque, alors que la TOKEN MAP et `generate_real_versions.py` utilisent `**[token]**`. Les fichiers récents utilisent le nouveau format `**[token]**`.

2. **Absence de token pour `Bernard TAVELLA`** — `batch_anonymize.py` ne contient aucun remplacement pour ce nom ou l'email `btavella@mairie-foix.fr`.

3. **Absence de token pour `108 Cité Aimé Surre`** et `7 Rue Camille Mussat`.

4. **`Dr DJERBI`** est tokenisé ligne 88, mais la forme exacte utilisée dans `06 Synthese` (`Dr DJERBI` sans le prénom Iskander) n'est pas listée — seulement `Dr DJERBI` avec la ligne 88 `("DJERBI", "[Le Chirurgien SOS Main]")` qui devrait attraper.

5. **Le `reverse_header_block`** dans `generate_real_versions.py` ne fonctionnera pas correctement — il cherche `**[L'Adresse de la Victime]**\n\nCourriel : **[L'Email de la Victime]**` qui est un format très spécifique pouvant ne pas correspondre à la réalité du document.

6. **`generate_real_versions.py` remplace les tokens `**[...]**`** par des valeurs réelles, mais il ignore les fichiers `INDEX.md` et `README.md` (ligne 147). Les fichiers dans `📂 Preuves officielles/01` seront traités car ils ne s'appellent ni INDEX ni README, mais `batch_anonymize.py` ne pourrait pas retokenizer les fichiers 00.

---

## 5. Recommandations

### Urgent (correction immédiate)

1. **Ne pas commit** l'état actuel — des données personnelles réelles sont en clair dans les fichiers tokenisés.

2. **Régénérer ou corriger manuellement** les 3 fichiers les plus critiques :
   - `🗂️ Organisation/22 📋 Modif Email Maire Foix.md` — Remplacer `Sébastien GRAZIDE` par `**[La Victime]**`, l'adresse par `**[L'Adresse de la Victime]**`, l'email par `**[L'Email de la Victime]**`
   - `📚 Analyses juridiques/18 Note Audit RNE NPAI SAS.md` — Tokeniser les noms complets, adresses personnelles, SIREN, dates de naissance des dirigeants
   - `✉️ Courriers/34 ✉️ EMAIL Maire Foix - Police Municipale ERP.md` — Remplacer `M. Bernard TAVELLA` par `**[L'Adjoint au Maire de la Commune]**`, les emails par `**[L'Email de l'Adjoint au Maire]**`

3. **Mettre à jour `batch_anonymize.py`** avec les nouveaux tokens manquants (TAVELLA, emails mairie, adresses dirigeants, SIREN).

4. **Compléter la TOKEN MAP** avec les 6+ tokens manquants listés section 2.

### Important (prochaine itération)

5. **Auditer les dates brutes** dans tous les fichiers tokenisés. Remplacer `29 mai 2026` par `**[J+0 Accident]**` systématiquement.

6. **Remplacer les SIREN en clair** (938 033 222) dans 5 fichiers par `**[SIREN de l'Exploitation]**`.

7. **Nettoyer `🗂️ Organisation/24 ✅ Checklist Envoi 11-07-2026.md`** — les lignes 62 et 69 contiennent `Sebastien GRAZIDE` en objet d'email.

8. **Nettoyer `🗂️ Organisation/21 📋 Plan Constat Police Foix.md`** — tokeniser le modèle d'email (adresse, nom SAS, date).

### Maintenance

9. **Uniformiser le format** `**[token]**` (avec double astérisque) entre `batch_anonymize.py`, `generate_real_versions.py` et `TOKEN MAP.md`.

10. **Supprimer les doublons** dans `REVERSE_MAP` (lignes dupliquées pour les mêmes tokens).

11. **Ajouter un test** d'intégrité qui vérifie qu'aucun fichier dans [⚖️ Actes/🔑 Token](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) ne contient de pattern PII (email, téléphone, SIREN, etc.).

---

## Annexe : Statistiques

| Métrique | Valeur |
|---|---|
| Fichiers scannés (Token/) | 35+ Markdown |
| Fichiers avec fuites | 8 (plus les README informatifs) |
| Fuites critiques (identité complète) | 3 fichiers |
| Noms propres en clair (hors tokens) | 5 personnes |
| Emails en clair | 3 distincts |
| Adresses postales en clair | 6 occurrences |
| SIREN en clair | 5 fichiers distincts |
| Tokens manquants dans TOKEN MAP | 6+ |
| Lignes dupliquées dans REVERSE_MAP | 4 blocs (8 lignes) |