---
title: "Audit des variables STRICT_VARIABLES et Tokens"
description: "Rapport recensant les incohérences factuelles dans les actes et rapports par rapport aux STRICT_VARIABLES."
type: rapport
---

<!-- Breadcrumb -->
<a href="../README.md">Retour</a>
<!-- /Breadcrumb -->

<hr>

# Audit des variables STRICT_VARIABLES et Tokens

Ce rapport liste les incohérences détectées dans les fichiers sous `⚖️ Actes/🔑 Token/` et `📊 Rapports/` par rapport aux règles définies dans `🧠 Memory/STRICT_VARIABLES.md`.

<hr><hr>

## I — INCOHÉRENCES DÉTECTÉES

### I.1 — Fichier : `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📑 Bordereau Unifie.md`

- **Ligne 28** : Profession erronée (victime qualifiée de 'coiffeur')
  - **Valeur erronée** : `- [**[J+4 Dépôt de plainte]**](../../%F0%9F%A7%A0%20Memory/%F0%9F%97%82%EF%B8%8F%20Tokens/token-j-4-depot-de-plainte.md) — Procès-verbal de police n° [**[N° PV Police]**](../../%F0%9F%A7%A0%20Memory/TOKEN%20MAP.md#donnees-localisantes) (Police Nationale [**[La Métropole Régionale]**](../../%F0%9F%A7%A0%20Memory/%F0%9F%97%82%EF%B8%8F%20Tokens/token-accident-metropole.md)) : Dépôt de plainte de [**[La Victime]**](../../%F0%9F%A7%A0%20Memory/%F0%9F%97%82%EF%B8%8F%20Tokens/token-victime-nom-complet.md) pour blessures involontaires. Description de l'accident : montée du coiffeur sur la vasque en céramique, basculement, cassure préexistante. PV complet 3 pages.`
  - **Correction suggérée** : Remplacer par 'informaticien indépendant'.

### I.2 — Fichier : `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/🚔 PV Audition Plainte Complementaire Foix.md`

- **Ligne 58** : Date d'accident erronée (29 mai 2026 attendu)
  - **Valeur erronée** : `Premièrement, face au silence de l'exploitant le jour de l'accident, j'ai envoyé des lettres recommandées avec accusé de réception (LRAR) le 29 juin 2026 aux dirigeants ainsi qu'au propriétaire des murs. Le but de ces courriers était d'obtenir les coordonnées de leur assurance Responsabilité Civile Professionnelle, une obligation légale, pour permettre la prise en charge de mes préjudices, qui sont lourds (j'ai 56 jours d'ITT). Or, ces courriers me sont revenus avec la mention "NPAI - Destinataire inconnu à l'adresse". Pourtant, j'ai vérifié sur le RNE/INPI le 10 juillet 2026, la société est toujours officiellement immatriculée à cette adresse au [**[L'Adresse de l'Exploitation]**]. Il y a donc une volonté manifeste de se soustraire à leurs obligations et de ne réceptionner aucune communication de ma part ou de celle de la justice.`
  - **Correction suggérée** : Corriger la date en '29 mai 2026'.

### I.3 — Fichier : `⚖️ Actes/🔑 Token/✉️ Courriers/📋s/📋 Temoin Client.md`

- **Ligne 40** : Profession erronée (victime qualifiée de 'coiffeur')
  - **Valeur erronée** : `J'ai alors vu un autre client, [**[La Victime]**](../../%F0%9F%A7%A0%20Memory/%F0%9F%97%82%EF%B8%8F%20Tokens/token-victime-nom-complet.md), tendre la main droite par un réflexe immédiat pour tenter de rattraper le coiffeur et le protéger de la chute. Sa paume a heurté le flanc de la vasque.`
  - **Correction suggérée** : Remplacer par 'informaticien indépendant'.

### I.4 — Fichier : `⚖️ Actes/🔑 Token/✉️ Courriers/🚨 Signalements/✉️🚨 URSSAF.md`

- **Ligne 60** : Profession erronée (victime qualifiée de 'coiffeur')
  - **Valeur erronée** : `- Le prepose de l'exploitation exercait une activite professionnelle de coiffeur au sein de l'etablissement sans qu'aucune information sur son statut (contrat de travail, bulletin de paie, declaration prealable a l'embauche) n'ait pu etre communiquee<br>`
  - **Correction suggérée** : Remplacer par 'informaticien indépendant'.

### I.5 — Fichier : `⚖️ Actes/🔑 Token/📚 Analyses juridiques/🛡️ Tableau Defense Reponse.md`

- **Ligne 22** : Profession erronée (victime qualifiée de 'coiffeur')
  - **Valeur erronée** : `| A3 | « La victime a mis sa main là où il ne fallait pas, c'est sa faute. » | Le geste de tendre la main pour retenir un coiffeur qui tombe est un **réflexe de protection**, pas une prise de risque volontaire. Il n'y a pas de comportement anormal ou téméraire de la victime ; au contraire, l'origine du danger est la combinaison vasque cassée + montée dessus sans moyen adapté. | Déclaration victime (PV initial + plainte complémentaire), jurisprudence générale sur le réflexe de protection (à documenter par l'avocat si besoin) |`
  - **Correction suggérée** : Remplacer par 'informaticien indépendant'.

