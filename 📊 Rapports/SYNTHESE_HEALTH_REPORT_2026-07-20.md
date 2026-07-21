---
title: "Synthèse Rapport de Santé — 2026-07-20"
description: "Synthèse des points critiques suite à l'exécution de health_report.py"
type: rapport
date: 2026-07-20
---

# Synthèse du Rapport de Santé (20 Juillet 2026)

L'exécution du script d'audit `.dev/app/health_report.py` a relevé un total de **2 échecs critiques** et **1 avertissement**.

## 1. Fichiers orphelins (Reel vs Token)
- **Statut** : ✅ Passé

- **Détails** : Aucun fichier "Reel" n'est orphelin de son "Token" (0 occurrence). Les 150 fichiers de la strate réelle correspondent à leurs 120 dépendances déclarées.

## 2. Dossiers vides / Violations YAML
- **Statut** : 🔴 Échec

- **Détails** : Il y a **13** violations concernant le *frontmatter* YAML, principalement des fichiers sous le répertoire `📜 Lois/` (`RGPD_Articles7_9_82.md`, `code_assurances_artL113-1.md`, divers articles du `Code civil`, etc.) auxquels il manque le champ obligatoire `type`.

- Un fichier, `🧠 Memory/🗂️ Tokens/token-lrar-exploitant.md`, possède un type non canonique ('token').

## 3. Liens internes brisés
- **Statut** : 🔴 Échec

- **Détails** : Plus de **4200** liens internes sont signalés comme brisés (dont beaucoup liés à la résolution du fichier `🧠 Memory/TOKEN MAP.md` ou vers des preuves officielles).

## 4. Écarts factuels canoniques
- **Statut** : ✅ Passé (l'outil a fonctionné mais a trouvé des écarts)

- **Détails** : Le check remonte **11** écarts factuels vs `STRICT VARIABLES.md`.

  - Des erreurs de dates d'accident : '29 juin 2026' écrit au lieu de la vraie date '29 mai 2026' dans plusieurs documents (ex: Note Synthèse Avocat, Erratums, Plaintes).
  - Le numéro de LRAR réel `87001424863012T` apparaît en clair dans un fichier anonymisé `Token/✉️ Courriers/👮 Police/✉️ Police Plainte 🛟Guide 📋Orale.md` au lieu du token approprié.

## 5. Attributs manquants (calendar_event_id)
- **Statut** : ⚠️ Avertissement

- **Détails** : **56** courriers (`type=courrier`) n'ont pas d'identifiant d'événement d'agenda (`calendar_event_id`) associé, ce qui pourrait poser des problèmes de traçabilité.

## Recommandations
1. **Corriger le frontmatter** : Ajouter le champ `type` (ex: `type: loi`) aux fichiers du répertoire `📜 Lois/`.

2. **Liens internes** : Exécuter la correction via `python3 .dev/app/fix_internal_links.py` et vérifier la racine des liens cassés pour s'assurer qu'aucun chemin absolu ou erroné ne persiste.

3. **Écarts factuels** : Rectifier manuellement les dates erronées dans les Actes listés (remplacer 29 juin par 29 mai). Remplacer le numéro LRAR réel dans le fichier token par sa balise d'anonymisation.
