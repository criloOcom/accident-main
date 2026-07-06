# 📁 Actes / reel — Version Réelle

```
🏠 [Accueil](../../README.md) → 📁 [actes](../README.md) → 🔓 reel/
```

---

**Ce dossier contient les versions réelles de tous les actes.**  
Les tokens anonymisés (`**[La Victime]**`, `**[L'Exploitant du Commerce]**`) y sont résolus en identités réelles.

## ⚠️ Règle

> **Ne jamais modifier les fichiers dans `reel/` directement.**  
> Toute modification doit être faite dans `actes/token/`, puis regénérée via :
> ```bash
> python3 app/generate_real_versions.py
> ```

## 📂 Contenu

| Dossier | Fichiers | Description |
|---------|----------|-------------|
| **[01_Actes_proceduraux](01_Actes_proceduraux/README.md)** | 6 | Assignations, conclusions, requêtes (versions réelles) |
| **[02_Courriers](02_Courriers/README.md)** | 20 | Courriers et signalements (versions réelles) |
| **[03_Analyses_juridiques](03_Analyses_juridiques/README.md)** | 4 | Plaidoiries, FAQ (versions réelles) |
| **[04_Etudes_indemnisation](04_Etudes_indemnisation/README.md)** | 1 | Étude d'indemnisation (version réelle) |
| **[05_Organisation](05_Organisation/README.md)** | 3 | Index, plan, calendrier (versions réelles) |
| **[06_Archives](06_Archives/README.md)** | 7 | Archives (versions réelles) |

## 🔗 Source

Tous ces fichiers sont générés depuis :
> `actes/token/` → `python3 app/generate_real_versions.py` → `actes/reel/`
