---
title: "TABLE DE SUBSTITUTION — Anonymisation (tokens V2)"
description: "| Texte original | Token |"
type: memory
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › TOKEN MAP*
<hr>
<!-- /Breadcrumb -->

# TABLE DE SUBSTITUTION<br>Anonymisation (tokens V2)

## Personnes physiques {#personnes-physiques}
| Texte original | Token |
|---|---|
<a id="token-la-victime"></a>
| Sébastien GRAZIDE / Grazide / GRAZIDE | `**[La Victime]**` |
<a id="token-le-president-de-l-exploitation"></a>
| Sabir MOUNTASSER / MOUNTASSER / Mountasser SABIR / SABIR / Mountasser Sabir | `**[Le Président de l'Exploitation]**` |
<a id="token-la-directrice-generale-de-l-exploitation"></a>
| Catherine ANDISSAC / SORROCHE / Catherine Andissac / Catherine Sorroche | `**[La Directrice Générale de l'Exploitation]**` |
<a id="token-le-prepose-de-l-exploitation"></a>
| Ayoub Bennourine / BENNOURINE | `**[Le Préposé de l'Exploitation]**` |
<a id="token-le-proprietaire-des-murs"></a>
| Romain DELRIEU / DELRIEU | `**[Le Propriétaire des Murs]**` |
<a id="token-le-chirurgien-sos-main"></a>
| Dr Iskander Djerbi / DJERBI | `**[Le Chirurgien SOS Main]**` |
<a id="token-le-medecin-en-urgence"></a>
| Dr Julie Jardon / JARDON | `**[Le Médecin en Urgence]**` |
<a id="token-le-medecin-generaliste"></a>
| Dr Oxybel / Oxybel | `**[Le Médecin Généraliste]**` |
<a id="token-la-gestionnaire-cpam"></a>
| Sigrid DESBOIS / DESBOIS | `**[La Gestionnaire CPAM]**` |
<a id="token-nom-de-l-avocat-de-la-victime"></a>
| (Avocat de la victime — nom réel à définir) | `**[Nom de l'Avocat de la Victime]**` |
<a id="token-l-adjoint-au-maire-de-la-commune"></a>
| Bernard TAVELLA / TAVELLA / M. TAVELLA | `**[L'Adjoint au Maire de la Commune]**` |

