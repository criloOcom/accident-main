---
title: "Exemples de Requêtes MCP Valides"
date: FIXME
description: "Ce document fournit des exemples concrets et testés pour utiliser les MCP Légifrance et Judilibre dans le cadre du projet 'accident-main'."
type: loi
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [⚖️ Lois](./README.md)*
<hr>
<!-- /Breadcrumb -->

# Exemples de Requêtes MCP Valides

Ce document fournit des exemples concrets et testés pour utiliser les MCP Légifrance et Judilibre dans le cadre du projet 'accident-main'.

---

## Légifrance

### Recherche dans les Codes

```python
from mcp_legifrance.server import LegifranceClient

client = LegifranceClient()

# Recherche responsabilité civile
result = client.search(
    query='responsabilité civile',
    fond='CODE',
    page_size=10
)
print(f"Trouvé {len(result['results'])} articles")

# Recherche accidents du travail
result = client.search(
    query='accident du travail',
    fond='CODE',
    page_size=5
)
```

### Recherche Jurisprudence

```python
# Recherche jurisprudence sur accidents en salon de coiffure
result = client.search(
    query='accident salon coiffure',
    fond='JURI',
    page_size=5
)

# Recherche section nerveuse main
result = client.search(
    query='section nerveuse main',
    fond='JURI',
    page_size=3
)
```

### Consultation Directe d'Articles

```python
# Article 1240 Code civil (responsabilité)
article = client.consulte_article('LEGIARTI000032041571')
print(article['text'][:500])  # Affiche les 500 premiers caractères

# Article 1242 Code civil (gardien de la chose)
article = client.consulte_article('LEGIARTI000051786000')

# Article 1719 Code civil (bail)
article = client.consulte_article('LEGIARTI000020459127')
```

### Recherche de Textes Légaux

```python
# Recherche lois sur la responsabilité
result = client.search(
    query='responsabilité',
    fond='LODA',
    page_size=5
)
```

---

## Judilibre

### Recherche par Chambre

```python
from mcp_judilibre.server import JudilibreClient

client = JudilibreClient()

# Chambre civile 1 (responsabilité)
result = client.search(
    query='accident salon coiffure',
    chamber='civ1',
    page_size=5
)

# Chambre sociale (accidents du travail)
result = client.search(
    query='accident travail trajet',
    chamber='soc',
    page_size=5
)

# Chambre commerciale
result = client.search(
    query='responsabilité dirigeant',
    chamber='com',
    page_size=5
)
```

### Recherche par Solution

```python
# Décisions avec cassation
result = client.search(
    query='responsabilité civile',
    solution='cassation',
    page_size=5
)

# Décisions avec rejet
result = client.search(
    query='accident du travail',
    solution='rejet',
    page_size=5
)

# Questions prioritaires de constitutionnalité
result = client.search(
    query='assurance responsabilité',
    solution='qpc',
    page_size=3
)
```

### Recherche par Date

```python
# Jurisprudence récente (2020-2026)
result = client.search(
    query='accident salon',
    date_from='2020-01-01',
    date_to='2026-12-31',
    page_size=10
)

# Jurisprudence avant 2020
result = client.search(
    query='responsabilité civile',
    date_to='2019-12-31',
    page_size=5
)
```

### Recherche par ECLI

```python
# Recherche par identifiant ECLI
result = client.rechercher_par_ecli('ECLI:FR:CCASS:2018:C100865')
print(f"Décision: {result['results'][0]['title']}")
```

### Consultation de Décision

```python
# Consultation par ID Judilibre
decision = client.consulter_decision('60793b3c9ba5988459c3c65e')
print(f"Juridiction: {decision['jurisdiction']}")
print(f"Date: {decision['decision_date']}")
print(f"Solution: {decision['solution']}")
```

---

## Bonnes Pratiques

### 1. Gestion des Erreurs

```python
try:
    result = client.search('terme inexistant', 'JURI')
    if len(result['results']) == 0:
        print("Aucun résultat trouvé")
except Exception as e:
    print(f"Erreur de recherche: {e}")
    # Gérer l'erreur appropriément
```

### 2. Utilisation du Cache

```python
# Le client gère automatiquement le cache pour 24h
# Pas besoin de requêter plusieurs fois pour la même recherche

# Première requête - sera mise en cache
result1 = client.search('responsabilité civile', 'CODE')

# Deuxième requête identique - sera servie depuis le cache
result2 = client.search('responsabilité civile', 'CODE')
```

### 3. Pagination

```python
# Récupération de tous les résultats (avec pagination)
all_results = []
page = 1
while True:
    result = client.search('accident travail', 'JURI', page_size=10, page=page)
    all_results.extend(result['results'])
    if len(result['results']) < 10:  # Moins que page_size = dernière page
        break
    page += 1

print(f"Total résultats: {len(all_results)}")
```

### 4. Filtrage des Résultats

```python
# Filtrer les résultats par pertinence
result = client.search('responsabilité civile', 'JURI', page_size=10)
high_relevance = [r for r in result['results'] if r['score'] > 0.8]

# Filtrer par date
recent = [r for r in result['results'] if r['decision_date'] >= '2020-01-01']
```

