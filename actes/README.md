# 📁 Actes — Dossier Contentieux

```
🏠 [Accueil](../README.md) → 📁 actes/
```

---

Bienvenue dans le dossier central du contentieux. Ce dossier repose sur une **double strate** : des versions anonymisées pour le travail courant, et des versions réelles pour l'impression et l'envoi.

## 🗂️ Structure

| Dossier | Contenu |
|---------|---------|
| **[`token/`](token/README.md)** | **Versions tokenisées** — Identités remplacées par `**[La Victime]**`, etc. C'est la strate de travail. |
| **[`reel/`](reel/README.md)** | **Versions réelles** — Tokens résolus (noms, adresses, email réels). Version imprimable et envoyable. |

## 🔄 Workflow

1. On travaille exclusivement dans `token/` (création, modification, révision)
2. On génère `reel/` via `python3 app/generate_real_versions.py`
3. On imprime/envoie depuis `reel/`

## 📋 Sous-dossiers token/ (miroir identique dans reel/)

| N° | Dossier | Description |
|----|---------|-------------|
| `00` | **[Preuves officielles](token/00_Preuves_officielles/README.md)** | Documents physiques, CR opératoire, PV police |
| `01` | **[Actes procéduraux](token/01_Actes_proceduraux/README.md)** | Assignations, conclusions, requêtes |
| `02` | **[Courriers](token/02_Courriers/README.md)** | Mises en demeure, signalements, relances |
| `03` | **[Analyses juridiques](token/03_Analyses_juridiques/README.md)** | Plaidoiries, FAQ, mémorandums |
| `04` | **[Études d'indemnisation](token/04_Etudes_indemnisation/README.md)** | Évaluation Dintilhac (59 600 €) |
| `05` | **[Organisation](token/05_Organisation/README.md)** | Index, plan d'action, calendrier |
| `06` | **[Archives](token/06_Archives/README.md)** | Anciens documents de travail, annexes |