### I.6 — Fichier : `📊 Rapports/MODELE_ENVOI_AVOCAT_REEL.md`

- **Ligne 11** : Nom SAS non tokenisé
  - **Valeur erronée** : `**Objet** : Dossier accident corporel — [NOM_VICTIME] c. SAS [NOM_SAS] — TJ Foix — Demande de prise en charge`
  - **Correction suggérée** : Remplacer 'NOM_SAS' par '**[L'Exploitant du Commerce (La SAS)]**'.

- **Ligne 17** : Nom SAS non tokenisé
  - **Valeur erronée** : `Vous avez été désigné au titre de l'aide juridictionnelle pour défendre mes intérêts dans le cadre de l'accident dont j'ai été victime le [DATE_ACCIDENT] au salon [NOM_SAS] à [VILLE].`
  - **Correction suggérée** : Remplacer 'NOM_SAS' par '**[L'Exploitant du Commerce (La SAS)]**'.

- **Ligne 47** : Nom SAS non tokenisé
  - **Valeur erronée** : `**Objet** : Demande de désignation d'avocat au titre de l'aide juridictionnelle — Dossier accident corporel — [NOM_VICTIME] c. SAS [NOM_SAS] — TJ Foix`
  - **Correction suggérée** : Remplacer 'NOM_SAS' par '**[L'Exploitant du Commerce (La SAS)]**'.

- **Ligne 56** : Montant DFP erroné (25 200 € attendu)
  - **Valeur erronée** : `Victime d'un accident corporel grave le [DATE_ACCIDENT] au salon [NOM_SAS] à [VILLE], j'ai subi une plaie palmaire profonde de la main droite dominante avec section partielle du tendon FDP et du paquet vasculo-nerveux collatéral radial de l'index, ayant nécessité une microchirurgie d'urgence en SOS Main. L'expertise judiciaire du 29 mai 2027 a fixé la consolidation au 1er mars 2027, retenu un DFP de 12 % et une incidence professionnelle majeure (informaticien indépendant — perte fonctionnelle de la main droite). La fourchette globale d'indemnisation est estimée entre 120 000 et 160 000 €.`
  - **Correction suggérée** : Mettre à jour à 25 200 €.
  - **⚠️ CORRIGÉ (14/07/2026) — AUSSI :** La date expertise `29 mai 2027` a été corrigée en `12 novembre 2026` dans 8 fichiers.

- **Ligne 56** : Nom SAS non tokenisé
  - **Valeur erronée** : `Victime d'un accident corporel grave le [DATE_ACCIDENT] au salon [NOM_SAS] à [VILLE], j'ai subi une plaie palmaire profonde de la main droite dominante avec section partielle du tendon FDP et du paquet vasculo-nerveux collatéral radial de l'index, ayant nécessité une microchirurgie d'urgence en SOS Main. L'expertise judiciaire du 29 mai 2027 a fixé la consolidation au 1er mars 2027, retenu un DFP de 12 % et une incidence professionnelle majeure (informaticien indépendant — perte fonctionnelle de la main droite). La fourchette globale d'indemnisation est estimée entre 120 000 et 160 000 €.`
  - **Correction suggérée** : Remplacer 'NOM_SAS' par '**[L'Exploitant du Commerce (La SAS)]**'.
  - **⚠️ CORRIGÉ (14/07/2026)** : `NOM_SAS` → `[L'Exploitant du Commerce (La SAS)]` appliqué. **AUSSI :** date expertise corrigée (cf. ci-dessus).

- **Ligne 77** : Nom SAS non tokenisé
  - **Valeur erronée** : ``[NOM_SAS]` — Raison sociale de l'exploitation`
  - **Correction suggérée** : Remplacer 'NOM_SAS' par '**[L'Exploitant du Commerce (La SAS)]**'.

### I.7 — Fichier : `📊 Rapports/RAPPORT_AUDIT_FGTI_DINTILHAC.md`

- **Ligne 178** : Montant DFP erroné (25 200 € attendu)
  - **Valeur erronée** : `| Justification de l'IP à 30 000 € | **7/10** | Méthode BIBAL solide mais risque de double compte DFP |`
  - **Correction suggérée** : Mettre à jour à 25 200 €.

### I.8 — Fichier : `📊 Rapports/analyse-multi-angle/04_Rapport_Juge_Civil.md`

- **Ligne 65** : Montant/Cotation SE erroné (14 000 € ou 4/7 attendu)
  - **Valeur erronée** : `- **Souffrances Endurées (SE)** : 15 000 €.`
  - **Correction suggérée** : Mettre à jour avec 14 000 € (cotation 4/7).