---

## Exemples Spécifiques au Projet "accident-main"

### Recherches Recommandées

```python
# 1. Responsabilité des établissements recevant du public (ERP)
client.search('responsabilité ERP accident', 'JURI', chamber='civ1')

# 2. Jurisprudence sur les vasques de salon de coiffure
client.search('vasque salon coiffure accident', 'JURI')

# 3. Responsabilité des dirigeants pour défaut d'assurance
client.search('dirigeant responsabilité défaut assurance', 'JURI', chamber='com')

# 4. Accidents du travail dans les salons de coiffure
client.search('accident travail salon coiffure', 'JURI', chamber='soc')

# 5. Indemnisation des préjudices corporels (Dintilhac)
client.search('préjudice corporel indemnisation', 'JURI')
```

### Articles de Loi Pertinents

```python
# Articles à consulter directement
articles_pertinents = [
    'LEGIARTI000032041571',  # Art. 1240 C. civ. (responsabilité)
    'LEGIARTI000051786000',  # Art. 1242 C. civ. (gardien de la chose)
    'LEGIARTI000020459127',  # Art. 1719 C. civ. (bail)
    'LEGIARTI000017735449',  # Art. L. 124-3 C. assur.
    'LEGIARTI000051869339',  # Art. 145 CPC
    'LEGIARTI000045268436',  # Art. 700 CPC
    'LEGIARTI000042597284',  # Art. 835 CPC
]

for article_id in articles_pertinents:
    article = client.consulte_article(article_id)
    print(f"{article['title']}: {article['url']}")
```

---

## Intégration avec le Projet

### Utilisation dans les Scripts Python

```python
# Dans .dev/app/batch_link_legifrance.py ou autres scripts

from mcp_legifrance.server import LegifranceClient
from mcp_judilibre.server import JudilibreClient

def rechercher_jurisprudence_pertinente():
    """Recherche jurisprudence pour le dossier accident-main."""
    judilibre = JudilibreClient()
    
    # Recherche accidents salon de coiffure
    results = judilibre.search(
        query='accident salon coiffure',
        chamber='civ1',
        page_size=5
    )
    
    # Retourne les 3 décisions les plus pertinentes
    return sorted(results['results'], key=lambda x: x['score'], reverse=True)[:3]

def verifier_article_loi(article_id):
    """Vérifie et retourne le texte d'un article de loi."""
    legifrance = LegifranceClient()
    return legifrance.consulte_article(article_id)
```

### Utilisation dans les Documents Markdown

```markdown
# Références Juridiques

## Jurisprudence Pertinente

### Accident en salon de coiffure
- [Cass. Civ. 2ème, 8 juillet 2021, n° 20-15.106](https://www.legifrance.gouv.fr/juri/id/JURITEXT000043782126)
- [Cass. Civ. 1ère, 8 décembre 2021, n° 20-16.463](https://www.legifrance.gouv.fr/juri/id/JURITEXT000044482848)

## Articles de Loi

- [Article 1240 du Code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041571) (Responsabilité civile)
- [Article 1242 du Code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051786000) (Gardien de la chose)
- [Article 145 du CPC](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051869339) (Mesures d'instruction)
```

---

## Dépannage

### Erreurs Courantes

1. **PISTE_CREDENTIALS non trouvé**
   ```bash
   # Solution: Exécuter setup.sh ou exporter la variable
   export PISTE_CREDENTIALS=$(python3 -c "from souverain import get_secret; print(get_secret('PISTE_CREDENTIALS'))")
   ```

2. **Dépassement de quota**
   ```python
   # Solution: Attendre ou utiliser le cache
   import time
   time.sleep(60)  # Attend 1 minute
   ```

3. **ID JURITEXT invalide**
   ```python
   # Solution: Vérifier l'ID sur Légifrance
    client.consulte_decision('JURITEXT000007043704')  # Ex: Arrêt Costedoat (Ass. Plén., 25 fév. 2000, n° 97-17.378)
   ```

### Vérification des Credentials

```python
# Vérifier que les credentials sont bien configurés
import os
print("PISTE_ENV:", os.environ.get("PISTE_ENV", "sandbox"))
print("PISTE_CREDENTIALS configuré:", bool(os.environ.get("PISTE_CREDENTIALS")))
```

---

## Référence Rapide

### Légifrance - Fonds Disponibles
- `JURI` : Jurisprudence

- `CODE` : Codes (Civil, Pénal, etc.)

- `LODA` : Lois et décrets

- `KALI` : Conventions collectives

- `CNIL` : CNIL

- `CONSTIT` : Constitution

- `JUF` : Jurisprudence financière

### Judilibre - Chambres
- `civ1`, `civ2`, `civ3` : Chambres civiles

- `soc` : Chambre sociale

- `com` : Chambre commerciale

- `crim` : Chambre criminelle

### Judilibre - Solutions
- `cassation` : Décision de cassation

- `rejet` : Rejet du pourvoi

- `qpc` : Question prioritaire de constitutionnalité

- `irrecevabilité` : Pourvoi irrecevable

---

**Dernière mise à jour** : 10 juillet 2026
**Auteur** : Agent IA - Projet Accident-Main