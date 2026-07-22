---
title: "PHASE 45 — A8 — Rapport Consolidé"
description: "Liste exhaustive des erreurs détectées par Phase 45, classées par priorité, avant correction"
type: rapport
date: 2026-07-22
---

# PHASE 45 — A8<br>Rapport Consolidé des Anomalies

> **Source** : Rapports A1-A7 (détection + cross-validation)
> **Date** : 22 juillet 2026
> **Périmètre** : `Actes/Token/` sauf `Preuves_officielles/`

---

## P0 — FUITES PII (🔴 12 fichiers)

| # | Fichier | Ligne(s) | PII | Correctif |
|---|---------|-----------|-----|-----------|
| 1 | `Courriers/Police/Police - Plainte Complémentaire.md` | 172,174,176,178,180 | LRAR réels `87500152771696F`, etc. | Remplacer par `[**[N° LRAR HB BARBER Société]**]` etc. |
| 2 | `Courriers/Police/Police - Plainte Complémentaire.md` | 184,186,188,298 | `M. Frédéric MATHIEU` | Remplacer par `[**[Le Témoin Mathieu]**]` |
| 3 | `Courriers/Police/Police - Plainte Complémentaire.md` | 296 | `+33 7 58 40 12 87` réel | Remplacer par `[**[Téléphone du Témoin Mathieu]**]` |
| 4 | `Courriers/Police/Police - Note Personnelle.md` | 53 | `Jordy RODRIGUEZ CAPARROS` | Remplacer par token |
| 5 | `Courriers/Police/Police - Note Personnelle.md` | 86,92,109 | 3 RPPS réels (identifiants médicaux) | Remplacer par tokens |
| 6 | `Courriers/Police/Police - Note Personnelle.md` | 109 | `Dr Yogan OXYBEL` | Remplacer par `[**[Le Chirurgien SOS Main]**]` |
| 7 | `Courriers/Police/Police - Note Personnelle.md` | 296,343 | `+33 7 58 40 12 87` | Remplacer par token téléphone |
| 8 | `Courriers/Police/Police - Note Erratum Identité.md` | 78,125 | `Sabir MOUNTASSER` | Remplacer par token |
| 9 | `Courriers/Police/Police - Note Erratum Identité.md` | 80,127 | `Catherine ANDISSAC` | Remplacer par token |
| 10 | `Courriers/Police/Police - Note Erratum Identité.md` | 158 | `Hamza El Hachemi BERGUIGA` | Remplacer par token |
| 11 | `Courriers/Police/Police - Note Erratum Identité.md` | 160 | `Catherine SORROCHE` | Remplacer par token |
| 12 | `Courriers/Police/Police - Bordereau Pièces.md` | 84 | `Mme MAGALHAES` | Remplacer par token |
| 13 | `Courriers/Police/Police - Note Personnelle.md` | 122 | `Mme MAGALHAES` | Remplacer par token |
| 14 | `Courriers/Propriétaire/Propriétaire - Courrier - Relance 3.md` | 4 (YAML) | `Romain DELRIEU` | Remplacer par token |
| 15 | `Courriers/Propriétaire/Propriétaire - Courrier - Relance 3.md` | 124,126,136 | SIREN `104103262` / `938033222` | Remplacer par `[**[SIREN de l'Exploitation]**]` etc. |
| 16 | `Courriers/Propriétaire/Propriétaire - Courrier - Relance 3.md` | 161 | CPAM `31727387` | Remplacer par token |
| 17 | `Courriers/Médical/CHIVA - Dossier Médical - Demande.md` | 82 | `Dr Jardon` | Remplacer par token |
| 18 | `Courriers/SAS_&_Salon/SAS HB BARBER - Président - Courrier.md` | 23 | `BERGUIGA` dans URL Drive | Remplacer par token |
| 19 | `Organisation/Fiche Synthétique - HB BARBER.md` | 41 | `BERGUIGA Hamza El Hachemi` | Remplacer par token |
| 20 | `Organisation/Fiche Synthétique - HB BARBER.md` | 47,57 | `SORROCHE Catherine` | Remplacer par token |
| 21 | `Organisation/34 EMAIL Maire Foix - Police Municipale ERP.md` | 13-14 | Emails réels (`btavella@...`, `secretariat@...`) | Remplacer par tokens |
| 22 | `Organisation/34 EMAIL Maire Foix - Police Municipale ERP.md` | 7 | `M. Bernard TAVELLA` | Remplacer par token |
| 23 | `Attestations/Attestation - Témoin Mathieu Frédéric.md` | (nom fichier) | `Mathieu Frédéric` dans le nom | Renommer le fichier |
| 24 | `Organisation/Checklist - Déplacement 20-07.md` | 112-121 | Téléphones TJ Foix, Commissariat, etc. | À évaluer (numéros publics) |
| 25 | `Organisation/Note - Kit Foix 27-07-2026.md` | 103-107 | Téléphones TJ Foix, Commissariat | À évaluer (numéros publics) |

