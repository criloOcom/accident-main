---
title: "🛠️ Environnement de Développement"
description: "Ce dossier contient le code, les scripts et les outils de développement du projet."
type: readme
---
<!-- Breadcrumb -->
*[🏠](../README.md) › .dev*
<hr>
<!-- /Breadcrumb -->

# 🛠️ Environnement de Développement

Ce dossier contient le code, les scripts et les outils de développement du projet.

## 📁 Structure

### app/
- Scripts Python et outils automatisés

- Organisés par fonctionnalité

### artifacts/
- Artefacts générés par les scripts

- Résultats intermédiaires

### data/
- Données de référence et jeux de test

### deployment/
- Configuration de déploiement

- Scripts CI/CD

### tests/
- Tests unitaires et d'intégration

- Couverture de test

### .venv/
- Environnement virtuel Python

- Dépendances du projet

## 🚀 Utilisation

### Exécution des scripts
```bash
# Exemple : Exécuter un script Python
python3 .dev/app/script.py

# Avec environnement virtuel
source .dev/.venv/bin/activate
python3 script.py
```