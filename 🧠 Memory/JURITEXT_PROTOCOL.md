---
title: "PROTOCOLE JURITEXT — Vérification obligatoire des identifiants de jurisprudence"
description: "Quand tu dois insérer ou vérifier une JURITEXT :"
type: memory
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › JURITEXT PROTOCOL*
<hr>
<!-- /Breadcrumb -->

# PROTOCOLE JURITEXT<br>Vérification obligatoire des identifiants de jurisprudence

> **Règle absolue** : tout agent qui insère, modifie ou vérifie une JURITEXT
> DOIT suivre ce protocole. Pas d'exception.

---

## RÈGLES OBLIGATOires

### RÈGLE 1 — Vérification en 2 étapes (SANS EXCEPTION)

Quand tu dois insérer ou vérifier une JURITEXT :

**Étape 1** : Rechercher l'arrêt par son numéro d'affaire via le MCP Légifrance :
```
legifrance-prod_rechercher_jurisprudence(query="NUMERO-AFFAIRE", page_size=1)
```
→ L'API retourne le `JURITEXT0000XXXXXXXX` dans `results[0].titles[0].id`

**Étape 2** : Confirmer que le JURITEXT trouvé correspond bien au bon arrêt :
```
openlegi_rechercher_jurisprudence_judiciaire(search="NUMERO-AFFAIRE", page_size=1)
```
→ Vérifier que le `identifiant` retourné est le même

**Si les 2 outils retournent le même ID** → l'ID est validé ✅

**Si les 2 outils sont en timeout** → relancer UNE fois, puis signaler à l'utilisateur
**Si les 2 outils retournent des IDs différents** → ne PAS choisir, demander à l'utilisateur

### RÈGLE 2 — JAMAIS deviner un JURITEXT

**INTERDIT** de :
- Prendre un JURITEXT qui "semble correct" parce qu'il est déjà dans le codebase

- Remplacer un JURITEXT invalide par un autre sans le vérifier

- Se fier à une coche "✓" dans un fichier — la coche ne prouve rien

- Utiliser Judilibre comme seule source — si 0 résultat, passer à Légifrance-prod

**Si un JURITEXT est introuvable** :
1. Noter "JURITEXT INTRUOUVABLE" dans le fichier

2. Mettre le numéro d'affaire en attendant

3. Signaler à l'utilisateur

4. NE PAS deviner

### RÈGLE 3 — Audit de tous les JURITEXT existants

Avant tout commit ou finalisation d'un document contenant des JURITEXT :
1. Extraire toutes les JURITEXT uniques du fichier (`grep -oh 'JURITEXT[0-9]\+'`)

2. Vérifier CHAQUE JURITEXT via `legifrance-prod_rechercher_jurisprudence`

3. Si un ID est introuvable → marquer comme "À VÉRIFIER" et signaler

### RÈGLE 4 — Chaîne de propagation des erreurs

Si tu découvres une JURITEXT fausse :
1. **CORRIGER** le fichier source immédiatement

2. **CHERCHER** les autres occurrences dans tout le projet (`grep -r`)

3. **CORRIGER** toutes les occurrences

4. **VÉRIFIER** que la nouvelle JURITEXT est bien correcte via les 2 outils

5. **NOTER** l'erreur dans STATUS.md avec la correction appliquée

---

## OUTILS DE VÉRIFICATION

| Outil | Commande | Usage |
|-------|----------|-------|
| **Légifrance-prod** | `legifrance-prod_rechercher_jurisprudence(query="NUMERO", page_size=1)` | Recherche par numéro d'affaire → retourne JURITEXT |
| **OpenLegi** | `openlegi_rechercher_jurisprudence_judiciaire(search="NUMERO", page_size=1)` | Vérification croisée → retourne `identifiant` |
| **Judilibre** | `judilibre_rechercher_jurisprudence(query="NUMERO", page_size=1)` | Recherche secondaire (moins fiable, peut retourner 0) |

**Priorité** : Légifrance-prod > OpenLegi > Judilibre

---

## ANTI-PATTERNS (ce qu'il ne faut JAMAIS faire)

❌ "Judilibre retourne 0 résultat, donc JURITEXT0000XXX est probablement correct"
→ FAUX. 0 résultat signifie que l'ID n'existe pas dans Judilibre, pas qu'il est correct.

❌ "Je vois JURITEXT0000XXX dans un autre fichier avec une coche ✓, donc c'est bon"
→ FAUX. La coche ne prouve rien — elle peut être erronée depuis le début.

❌ "Le JURITEXT précédent était faux, je vais essayer celui-ci"
→ FAUX. Ne JAMAIS remplacer un faux par un autre sans vérification.

❌ "L'API timeout, donc l'ID est probablement valide"
→ FAUX. Timeout = problème réseau, pas validation.

---

## EXEMPLE CORRECT

```
Besoin : insérer la JURITEXT pour l'arrêt n° 13-80.849

1. legifrance-prod_rechercher_jurisprudence(query="13-80.849", page_size=1)
   → results[0].titles[0].id = JURITEXT000029014493 ✅

2. openlegi_rechercher_jurisprudence_judiciaire(search="13-80.849", page_size=1)
   → identifiant = JURITEXT000029014493 ✅

3. Les 2 outils concordent → JURITEXT000029014493 est validé

4. Insérer : [Arrêt n°13-80.849](https://www.legifrance.gouv.fr/juri/id/JURITEXT000029014493)
```

---