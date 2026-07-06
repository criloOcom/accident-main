# VARIABLES STRICTES — Source Unique de Vérité

**NE JAMAIS MODIFIER NI INVENTER.** Ces valeurs prévalent sur tout autre contenu.

## Identité de la victime
- NOM : **[La Victime]**
- DATE_NAISSANCE : **18 janvier 1982** (⚠ jamais 12 mars)
- VILLE_NAISSANCE : **[La Métropole Régionale]**
- NATIONALITÉ : française
- PROFESSION : informaticien indépendant
- ADRESSE : **[L'Adresse de la Victime]**
- EMAIL : **[L'Email de la Victime]**
- SIREN : **[L'Identifiant Professionnel de la Victime]**

## Montants financiers
- MONTANT_PROVISION_REFERE : 5 000 € (demande judiciaire en référé)
- MONTANT_PROVISION_AMIABLE : 15 000 € (demande amiable en mise en demeure)
- MONTANT_ARTICLE_700 : 3 000 €
- MONTANT_TOTAL_ESTIME : 59 600 € (selon tableau détaillé Doc 7 : PGPA 1 400 + IP 15 000 + DFP 25 200 + SE 12 000 + Agrément 3 000 + Art.700 3 000)
- CA_MENSUEL_MOYEN : 750 € (déclaré URSSAF, CA annuel 9 000 € net)
- PGPA_ASSIGNATION : 7 500 € (évaluation forfaitaire dans assignation)
- PGPA_ETUDE : 1 400 € (prorata réel : 750/30×56 jours)
- FACTURE_CHIRURGIE : 790,23 €
- MONTANT_ASTREINTE_145 : 150 €/jour
- MONTANT_ARTICLE_700_145 : 1 500 € (assignation article 145)
- MONTANT_PROVISION_PENALE : 5 000 € (constitution de partie civile)
- MONTANT_ARTICLE_475_1 : 3 000 € (constitution de partie civile — équivalent pénal de l'art. 700)

⚠ **Explication 5k€ vs 15k€** : La demande amiable (15k€) est volontairement plus élevée que la demande en référé (5k€). C'est une stratégie juridique normale : la phase amiable fixe un plafond de négociation, le référé demande un minimum immédiat. Ce n'est pas une incohérence.
⚠ **Doc 7 vs Doc 1** : Les deux documents utilisent des bases de calcul PGPA différentes (forfaitaire vs prorata réel). Ce n'est pas une contradiction — l'assignation fait une estimation large, l'étude détaille le calcul précis. Les deux peuvent coexister.

## Dates clés (⚠ précision absolue requise)
- DATE_ACCIDENT : **29 mai 2026** (vendredi)
- HEURE_ACCIDENT : 15h00
- DATE_CHIRURGIE_SOS_MAIN : **30 mai 2026** (samedi — ⚠ JAMAIS 31 ; le 31/05 est la date du COMPTE-RENDU, pas de la chirurgie)
- LIEU_ACCIDENT : **[L'Adresse de l'Exploitation]**
- ETABLISSEMENT : **[L'Exploitant du Commerce (La SAS)]**
- SERVICES_URGENCE : SMUR 09 (Centre Ariégeois de Soins Immédiats)
- ITT_TOTAL : 56 jours (29/05/2026 → 23/07/2026)
- ⚠ ITT_INITIALE_ERREUR : **[Le Médecin Généraliste]** a noté 1 jour le 01/06 (erreur matérielle, rectifiée à 56j)
- PV_POLICE : 2026/015967 (⚠ info non confirmée par retour officiel — source : courriel Mairie de **[La Ville de l'Accident]** du 01/06/2026 + dossier de plainte déposé par **[La Victime]**)
- DOSSIER_CPAM : **31727387** (⚠ jamais 31713398 — obsolète)
- CAPITAL_SOCIAL : 200 € (2 000 actions de 0,10 €)
- MAIN_ATTEINTE : Main droite uniquement — index droit (⚠ jamais 5e doigt/auriculaire)
- ZONE_LESEE : Index droit uniquement (section partielle tendon fléchisseur + paquet collatéral + neurolyse nerf palmaire)
- PREUVE_BANCAIRE : Wero 15,00 € payé puis remboursé le jour même (aveu implicite de responsabilité)
- DATE_ACCIDENT_CERTIFICAT_ERREUR : Certains certificats mentionnent 29/06/2026 par erreur (date réelle : 29/05/2026)

## Mécanisme de l'accident (VÉRITÉ FACTUELLE)
1. Le coiffeur (**[Le Préposé de l'Exploitation]**) est monté physiquement sur la vasque en céramique du bac à shampoing
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

⚠ **Statut de la SAS vérifié (2026-07-06)** : Active (état administratif "A"), créée le 01/06/2024, siège social au 22 Rue Lafaurie 09000 Foix. Président : Mountasser Sabir. Directrice Générale : Catherine Andissac/Sorroche. Aucune procédure de dissolution ou liquidation en cours (source : API Recherche Entreprises).

## Personnes morales (tokens)
| Rôle | Jeton | Note |
|------|-------|------|
| Exploitant du commerce (la SAS) | `**[L'Exploitant du Commerce (La SAS)]**` | ⚠ Désigne la PERSONNE MORALE SAS, pas ses dirigeants. L'ajout `(La SAS)` prévient toute confusion. Le singulier est correct car une SAS = une entité unique. |
| Établissement SOS Main | `**[L'Établissement SOS Main]**` | |

## Codéfendeurs — Stratégie de mise en cause plurielle
⚠ **Capital 200 € — risque majeur d'insolvabilité.** La SAS seule ne pourra probablement pas indemniser. **Les dirigeants (Président + DG) doivent être assignés PERSONNELLEMENT** comme codéfendeurs, in solidum avec la SAS.

| Défendeur | Qualité | Fondement |
|-----------|---------|-----------|
| `**[L'Exploitant du Commerce (La SAS)]**` | Personne morale (gardienne de la chose + commettant) | Art. 1240, 1242 C.civ. + L.4121-1 C.trav. |
| `**[Le Président de l'Exploitation]**` | Dirigeant de droit (L.227-6 C.com.) | L.227-8 + L.225-251 C.com. + 1240 C.civ. (faute séparable) |
| `**[La Directrice Générale de l'Exploitation]**` | Dirigeante de droit (L.227-6 C.com.) | L.227-8 + L.225-251 C.com. + 1240 C.civ. (faute séparable) |

**Formulation standard à employer partout :**
> *à l'encontre de **[L'Exploitant du Commerce (La SAS)]**, pris en la personne de ses dirigeants, **[Le Président de l'Exploitation]** et **[La Directrice Générale de l'Exploitation]**, et personnellement contre ces derniers*
