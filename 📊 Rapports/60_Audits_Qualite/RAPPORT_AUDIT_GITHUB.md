---
title: "RAPPORT D'AUDIT — Repository GitHub"
description: "Projet** : accident-main · **Remote** : `github.com/criloOcom/accident-main.git`"
type: rapport
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports et Analyses](./README.md) › RAPPORT AUDIT GITHUB*
<hr>
<!-- /Breadcrumb -->

# RAPPORT D'AUDIT<br>Repository GitHub

**Projet** : accident-main · **Remote** : `github.com/criloOcom/accident-main.git`
**Date** : 10 juillet 2026 · **Auditeur** : Agent opencode

---

## I — Résumé exécutif

| Domaine | Statut | Sévérité |
|---------|--------|----------|
| 🔴 Fuite token GitHub dans `.git/config` | **CRITIQUE** | 🔴🔴🔴 |
| 🔴 Token dans `~/.git-credentials` (visible tout process) | **CRITIQUE** | 🔴🔴🔴 |
| 🟡 Pollution branches (80+ locales, 100+ distantes) | **ÉLEVÉ** | 🟡🟡 |
| 🟡 Répertoires rapports dupliqués (`reports/` + [📊 Rapports](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md)) | **MOYEN** | 🟡 |
| 🟢 README.md à jour | **BON** | ✅ |
| 🟢 pre-commit hook actif | **BON** | ✅ |
| 🟢 .gitignore complet | **BON** | ✅ |
| 🟢 Workflow Git structuré (emojis, conventions) | **BON** | ✅ |

---

## II — Derniers commits

```
eda02b9 📋 Fichiers suivi LRAR (23) + checklist envoi 11/07 (24)
485909b 📬 Mise à jour courriers 12, 14, 19, 35 (adresses PJ délai)
10c4554 Correction ton courrier 34
bd00859 docs(audit): unify tribunal locations + add audit report
6156fc3 🧹 Audit et correction dates courriers 09-34
141f5c3 🧹 Amélioration rédactionnelle email 34 Maire de Foix
aae77c7 🧹 [RGPD Audit] Rapport tokenisation résiduelle
640ed28 Corrections juridiques : L.227-8 + courrier 31
f5a2e64 Adoucir le ton paragraphe CADA dans Email 34
11b1508 Ajout paragraphe droit d'accès CADA + tokenisation PV n°
```

**Statut : ✅ Bon**
- Messages clairs, émojis thématiques, référence aux numéros de courrier.
- Premier commit : `f4637bf` (04/07/2026) — repo jeune (~6 jours).
- 442 commits au total (actif : ~70 commits/jour).

---

## III — .gitignore

**Fichier** : `.gitignore` (créé dès le commit initial)

```
__pycache__/
*.pyc
.env
.dev/.env
.venv/
.dev/.venv/
node_modules/
*.pdf
!lois/pdfs/*.pdf
/tmp/
.drive-token.json
.piste-credentials.json
venv/
```

**Statut : 🟡 Satisfaisant mais incomplet**
- ✅ `.env` / `.venv` / `__pycache__` exclus
- ✅ Fichiers token Drive/Piste exclus
- ✅ PDFs exclus sauf [📜 Lois/pdfs](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) (jurisprudence)
- ⚠️ `.git-credentials` non listé (ne peut pas être ignoré par `.gitignore`)
- ⚠️ `.git/config` non protégeable via `.gitignore` — le token y est stocké en clair
- ⚠️ `.dev/artifacts/` et `.dev/data/scratch/` non exclus (fichiers volumineux)

---

## IV — Pre-commit hook

**Fichier** : `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Hook pre-commit<br>vérifie l'intégrité des README.md avant chaque commit
echo "🔍 [AUDIT] Vérification automatique des README.md..."
SCRIPT=".dev/app/audit_readme_integrity.py"
...
```

**Statut : ✅ Actif mais limité**
- ✅ Hook personnalisé actif (pas le `.sample`)
- ✅ Vérifie l'intégrité des README.md via `.dev/app/audit_readme_integrity.py`
- ✅ Codes retour : 1 = bloquant, 2 = warning avec confirmation manuelle
- ❌ Ne vérifie **pas** la présence de secrets/tokens dans les fichiers
- ❌ Ne vérifie **pas** la taille des fichiers ou des diffs
- ❌ Ne vérifie **pas** les branches orphelines/stale

---

## V — 🔴 Fichiers sensibles dans l'historique

### V.1 — 🔴 CRITIQUE : Token GitHub exposé

**Emplacement** : `.git/config` (remote origin URL)
```ini
url = https://criloOcom:[REVOKED_TOKEN]@github.com/...
```

**Emplacement** : `~/.git-credentials`
```
https://criloOcom:[REVOKED_TOKEN]@github.com
```

**Risques** :
- Tout processus sur la machine peut lire `~/.git-credentials`
- `git remote -v` affiche le token en clair
- Tout commit push expose le token dans le trafic (même si GitHub masque dans les logs)
- Le token était un `ghp_` (classic) — permissions étendues