## Personnes morales {#personnes-morales}
| Texte original | Token | Note |
|---|---|---|
<a id="token-l-exploitant-du-commerce-la-sas"></a>
| SAS LES MAUVAIS GARCONS / LES MAUVAIS GARÇONS | `**[L'Exploitant du Commerce (La SAS)]**` | ⚠ Personne morale UNIQUE — PAS le Président ni la DG. L'ajout `(La SAS)` clarifie qu'il s'agit de la société, pas de ses dirigeants. |
<a id="token-l-etablissement-sos-main"></a>
| Clinique de l'Union | `**[L'Établissement SOS Main]**` | |

## Données localisantes / identifiantes {#donnees-localisantes}
| Texte original | Token |
|---|---|
<a id="token-l-adresse-de-la-victime"></a>
| 10 Avenue de Purpan, 31700 Blagnac | `**[L'Adresse de la Victime]**` |
<a id="token-l-adresse-de-l-exploitation"></a>
| 22 Rue Lafaurie, 09000 Foix | `**[L'Adresse de l'Exploitation]**` |
<a id="token-l-adresse-du-president"></a>
| 108 Avenue Paul Bert, 09000 Foix | `**[L'Adresse du Président]**` |
<a id="token-la-ville-de-l-accident"></a>
| Foix | `**[La Ville de l'Accident]**` |
<a id="token-la-ville-de-residence-de-la-victime"></a>
| Blagnac | `**[La Ville de Résidence de la Victime]**` |
<a id="token-la-metropole-regionale"></a>
| Toulouse | `**[La Métropole Régionale]**` |
<a id="token-la-ville-de-l-etablissement-sos-main"></a>
| Saint-Jean | `**[La Ville de l'Établissement SOS Main]**` |
<a id="token-le-telephone-de-la-victime"></a>
| 06 30 51 67 75 | `**[Le Téléphone de la Victime]**` |
<a id="token-code-postal-de-l-accident"></a>
| 09000 | `**[Code Postal de l'Accident]**` |
<a id="token-date-de-naissance-de-la-victime"></a>
| 18 janvier 1982 | `**[Date de naissance de la victime]**` |
<a id="token-l-email-de-la-victime"></a>
| sebastien.grazide@gmail.com | `**[L'Email de la Victime]**` |
<a id="token-l-identifiant-professionnel-de-la-victime"></a>
| 500 474 457 | `**[L'Identifiant Professionnel de la Victime]**` |
<a id="token-l-identifiant-de-l-exploitation"></a>
| 938 033 222 00010 | `**[L'Identifiant de l'Exploitation]**` |
<a id="token-siren-de-l-exploitation"></a>
| 938 033 222 | `**[SIREN de l'Exploitation]**` |
| 31727387 / 2026/015967 | `[ ... ]` (ou le contexte approprié) |

## Personnes morales (suite) {#personnes-morales-suite}
| Texte original | Token |
|---|---|
<a id="token-l-adjoint-au-maire-de-la-commune"></a>
| Monsieur TAVELLA | `**[L'Adjoint au Maire de la Commune]**` |
<a id="token-l-email-de-l-adjoint-au-maire"></a>
| btavella@mairie-foix.fr | `**[L'Email de l'Adjoint au Maire]**` |
<a id="token-l-email-du-secretariat-de-la-mairie"></a>
| secretariat@mairie-foix.fr | `**[L'Email du Secrétariat de la Mairie]**` |

## Tokens temporaires / date tokens (generate_real_versions.py) {#tokens-temporaires}
| Token | Valeur réelle |
|---|---|
<a id="token-date-relance-v2"></a>
| `**[DATE RELANCE V2]**` | 8 juillet 2026 |
<a id="token-date-reouverture-boutique"></a>
| `**[DATE REOUVERTURE BOUTIQUE]**` | 6 juillet 2026 |

## Tokens événementiels (J+) {#tokens-evenementiels}
| Token | Événement |
|---|---|
<a id="token-j-0-accident"></a>
| `**[J+0 Accident]**` | 29 mai 2026 — Jour de l'accident (basculement vasque, plaie main droite) |
<a id="token-j-1-chirurgie"></a>
| `**[J+1 Chirurgie]**` | 30 mai 2026 — Microchirurgie d'urgence SOS Main |
<a id="token-j-2-sortie"></a>
| `**[J+2 Sortie]**` | 31 mai 2026 — Sortie clinique avec ordonnance antalgiques |
<a id="token-j-3-premiers-arrets"></a>
| `**[J+3 Premiers arrêts]**` | 1er juin 2026 — Prescription arrêt de travail Dr OXYBEL |
<a id="token-j-4-depot-de-plainte"></a>
| `**[J+4 Dépôt de plainte]**` | 2 juin 2026 — Dépôt de plainte + constitution partie civile |
<a id="token-j-5-ouverture-cpam"></a>
| `**[J+5 Ouverture CPAM]**` | 3 juin 2026 — Ouverture dossier RCT CPAM |
<a id="token-j-12-facture"></a>
| `**[J+12 Facture]**` | 10 juin 2026 — Facture chirurgie 790,23 € |
<a id="token-j-18-incoherence-cpam"></a>
| `**[J+18 Incohérence CPAM]**` | 16 juin 2026 — Anomalie détectée dossier CPAM |
<a id="token-j-21-controle-chirurgical"></a>
| `**[J+21 Contrôle chirurgical]**` | 19 juin 2026 — Consultation de contrôle J+20 Dr DJERBI |
<a id="token-j-25-premiere-kine"></a>
| `**[J+25 Première kiné]**` | 23 juin 2026 — Début kinésithérapie |
<a id="token-j-27-confirmation-kine"></a>
| `**[J+27 Confirmation kiné]**` | 25 juin 2026 — Confirmation poursuite kiné |
<a id="token-j-31-mises-en-demeure"></a>
| `**[J+31 Mises en demeure]**` | 29 juin 2026 — Envoi LRAR mises en demeure (SAS, Président, DG, Bailleur, Assureur) |
<a id="token-j-32-assignation-refere"></a>
| `**[J+32 Assignation référé]**` | 30 juin 2026 — Rédaction assignation référé-provision |
<a id="token-j-33-plainte-complementaire"></a>
| `**[J+33 Plainte complémentaire]**` | 1er juillet 2026 — Préparation plainte complémentaire |
<a id="token-j-35-ar-proprietaire"></a>
| `**[J+35 AR propriétaire]**` | 3 juillet 2026 — Accusé réception courrier propriétaire |
<a id="token-j-36-lettre-consolidation"></a>
| `**[J+36 Lettre consolidation]**` | 4 juillet 2026 — Demande certificat consolidation à Dr DJERBI |
<a id="token-j-37-assignation-145"></a>
| `**[J+37 Assignation 145]**` | 5 juillet 2026 — Requête article 145 CPC |
<a id="token-j-38-constitution-pc"></a>
| `**[J+38 Constitution PC]**` | 6 juillet 2026 — Constitution de partie civile |
<a id="token-j-38-mise-a-jour"></a>
| `**[J+38 Mise à jour]**` | 6 juillet 2026 — Mise à jour dossier |
<a id="token-j-40-consultation-suivi"></a>
| `**[J+40 Consultation suivi]**` | 8 juillet 2026 — Consultation de suivi J+39 |
<a id="token-j-41-courrier-sie-urssaf"></a>
| `**[J+41 Courrier SIE URSSAF]**` | 9 juillet 2026 — Courrier mutualisation fiscale et sociale |
<a id="token-j-41-requete-constat-145"></a>
| `**[J+41 Requête Constat 145]**` | 9 juillet 2026 — Requête constat huissier article 145 |
<a id="token-j-46-echeance-amiable"></a>
| `**[J+46 Échéance amiable]**` | 14 juillet 2026 — Fin délai amiable avant action judiciaire |
<a id="token-j-55-fin-d-itt"></a>
| `**[J+55 Fin d'ITT]**` | 23 juillet 2026 — Fin prévisionnelle ITT (56 jours) |
<a id="token-j-167-expertise-umj"></a>
| `**[J+167 Expertise UMJ]**` | 12 novembre 2026 — Expertise UMJ (réquisition judiciaire) |

## Limitations connues du script batch_anonymize.py
- Le script utilise `str.replace()` — il ne capture que les chaînes exactes listées
- Les prénoms/noms en casse mixte sans espace entre les deux (ex. "Mountasser Sabir" — ancien format inversé) doivent être ajoutés manuellement comme entrées au script
- Les prénoms seuls (ex. "Sébastien", "Sabir") ne sont pas dans la table — ils peuvent apparaître dans des documents conversationnels (doc 11)