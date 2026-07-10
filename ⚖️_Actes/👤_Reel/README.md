# 📁 Actes / reel — Version Réelle

```
🏠 [Accueil](../../README.md) → 📁 [actes](../README.md) → 🔓 reel/
```

---

**Ce dossier contient les versions réelles de tous les actes.**  
Les tokens anonymisés (`**[La Victime]**`, `**[L'Exploitant du Commerce (La SAS)]**`) y sont résolus en identités réelles.

## ⚠️ Règle

> **Ne jamais modifier les fichiers dans `reel/` directement.**  
> Toute modification doit être faite dans `⚖️_Actes/🔑_Token/`, puis regénérée via :
> ```bash
> python3 app/generate_real_versions.py
> ```

## 📂 Contenu

| Dossier | Fichiers | Description |
|---------|----------|-------------|
| **[01_⚖️_Actes_proceduraux](01_⚖️_Actes_proceduraux/README.md)** | 6 | Assignations, conclusions, requêtes (versions réelles) |
| **[02_✉️_Courriers](02_✉️_Courriers/README.md)** | 20 | Courriers et signalements (versions réelles) |
| **[03_📚_Analyses_juridiques](03_📚_Analyses_juridiques/README.md)** | 4 | Plaidoiries, FAQ (versions réelles) |
| **[04_💰_Etudes_indemnisation](04_💰_Etudes_indemnisation/README.md)** | 1 | Étude d'indemnisation (version réelle) |
| **[05_🗂️_Organisation](05_🗂️_Organisation/README.md)** | 3 | Index, plan, calendrier (versions réelles) |
| **[06_🗄️_Archives](06_🗄️_Archives/README.md)** | 7 | Archives (versions réelles) |

## 🔗 Source

Tous ces fichiers sont générés depuis :
> `⚖️_Actes/🔑_Token/` → `python3 app/generate_real_versions.py` → `⚖️_Actes/👤_Reel/`
