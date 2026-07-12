---
title: "TABLE DE SUBSTITUTION — Anonymisation (tokens V2)"
description: "| Texte original | Jeton |"
type: memory
---











<!-- Breadcrumb -->
[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › TOKEN MAP
<!-- /Breadcrumb -->

# TABLE DE SUBSTITUTION — Anonymisation (tokens V2)

## Personnes physiques {#personnes-physiques}
| Texte original | Jeton |
|---|---|
| Sébastien GRAZIDE / Grazide / GRAZIDE | `**[La Victime]**` |
| Sabir MOUNTASSER / MOUNTASSER / Mountasser SABIR / SABIR / Mountasser Sabir | `**[Le Président de l'Exploitation]**` |
| Catherine ANDISSAC / SORROCHE / Catherine Andissac / Catherine Sorroche | `**[La Directrice Générale de l'Exploitation]**` |
| Ayoub Bennourine / BENNOURINE | `**[Le Préposé de l'Exploitation]**` |
| Romain DELRIEU / DELRIEU | `**[Le Propriétaire des Murs]**` |
| Dr Iskander Djerbi / DJERBI | `**[Le Chirurgien SOS Main]**` |
| Dr Julie Jardon / JARDON | `**[Le Médecin en Urgence]**` |
| Dr Oxybel / Oxybel | `**[Le Médecin Généraliste]**` |
| Sigrid DESBOIS / DESBOIS | `**[La Gestionnaire CPAM]**` |
| (Avocat de la victime — nom réel à définir) | `**[Nom de l'Avocat de la Victime]**` |
| Bernard TAVELLA / TAVELLA / M. TAVELLA | `**[L'Adjoint au Maire de la Commune]**` |

## Personnes morales {#personnes-morales}
| Texte original | Jeton | Note |
|---|---|---|
| SAS LES MAUVAIS GARCONS / LES MAUVAIS GARÇONS | `**[L'Exploitant du Commerce (La SAS)]**` | ⚠ Personne morale UNIQUE — PAS le Président ni la DG. L'ajout `(La SAS)` clarifie qu'il s'agit de la société, pas de ses dirigeants. |
| Clinique de l'Union | `**[L'Établissement SOS Main]**` | |

## Données localisantes / identifiantes {#donnees-localisantes}
| Texte original | Jeton |
|---|---|
| 10 Avenue de Purpan, 31700 Blagnac | `**[L'Adresse de la Victime]**` |
| 22 Rue Lafaurie, 09000 Foix | `**[L'Adresse de l'Exploitation]**` |
| 108 Avenue Paul Bert, 09000 Foix | `**[L'Adresse du Président]**` |
| Foix | `**[La Ville de l'Accident]**` |
| Blagnac | `**[La Ville de Résidence de la Victime]**` |
| Toulouse | `**[La Métropole Régionale]**` |
| Saint-Jean | `**[La Ville de l'Établissement SOS Main]**` |
| sebastien.grazide@gmail.com | `**[L'Email de la Victime]**` |
| 500 474 457 | `**[L'Identifiant Professionnel de la Victime]**` |
| 938 033 222 00010 | `**[L'Identifiant de l'Exploitation]**` |
| 938 033 222 | `**[SIREN de l'Exploitation]**` |
| 31727387 / 2026/015967 | `[ ... ]` (ou le contexte approprié) |

## Personnes morales (suite) {#personnes-morales-suite}
| Texte original | Jeton |
|---|---|
| Monsieur TAVELLA | `**[L'Adjoint au Maire de la Commune]**` |
| btavella@mairie-foix.fr | `**[L'Email de l'Adjoint au Maire]**` |
| secretariat@mairie-foix.fr | `**[L'Email du Secrétariat de la Mairie]**` |

## Tokens temporaires / date tokens (generate_real_versions.py) {#tokens-temporaires}
| Token | Valeur réelle |
|---|---|
| `**[DATE RELANCE V2]**` | 8 juillet 2026 |
| `**[DATE REOUVERTURE BOUTIQUE]**` | 6 juillet 2026 |

## Tokens événementiels (J+) {#tokens-evenementiels}
| Token | Événement |
|---|---|
| `**[J+0 Accident]**` | 29 mai 2026 — Jour de l'accident (basculement vasque, plaie main droite) |
| `**[J+1 Chirurgie]**` | 30 mai 2026 — Microchirurgie d'urgence SOS Main |
| `**[J+2 Sortie]**` | 31 mai 2026 — Sortie clinique avec ordonnance antalgiques |
| `**[J+3 Premiers arrêts]**` | 1er juin 2026 — Prescription arrêt de travail Dr OXYBEL |
| `**[J+4 Dépôt de plainte]**` | 2 juin 2026 — Dépôt de plainte + constitution partie civile |
| `**[J+5 Ouverture CPAM]**` | 3 juin 2026 — Ouverture dossier RCT CPAM |
| `**[J+12 Facture]**` | 10 juin 2026 — Facture chirurgie 790,23 € |
| `**[J+18 Incohérence CPAM]**` | 16 juin 2026 — Anomalie détectée dossier CPAM |
| `**[J+21 Contrôle chirurgical]**` | 19 juin 2026 — Consultation de contrôle J+20 Dr DJERBI |
| `**[J+25 Première kiné]**` | 23 juin 2026 — Début kinésithérapie |
| `**[J+27 Confirmation kiné]**` | 25 juin 2026 — Confirmation poursuite kiné |
| `**[J+31 Mises en demeure]**` | 29 juin 2026 — Envoi LRAR mises en demeure (SAS, Président, DG, Bailleur, Assureur) |
| `**[J+32 Assignation référé]**` | 30 juin 2026 — Rédaction assignation référé-provision |
| `**[J+33 Plainte complémentaire]**` | 1er juillet 2026 — Préparation plainte complémentaire |
| `**[J+35 AR propriétaire]**` | 3 juillet 2026 — Accusé réception courrier propriétaire |
| `**[J+36 Lettre consolidation]**` | 4 juillet 2026 — Demande certificat consolidation à Dr DJERBI |
| `**[J+37 Assignation 145]**` | 5 juillet 2026 — Requête article 145 CPC |
| `**[J+38 Constitution PC]**` | 6 juillet 2026 — Constitution de partie civile |
| `**[J+38 Mise à jour]**` | 6 juillet 2026 — Mise à jour dossier |
| `**[J+40 Consultation suivi]**` | 8 juillet 2026 — Consultation de suivi J+39 |
| `**[J+41 Courrier SIE URSSAF]**` | 9 juillet 2026 — Courrier mutualisation fiscale et sociale |
| `**[J+41 Requête Constat 145]**` | 9 juillet 2026 — Requête constat huissier article 145 |
| `**[J+46 Échéance amiable]**` | 14 juillet 2026 — Fin délai amiable avant action judiciaire |
| `**[J+55 Fin d'ITT]**` | 23 juillet 2026 — Fin prévisionnelle ITT (56 jours) |
| `**[J+167 Expertise UMJ]**` | 12 novembre 2026 — Expertise UMJ (réquisition judiciaire) |

## Limitations connues du script batch_anonymize.py
- Le script utilise `str.replace()` — il ne capture que les chaînes exactes listées
- Les prénoms/noms en casse mixte sans espace entre les deux (ex. "Mountasser Sabir" — ancien format inversé) doivent être ajoutés manuellement comme entrées au script
- Les prénoms seuls (ex. "Sébastien", "Sabir") ne sont pas dans la table — ils peuvent apparaître dans des documents conversationnels (doc 11)