---

## P1 — STRUCTURE (🔴 70+ fichiers)

### P1a — Doublons `<hr><hr>` back-to-back (~70 fichiers)
Tous les fichiers listés par A2. Solution : supprimer la première occurrence de chaque paire.

### P1b — Sections `##` sans `<hr><hr>` avant (15 fichiers)
- `Actes_proceduraux/Contentieux_civil/` : 7 fichiers (Constat Huissier, TC Foix, Bordereau, CPC 145, Conclusions Fond, Référé Provision Assignation, Référé Provision Conclusions)

- `Actes_proceduraux/Contentieux_penal/` : 6 fichiers (Réquisitoire, PC Constitution, Plainte Défaut, PV Audition Foix, PV Audition, Signalement Fraude)

- `Analyses_juridiques/README.md`

### P1c — Double H1 (2 fichiers)
- `Police - Plainte Complémentaire.md` (l.49-50)

- `Police - Note Guide Plainte Orale.md` (l.34,38,39)

### P1d — `---` dans le corps (4 fichiers)
- `Archives/annexes/README.md`, `Attestations/README.md`, `Preuves_officielles/20270529_Rapport_Expertise_Médicale.md`, `Preuves_officielles/Preparation_Expertise_UMJ.md`

---

## P2 — LIENS + JURITEXT (🟠 3+ fichiers)

| # | Fichier | Problème |
|---|---------|----------|
| 1 | `TJ Foix - Référé Provision - Assignation.md` | `JURITEXT000006927230` invalide (l.111,384) |
| 2 | `TJ Foix - Référé Provision - Assignation.md` | `JURITEXT000026156720` décrit comme "2e Civ, 18 sept 2003" mais renvoie à "1re Civ, 4 juil 2012" (divorce) — mauvais arrêt |
| 3 | `TJ Foix - Référé Provision - Assignation.md` | `JURITEXT000007044005` décrit comme "Costedoat, Ass. Plén., 25 fév 2000" mais renvoie à "Ch. com., 26 mai 1999" (capital social) — mauvais arrêt |
| 4 | `Note - Dossier Plaidoirie Référé.md` | Lien tronqué `[**[J+1 Chirurgie]**](../../../Memory/Tokens/token-j-1-chirurgie.md` (manque `)`) |
| 5 | Citations non liées | ~5 538 dans 79 fichiers (non-bloquant, `linkify_citations.py --apply`) |

---

## P3 — README (🟡 23 entrées + 18 tokens)

| Catégorie | Nombre | Détail |
|-----------|--------|--------|
| Fantômes (liés à renommage) | 23 | Archives (4), Attestations (6), Témoins (2), Rapports (11) |
| Fichiers non listés | 18 | Tokens LRAR dans `Memory/Tokens/README.md` |
| Résidu `[À FAIRE]` | 1 | `Rapports/90_TODO_Prompts/README.md` l.7 |

---

## Bilan

| Priorité | Nb fichiers | Statut |
|----------|-------------|--------|
| **P0 PII** | 12 fichiers, ~25 occurrences | 🔴 À CORRIGER |
| **P1 Structure** | 70+ fichiers | 🔴 À CORRIGER (scripts auto) |
| **P2 Liens** | 3 fichiers, 3 JURITEXT | 🟠 À CORRIGER |
| **P3 README** | 23+18 entrées | 🟡 À CORRIGER |
