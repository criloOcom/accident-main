# VARIABLES STRICTES — Source Unique de Vérité

**NE JAMAIS MODIFIER NI INVENTER.** Ces valeurs prévalent sur tout autre contenu.

## Identité de la victime
- NOM : GRAZIDE Sébastien
- DATE_NAISSANCE : **18 janvier 1982** (⚠ jamais 12 mars)
- VILLE_NAISSANCE : Toulouse (31)
- NATIONALITÉ : française
- PROFESSION : informaticien indépendant
- ADRESSE : 10 Avenue de Purpan, 31700 Blagnac (31)
- EMAIL : sebastien.grazide@gmail.com
- SIREN : 500 474 457

## Montants financiers
- MONTANT_PROVISION_REFERE : 5 000 € (demande judiciaire en référé)
- MONTANT_PROVISION_AMIABLE : 15 000 € (demande amiable en mise en demeure)
- MONTANT_ARTICLE_700 : 3 000 €
- MONTANT_TOTAL_ESTIME : 59 600 € (selon tableau détaillé Doc 7 : PGPA 1 400 + IP 15 000 + DFP 25 200 + SE 12 000 + Agrément 3 000 + Art.700 3 000)
- CA_MENSUEL_MOYEN : 750 € (déclaré URSSAF, CA annuel 9 000 € net)
- PGPA_ASSIGNATION : 7 500 € (évaluation forfaitaire dans assignation)
- PGPA_ETUDE : 1 400 € (prorata réel : 750/30×56 jours)

⚠ **Explication 5k€ vs 15k€** : La demande amiable (15k€) est volontairement plus élevée que la demande en référé (5k€). C'est une stratégie juridique normale : la phase amiable fixe un plafond de négociation, le référé demande un minimum immédiat. Ce n'est pas une incohérence.
⚠ **Doc 7 vs Doc 1** : Les deux documents utilisent des bases de calcul PGPA différentes (forfaitaire vs prorata réel). Ce n'est pas une contradiction — l'assignation fait une estimation large, l'étude détaille le calcul précis. Les deux peuvent coexister.

## Dates clés (⚠ précision absolue requise)
- DATE_ACCIDENT : **29 mai 2026** (vendredi)
- DATE_CHIRURGIE_SOS_MAIN : **30 mai 2026** (samedi — ⚠ JAMAIS 31 ; le 31/05 est la date du COMPTE-RENDU, pas de la chirurgie)
- LIEU_ACCIDENT : 22 Rue Lafaurie, 09000 Foix (09)
- ETABLISSEMENT : SAS LES MAUVAIS GARCONS
- ITT_TOTAL : 56 jours (29/05/2026 → 23/07/2026)
- ⚠ ITT_INITIALE_ERREUR : Dr Oxybel a noté 1 jour le 01/06 (erreur matérielle, rectifiée à 56j)
- PV_POLICE : 2026/015967 (⚠ info non confirmée par retour officiel — source : courriel Mairie de **[La Ville de l'Accident]** du 01/06/2026 + dossier de plainte déposé par **[La Victime]**)
- DOSSIER_CPAM : **31727387** (⚠ jamais 31713398 — obsolète)
- CAPITAL_SOCIAL : 200 € (2 000 actions de 0,10 €)
- MAIN_ATTEINTE : Main droite uniquement — index droit (⚠ jamais 5e doigt/auriculaire)
- ZONE_LESEE : Index droit uniquement (section partielle tendon fléchisseur + paquet collatéral + neurolyse nerf palmaire)
- PREUVE_BANCAIRE : Wero 15,00 € payé puis remboursé le jour même (aveu implicite de responsabilité)
- DATE_ACCIDENT_CERTIFICAT_ERREUR : Certains certificats mentionnent 29/06/2026 par erreur (date réelle : 29/05/2026)

## Mécanisme de l'accident (VÉRITÉ FACTUELLE)
1. Le coiffeur (Ayoub Bennourine) est monté physiquement sur la vasque en céramique du bac à shampoing
2. En descendant, son poids a provoqué le **basculement** de l'équipement
3. La victime a tendu la main droite par réflexe pour protéger le coiffeur
4. La paume a heurté une **cassure majeure préexistante** non signalée sur le flanc de la vasque
5. La vasque ne s'est PAS effondrée — il n'y a PAS de débris de céramique
6. Seule la main droite est touchée — la main gauche est fonctionnelle, la dictée vocale est possible

## Personnes physiques (tokens)
| Rôle | Jeton |
|------|-------|
| Victime | `**[La Victime]**` |
| Président de l'exploitation | `**[Le Président de l'Exploitation]**` |
| Directrice Générale | `**[La Directrice Générale de l'Exploitation]**` |
| Préposé (coiffeur) | `**[Le Préposé de l'Exploitation]**` |
| Propriétaire des murs | `**[Le Propriétaire des Murs]**` |
| Chirurgien SOS Main | `**[Le Chirurgien SOS Main]**` |
| Médecin Urgence | `**[Le Médecin en Urgence]**` |
| Médecin Généraliste | `**[Le Médecin Généraliste]**` |
| Gestionnaire CPAM | `**[La Gestionnaire CPAM]**` |

⚠ **Statut de la SAS inconnu (2026-07-03)** : Aucune information disponible sur le statut actuel de la SAS LES MAUVAIS GARÇONS (activité, fermeture, liquidation, radiation). Les courriers recommandés envoyés le 29 juin 2026 sont restés sans réponse ni AR signé. **Ne jamais affirmer un statut juridique (liquidation, dissolution, etc.) sans source vérifiable.**

## Personnes morales (tokens)
| Rôle | Jeton |
|------|-------|
| Exploitant du commerce | `**[L'Exploitant du Commerce]**` |
| Établissement SOS Main | `**[L'Établissement SOS Main]**` |
