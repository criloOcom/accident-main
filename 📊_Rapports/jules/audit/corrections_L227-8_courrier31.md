<!-- [🏠](../README.md) > 📁 [ 📊_Rapports ](....../README.md) > 📁 [ jules ](..../README.md) > 📁 [ audit ](../README.md) > 📄 [ corrections_L227-8_courrier31.md ](.corrections_L227-8_courrier31.md) -->
---
title: "Rapport de correction — L.227-8 et Courrier 31"
description: "Date : 2026-07-10"
type: rapport
---

# Rapport de correction — L.227-8 et Courrier 31

Date : 2026-07-10

## Corrections effectuées

### L.227-8 Code de commerce — 3 fichiers corrigés

**Problème** : L'article L.227-8 était cité avec des textes qui ne correspondent pas à son contenu réel.

**Vrai texte de L.227-8 C.com (LEGIARTI000006227036, VIGUEUR) :**
> « Les règles fixant la responsabilité des membres du conseil d'administration et du directoire des sociétés anonymes sont applicables au président et aux dirigeants de la société par actions simplifiée. »

C'est un article de **renvoi** : il ne définit pas la responsabilité lui-même mais rend applicables aux SAS les règles de responsabilité des SA.

| Fichier | Ancien texte erroné | Article confondu |
|---------|-------------------|------------------|
| `03 ✉️ Courrier SAS.md` | L.227-8 cité avec le texte de L.225-251 | L.225-251 (responsabilité des administrateurs/DG) |
| `06 ✉️ Courrier President DG.md` | L.227-8 cité avec le texte de L.225-254 | L.225-254 (prescription triennale) |
| `02b 🛡️ Constitution Partie Civile.md` | L.227-8 cité avec le texte de L.225-254 | L.225-254 (prescription triennale) |

**Correction dans les 3 fichiers** :
- Texte de la citation remplacé par le vrai texte de L.227-8
- Chemin de rubrique Légifrance corrigé (Livre II, Titre II, Chapitre VII)
- Introduction harmonisée

### Courrier 31 — 2 articles corrigés

**Problème** : Les articles L.123-5-1 et R.123-143 étaient cités avec des textes inventés/hallucinés ne correspondant à aucun article existant.

| Section | Ancienne citation | Article réel |
|---------|------------------|--------------|
| A. L.123-5-1 | « Le ministère public peut, dans un délai de deux mois... former opposition... » (TEXTE FABRIQUÉ) | **L.123-5-1 C.com** : président du tribunal en référé peut enjoindre sous astreinte |
| B. R.123-143 | « Tout déposant au greffe peut... former opposition... » (TEXTE FABRIQUÉ) | **L.123-3 C.com** : juge commis, à la requête de tout intéressé, peut ordonner radiation |

**Correction** :
- Section A : texte réel de L.123-5-1 (pouvoir du président du tribunal en référé) + adaptation de l'argumentaire
- Section B : remplacement par L.123-3 (droit de toute personne justifiant d'un intérêt légitime de saisir le juge commis)

## Vérification Légifrance

Tous les textes ont été vérifiés via l'API OpenLegi (Légifrance) le 10/07/2026 :
- L.227-8 : LEGIARTI000006227036 ✅ (VIGUEUR)
- L.225-251 : LEGIARTI000006226329 ✅ (VIGUEUR)
- L.225-254 : LEGIARTI000006226359 ✅ (VIGUEUR)
- L.123-5-1 : LEGIARTI000006219291 ✅ (VIGUEUR)
- L.123-3 : LEGIARTI000025559422 ✅ (VIGUEUR)

## Fichiers modifiés

1. `⚖️_Actes/🔑_Token/02_✉️_Courriers/03 ✉️ Courrier SAS.md` — L.227-8 texte corrigé
2. `⚖️_Actes/🔑_Token/02_✉️_Courriers/06 ✉️ Courrier President DG.md` — L.227-8 texte corrigé
3. `⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/02b 🛡️ Constitution Partie Civile.md` — L.227-8 texte corrigé
4. `⚖️_Actes/🔑_Token/02_✉️_Courriers/31 ✉️ Courrier INPI Opposition.md` — L.123-5-1 et R.123-143 remplacés par textes réels
