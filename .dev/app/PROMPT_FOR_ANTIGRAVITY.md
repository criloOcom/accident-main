<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › [app](./README.md) › PROMPT FOR ANTIGRAVITY*
<hr>
<!-- /Breadcrumb -->

# 🎯 PROMPT POUR ANTI-GRAVITY

Copie-colle ce prompt dans ta conversation anti-gravity :

---

Salut anti-gravity,

**J'ai fait un audit complet sur 6 documents Google Docs représentatifs.** Voici les 4 corrections critiques à appliquer dans `sync_reel_gdocs.py` avant le prochain sync global.

## 🔴 4 CORRECTIONS OBLIGATOIRES

### 1. Marges header/footer = 14pt (0.5cm) — TOUS LES DOCS
```python
# Dans apply_header_footer() + main() :
"marginHeader": {"magnitude": 14, "unit": "PT"},
"marginFooter": {"magnitude": 14, "unit": "PT"},

# AUSSI dans main() forcer documentStyle global :
docs_svc.documents().batchUpdate(documentId=doc_id, body={
    "requests": [{
        "updateDocumentStyle": {
            "documentStyle": {
                "marginTop": {"magnitude": 72, "unit": "PT"},
                "marginBottom": {"magnitude": 72, "unit": "PT"},
                "marginHeader": {"magnitude": 14, "unit": "PT"},
                "marginFooter": {"magnitude": 14, "unit": "PT"}
            },
            "fields": "marginTop,marginBottom,marginHeader,marginFooter"
        }
    }]
}).execute()
```

### 2. Header : Auteur = vrai nom (pas "La Victime") — COURRIERS
```python
auteur = (read_yaml_field(reel_path, "expediteur") or
          read_yaml_field(reel_path, "auteur") or
          read_yaml_field(reel_path, "redacteur") or
          "Sébastien GRAZIDE")
```

### 3. Footer : N° page dynamique `\u0001` — COURRIERS
```python
f_text = "Accident de la Main — Document confidentiel — Page \u0001\n"
# \u0001 = numéro de page dynamique natif Google Docs
```

### 4. Lignes horizontales header/footer — COURRIERS
```python
# Header : borderBottom
header_reqs.append({
    "updateParagraphStyle": {
        "range": {"segmentId": header_id, "startIndex": 0, "endIndex": len(h_text)},
        "paragraphStyle": {
            "alignment": "START",
            "borderBottom": {
                "color": {"color": {"rgbColor": {"red": 0.8, "green": 0.8, "blue": 0.8}}},
                "width": {"magnitude": 0.75, "unit": "PT"},
                "dashStyle": "SOLID"
            }
        },
        "fields": "alignment,borderBottom"
    }
})

# Footer : borderTop
footer_reqs.append({
    "updateParagraphStyle": {
        "range": {"segmentId": footer_id, "startIndex": 0, "endIndex": len(f_text)},
        "paragraphStyle": {
            "alignment": "CENTER",
            "borderTop": {
                "color": {"color": {"rgbColor": {"red": 0.8, "green": 0.8, "blue": 0.8}}},
                "width": {"magnitude": 0.75, "unit": "PT"},
                "dashStyle": "SOLID"
            }
        },
        "fields": "alignment,borderTop"
    }
})
```

---

## 📊 RÉSUMÉ SCORES

| Critère | Courriers | Analyses/Actes |
|---------|-----------|----------------|
| Justifié | 2/3 ✅ | 3/3 ✅ |
| Titres MAJ+GRAS | 2/3 ✅ | 3/3 ✅ |
| Sauts page natifs | 3/3 ✅ | 3/3 ✅ |
| Purge résidus | 3/3 ✅ | 3/3 ✅ |
| **Auteur correct** | **0/3 ❌** | N/A |
| **Ligne sous header** | **0/3 ❌** | N/A |
| **N° page dynamique** | **0/3 ❌** | N/A |
| **Ligne au-dessus footer** | **0/3 ❌** | N/A |
| **Marges 0.5cm** | **0/6 ❌** | **0/6 ❌** |

---

## ⚡ PLAN D'ACTION

1. **Attendre** fin des 2 processus sync en cours (PID 232717, 232743)
2. **Appliquer** les 4 corrections ci-dessus dans `sync_reel_gdocs.py`
3. **Relancer** `python3 .dev/app/sync_reel_gdocs.py --apply`
4. **Re-vérifier** sur 3 docs (1 courrier, 1 acte, 1 analyse)
5. **Commit** + push

---

## 📝 DOCUMENTATION À GRAVER

Dans `Memory/CONVENTIONS.md` §XV :
```
Google Docs Formatting Rules:
- Marges header/footer = 14pt (0.5cm) EXACTEMENT
- Header : "Auteur\tAccident Main — Document confidentiel" + borderBottom gris
- Footer : "Accident de la Main — Document confidentiel — Page \u0001" + borderTop gris
- Auteur lu depuis YAML : expediteur / auteur / redacteur
- Sans header/footer : analyse_juridique, etude_indemnisation, organisation
```

---

Le rapport complet est dans `.dev/app/AUDIT_REPORT_FOR_ANTIGRAVITY.md` si tu veux le détail.

**Attends la fin du sync actuel, puis applique les corrections. Merci !**