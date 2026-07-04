# TABLE DE SUBSTITUTION — Anonymisation (tokens V2)

## Personnes physiques
| Texte original | Jeton |
|---|---|
| Sébastien GRAZIDE / Grazide / GRAZIDE | `[La Victime]` |
| Mountasser SABIR / SABIR / Mountasser Sabir | `[Le Président de l'Exploitation]` |
| Catherine ANDISSAC / SORROCHE / Catherine Andissac / Catherine Sorroche | `[La Directrice Générale de l'Exploitation]` |
| Ayoub Bennourine / BENNOURINE | `[Le Préposé de l'Exploitation]` |
| Romain DELRIEU / DELRIEU | `[Le Propriétaire des Murs]` |
| Dr Iskander Djerbi / DJERBI | `[Le Chirurgien SOS Main]` |
| Dr Julie Jardon / JARDON | `[Le Médecin en Urgence]` |
| Dr Oxybel / Oxybel | `[Le Médecin Généraliste]` |
| Sigrid DESBOIS / DESBOIS | `[La Gestionnaire CPAM]` |

## Personnes morales
| Texte original | Jeton |
|---|---|
| SAS LES MAUVAIS GARCONS / LES MAUVAIS GARÇONS | `[L'Exploitant du Commerce]` |
| Clinique de l'Union | `[L'Établissement SOS Main]` |

## Données localisantes / identifiantes
| Texte original | Jeton |
|---|---|
| 10 Avenue de Purpan, 31700 Blagnac | `[L'Adresse de la Victime]` |
| 22 Rue Lafaurie, 09000 Foix | `[L'Adresse de l'Exploitation]` |
| 108 Avenue Paul Bert, 09000 Foix | `[L'Adresse du Président]` |
| Foix | `[La Ville de l'Accident]` |
| Blagnac | `[La Ville de Résidence de la Victime]` |
| Toulouse | `[La Métropole Régionale]` |
| Saint-Jean | `[La Ville de l'Établissement SOS Main]` |
| sebastien.grazide@gmail.com | `[L'Email de la Victime]` |
| 500 474 457 | `[L'Identifiant Professionnel de la Victime]` |
| 938 033 222 00010 | `[L'Identifiant de l'Exploitation]` |
| 31727387 / 2026/015967 | `[ ... ]` (ou le contexte approprié) |

## Limitations connues du script batch_anonymize.py
- Le script utilise `str.replace()` — il ne capture que les chaînes exactes listées
- Les prénoms/noms en casse mixte sans espace entre les deux (ex. "Mountasser Sabir") doivent être ajoutés manuellement comme entrées au script
- Les prénoms seuls (ex. "Sébastien", "Mountasser") ne sont pas dans la table — ils peuvent apparaître dans des documents conversationnels (doc 11)