**Recommandation immédiate** :
1. **Révoquer immédiatement** ce token sur GitHub
2. Remplacer par un token **fine-grained** avec scope limité (`repo` uniquement, pas d'admin)
3. Utiliser `credential.helper` avec stockage sécurisé :
   ```bash
   git remote set-url origin https://github.com/criloOcom/accident-main.git
   git config credential.helper "store --file ~/.git-credentials-secure"
   ```
   Ou mieux : utiliser un **GitHub CLI** (`gh auth login`) qui gère l'auth via OAuth device flow
4. Chiffrer `~/.git-credentials` ou utiliser un gestionnaire de secrets système

### V.2 — Autres fichiers suivis

- `.dev/.env.example` — **OK** (template, pas de secrets réels)
- `reports/audit/audit_tokenisation_residuelle.md` — **OK** (rapport RGPD, pas de secrets)
- Aucun fichier `.env` réel ni fichier de credentials dans l'historique Git

---

## VI — Taille du repository

| Métrique | Valeur |
|----------|--------|
| Taille totale (working tree) | **~1011 MB** |
| Taille `.git/` | **28 MB** |
| Taille `.git/objects/pack/` | **1.4 MB** |
| Objets total | 4 222 (1063 packés, 318 prune-packable) |
| Nombre de références | **255 fichiers** dans `.git/refs/` |
| Nombre de commits | **442** |
| Plus gros fichiers en historique | `uv.lock` (545 KB), `results_*.json/html` (jusqu'à 443 KB), PDFs jurisprudence (jusqu'à 218 KB) |

**Analyse** :
- Le poids vient surtout des **PDFs** dans [📜 Lois/pdfs](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) (117 Mo estimés)
- `.dev/artifacts/` contient des artefacts de test volumineux (json + html)
- 318 objets `prune-packable` indiquent des réécritures d'historique partielles
- **Propre** : pas de blobs géants (> 1 Mo) dans l'historique

---

## VII — README.md

**Fichier** : `README.md` (164 lignes)

**Statut : ✅ Excellent**
- ✅ Porte d'entrée complète avec statuts des courriers à jour
- ✅ Tableau d'échéances impératives (envoi n°34 aujourd'hui)
- ✅ Arborescence documentée
- ✅ Tableau des courriers avec statuts réels (envoyés/prêts/projets/gabarits)
- ✅ Liens vers [🧠 Memory](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) (VACCIN, STATUS, RULES, etc.)
- ✅ Workflow quotidien documenté (8 étapes)
- ✅ Scripts listés avec rôles
- ✅ Remote GitHub et token référencé (Secret Manager)

**⚠️ Anomalie mineure** : Le README référence `📦_pieces/` mais ce dossier n'existe pas dans `ls` (peut-être non versionné ou supprimé).

---

## VIII — Problèmes et recommandations

### VIII.1 — 🔴 CRITIQUE — Fuite de token GitHub

| Problème | Impact | Remédiation |
|----------|--------|-------------|
| Token `ghp_[...]` (classic) en clair dans `.git/config` | Exposé à tout `git remote -v` | Révoquer + remplacer par fine-grained + credential helper |
| Token dupliqué dans `~/.git-credentials` | Visible tout processus système | Supprimer ou chiffrer le fichier |

### VIII.2 — 🟡 ÉLEVÉ — Pollution de branches

| Problème | Impact | Remédiation |
|----------|--------|-------------|
| 80+ branches locales (jules/M*, feat/*, audit-*) | Désordre, risque de confusion | Nettoyer : `git branch -d` pour les mergées |
| 100+ branches distantes orphelines | Encombrement remote, PRs mortes | Nettoyer : `git push origin --delete` |
| Stash orphelin `jules/M06-...` | Perte de contexte | Review + apply ou drop |

### VIII.3 — 🟡 MOYEN — Duplication de répertoires

| Problème | Impact | Remédiation |
|----------|--------|-------------|
| `reports/` ET [📊 Rapports](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) | Ambiguïté, fragmentation | Fusionner dans [📊 Rapports](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) ou décider d'un seul standard |

### VIII.4 — 🟢 AMÉLIORATIONS SOUHAITABLES

| Domaine | Recommandation |
|---------|---------------|
| pre-commit hook | Ajouter une vérification `detect-secrets` ou `trufflehog` pour bloquer les tokens |
| .gitignore | Ajouter `.dev/artifacts/`, `.dev/data/scratch/`, `.git-credentials` (documentation) |
| Cleanup | `git gc --aggressive --prune=now` après le nettoyage des branches |
| Workflow | Imposer `git push --force-with-lease` plutôt que `--force` pour les réécritures |
| Prévention fuite | Ajouter une GitHub Action `.github/workflows/secret-scan.yml` avec `trufflehog` ou `ggshield` |

---

## IX — Conclusion

Le repository est **bien structuré**, avec une convention de commits claire, un README excellent, et un hook pre-commit actif. La menace principale est la **fuite du token GitHub** en clair dans la configuration Git — une action immédiate est requise. La pollution de branches (héritage des sessions Jules) et la duplication de dossiers rapports sont des problèmes de maintenance à traiter en priorité secondaire.