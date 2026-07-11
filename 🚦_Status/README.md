---
title: "🚦 Status — Index des documents par statut"
description: "Ce dossier regroupe tous les documents du dossier **Accident Main** classés par statut de délivrance."
type: readme
---


<!-- Breadcrumb -->
[🏠](../README.md) › 🚦 Status
<!-- /Breadcrumb -->

# 🚦 Status — Index des documents par statut

Ce dossier regroupe tous les documents du dossier **Accident Main** classés par statut de délivrance.

## Index

| Fichier | Statut | Description |
|---------|--------|-------------|
| [01_PREPARATION.md](01_PREPARATION.md) | 📋 Préparation | Documents en cours (brouillon, projet, fusionné) |
| [02_PRET_POUR_ENVOI.md](02_PRET_POUR_ENVOI.md) | 📤 Prêt pour envoi | Documents finalisés sans preuve d'envoi |
| [03_ENVOYE.md](03_ENVOYE.md) | ✅ Envoyé | Documents avec preuve de délivrance (LRAR/AR/dépôt) |

## Convention des statuts YAML

| `statut` | Signification | Index |
|----------|---------------|-------|
| `brouillon` | En cours de rédaction | 01_PREPARATION |
| `projet` | En attente de relecture | 01_PREPARATION |
| `fusionné_dans_01` | Fusionné avec un autre document | 01_PREPARATION |
| `preparation` | En préparation (checklist, planning) | 02_PRET_POUR_ENVOI |
| `final` | Finalisé — preuve d'envoi absente | 02_PRET_POUR_ENVOI |
| `envoye` | Envoyé avec preuve matérielle | 03_ENVOYE |

## Champs YAML obligatoires

```yaml
statut: final                # Valeur de la convention ci-dessus
reel_path: ../../👤_Reel/... # Dans 🔑_Token → lien vers 👤_Reel
token_path: ../../🔑_Token/... # Dans 👤_Reel → lien vers 🔑_Token
proof_delivery: "LRAR N°..."  # Preuve matérielle (null si non envoyé)
```

> Mis à jour automatiquement par `.dev/app/update_status_system.py` (cross-refs) et `.dev/app/update_proof_delivery.py` (statuts envoyés).