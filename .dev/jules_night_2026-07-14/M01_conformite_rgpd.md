# MISSION 1 — Audit de conformité RGPD / Loi Informatique et Libertés

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport `📊 Rapports/RAPPORT_CONFORMITE_RGPD_2026-07-14.md` analysant la **conformité du dossier accident-main au RGPD et à la loi n° 78-17 du 6 janvier 1978 (Informatique et Libertés)**, en vue de sécuriser juridiquement la gestion des données à caractère personnel (victime, dirigeants, témoins, tiers).

## ANGLES D'ANALYSE (développe chacun avec fondements légaux vérifiés)

1. **Double strate 🔑 Token / 👤 Reel** : évalue si le mécanisme d'anonymisation (tokens + génération des versions réelles via `generate_real_versions.py`) est conforme aux principes RGPD (minimisation des données, articles 5 et 25 RGPD, « privacy by design »). Recommande des renforcements.
2. **Fichiers contenant des données réelles** : liste (d'après ta lecture de TOKEN MAP.md et du dépôt) les endroits où des identités réelles pourraient encore fuiter (ex. anciens fichiers, caches, scripts). Propose un plan de purge.
3. **Durée de conservation** : quelle durée de conservation est légale pour ce dossier de contentieux (réf. art. L.213-1 à L.213-8 du CRPA pour le contentieux, et principe de proportionnalité RGPD) ? Donne une règle claire.
4. **Droits des personnes** : comment le dossier doit-il gérer un éventuel droit d'accès / de rectification / d'effacement d'un codéfendeur (ex. la SAS, ses dirigeants) ?
5. **Sécurité** : le dépôt Git (GitHub), les fichiers locaux, les caches — quels risques et quelles mesures (chiffrement, accès, .gitignore des fichiers réels) ?
6. **Base légale du traitement** : identifie la base légale (intérêt légitime de la victime à la défense de ses droits, art. 6 §1 f) RGPD ; art. 9 données santé → condition de l'art. 9 §2 f) RGPD pour contentieux).

## LIVRABLE

Un rapport structuré, avec : constat de conformité, liste des risques (sévériité), plan d'action chiffré et priorisé, et un modèle de mention de confidentialité à apposer en en-tête des versions réelles. Cite TOUS les articles via Légifrance.
