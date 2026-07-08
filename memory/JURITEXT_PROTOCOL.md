# PROTOCOLE JURITEXT — Vérification obligatoire des identifiants de jurisprudence

> **Origine** : erreurs récurrentes de JURITEXT fausses dans les actes, malgré
> l'accès aux outils MCP. Cette erreur est **inexcusable** quand les outils
> existent — elle provient de raccourcis et de l'absence de vérification
> systématique.
>
> **Règle absolue** : tout agent qui insère, modifie ou vérifie une JURITEXT
> DOIT suivre ce protocole. Pas d'exception.

---

## LE PROBLÈME

Des JURITEXT fausses ont été introduites dans les actes à plusieurs reprises :
1. **JURITEXT000007152625** — ID inexistant (erreur 400 API), utilisé comme source d'une citation fabriquée (hallucination SATI)
2. **JURITEXT000043514489** — mauvais ID pour l'arrêt 20-16.463 (le bon est JURITEXT000044482848)
3. **JURITEXT000028994017** — mauvais ID pour l'arrêt 13-80.849 (le bon est JURITEXT000029014493), introduit en voulant "corriger" un autre mauvais ID
4. **JURITEXT000050460532** — mauvais ID pour 22-19.307 (le bon est JURITEXT000049418278)

**Pattern commun** : l'agent a trouvé 0 résultat sur un outil, puis a **deviné** un remplaçant au lieu d'utiliser l'outil suivant disponible.

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

## HISTORIQUE DES ERREURS (pour mémoire)

| Date | JURITEXT fausse | Bonne JURITEXT | Arrêt | Cause |
|------|----------------|----------------|-------|-------|
| 2026-07-08 | JURITEXT000007152625 | JURITEXT000007047369 | 99-17.092 SATI | Citation inventée, ID inexistant |
| 2026-07-08 | JURITEXT000043514489 | JURITEXT000044482848 | 20-16.463 | Mauvais ID |
| 2026-07-08 | JURITEXT000028994017 | JURITEXT000029014493 | 13-80.849 | ID deviné en voulant corriger un autre faux |
| 2026-07-08 | JURITEXT000050460532 | JURITEXT000049418278 | 22-19.307 | Mauvais ID |
| 2026-07-08 | JURITEXT000006485532 | JURITEXT000007047223 | 02-14.783 | Mauvais ID |
| 2026-07-08 | JURITEXT000007043322 | JURITEXT000007071351 | 00-82.066 Cousin | Mauvais ID |
| 2026-07-08 | JURITEXT000007043831 | JURITEXT000007043704 | 97-17.378 Costedoat | Mauvais ID |
| 2026-07-08 | JURITEXT000033127860 (fabriquée) | JURITEXT000039122827 | 18-13.791 | L'agent a remplacé un JURITEXT correct par un ID fabriqué, sans vérifier le contexte de la ligne |
| 2026-07-08 | JURITEXT000044515079 | JURITEXT000044105739 | 20-17.263 | Mauvais ID + erreur de date (13/01/2022 → 09/09/2021) |
| 2026-07-08 | JURITEXT000021271787 | À VÉRIFIER | 08-15.103 | Numéro d'affaire introuvable dans Légifrance — citation potentiellement fabriquée |
| 2026-07-08 | JURITEXT000036835776 | JURITEXT000036780068 | 17-14.499 | Mauvais ID |
| 2026-07-08 | JURITEXT000049914357 | JURITEXT000049857400 | 23-15.345 | Mauvais ID |
| 2026-07-08 | JURITEXT000045683755 | JURITEXT000045822770 | 21-12.478 | Mauvais ID |
| 2026-07-08 | JURITEXT000046284523 | JURITEXT000046282365 | 20-20.404 | Mauvais ID |
