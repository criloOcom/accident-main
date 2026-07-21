---
title: "50 Questions d'Audit Inverse (V3)"
description: "Questions d'audit destinées à opencode pour valider l'intégrité du dépôt"
type: rapport
statut: preparation
date: FIXME
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [Rapports et Analyses](./README.md) › 50 QUESTIONS OPENCODE AUDIT INVERSE*
<hr>
<!-- /Breadcrumb -->

# 50 Questions d'Audit Inverse (V3) — Pour opencode

Ce document contient 50 questions d'audit précises destinées à l'agent **opencode** (dans son autre terminal) pour valider rigoureusement l'intégrité et la conformité des derniers correctifs appliqués au dépôt.

---

## 1. Sécurité & RGPD (Q1–Q10)

1. Le nom réel « DELRIEU » apparaît-il encore en clair dans un fichier du dossier `Token/` ?

2. Le prénom « Hamza » (associé au président de HB Barber) apparaît-il encore en clair dans le dossier `Token/` ?

3. Le nom réel « Catherine SORROCHE » apparaît-il encore en clair dans un document tokenisé (comme `TJ Foix - Mémo - Audience 31-07-2026.md` ou `Erratum`) ?

4. L'adresse email personnelle du bailleur (`romain.delrieu@live.fr`) a-t-elle été anonymisée dans `Police - Note Personnelle.md` ?

5. Quelle est l'adresse exacte de la fiche individuelle de token correspondant à `**[Le Prénom du Préposé]**` ?

6. La fiche `token-prepose-prenom.md` possède-t-elle des liens croisés et bidirectionnels vers `token-exploitation-prepose-nom.md` et `token-exploitation-prepose-telephone.md` ?

7. Le token `[**[Le Prénom du Préposé]**]` est-il correctement répertorié dans la `TOKEN MAP.md` à la ligne 25 ?

8. Le token `[**[Le Prénom du Préposé]**]` est-il listé dans le `README.md` du dossier `Memory/Tokens/` ?

9. Le script `batch_anonymize.py` contient-il les règles de substitution pour `"« Ayoub »"` et `"Ayoub"` ?

10. Reste-t-il des mentions de « Ayoub » en clair dans le corps du texte de `TJ Foix - TJ Foix - CPC 145 - Requête.md` ?

---

## 2. Cibles de Responsabilité — SAS HB BARBER (Q11–Q20)

11. L'introduction de l'acte `TJ Foix - TJ Foix - Référé Provision - Assignation.md` (ligne 32) vise-t-elle désormais la SAS HB BARBER au lieu de la SAS Les Mauvais Garçons (LMG) ?

12. La liste des défendeurs (partie "CONTRE :") dans `TJ Foix - TJ Foix - Référé Provision - Assignation.md` (lignes 52-56) désigne-t-elle la SAS HB BARBER en premier défendeur ?

13. Le président de HB Barber (`[**[Le Président du Nouvel Exploitant]**]`) est-il correctement mentionné en défendeur 2 de l'assignation en référé ?

14. Les adresses respectives de la SAS HB BARBER et de ses dirigeants sont-elles correctement tokenisées dans l'assignation ?

15. La `TC Foix - TC Foix - Mandataire Ad Hoc - Requête.md` vise-t-elle la SAS HB BARBER ou la SAS Les Mauvais Garçons en partie adverse ?

16. Combien d'occurrences de l'ancienne SAS (LMG) ont été remplacées par la SAS HB Barber dans la Requête Mandataire Ad Hoc ?

17. La mission du mandataire ad hoc consiste-t-elle bien à auditer la gestion de la SAS HB BARBER (ligne 103) ?

18. L'interdiction de cession d'actifs demandée au juge dans la Requête Mandataire Ad Hoc vise-t-elle bien les comptes de la SAS HB BARBER ?

19. L'indemnité d'article 700 demandée dans la Requête Mandataire Ad Hoc condamne-t-elle in solidum la SAS HB BARBER et ses dirigeants ?

20. Existe-t-il un erratum d'identité (`Police - Note Erratum Identité.md`) visant à corriger l'erreur de désignation initiale ?

---

## 3. Validité Technique des Builds & Strate Reel (Q21–Q30)

21. Le script `generate_real_versions.py` s'exécute-t-il sans aucune erreur ni avertissement en local ?

22. Combien de fichiers sont actuellement générés dans l'arborescence `Actes/Reel/` ?

23. La version Reel de `Plainte Complémentaire - Correction HB BARBER.md` contient-elle encore des tokens non résolus entre crochets ?

24. Le document Reel `TJ Foix - TJ Foix - Référé Provision - Assignation.md` a-t-il vu ses tokens résolus avec les identités réelles uniformisées ?

25. La valeur réelle de `[N° Transaction Wero]` (`IPR000297029234`) est-elle correctement substituée dans les versions réelles ?

26. Les adresses des dirigeants de HB BARBER sont-elles bien résolues par le dictionnaire du générateur réel ?

27. Existe-t-il des fichiers de cache `__pycache__` ou `.pytest_cache` résiduels dans le dossier `.dev/app/` ?

28. Le script unitaire `anonymize_doc.py` comporte-t-il une erreur d'import de `sys` à son exécution ?

29. Le dictionnaire de `consolidate_sheet.py` gère-t-il bien l'entrée `"Ayoub"` ?

30. Le script `check_consistency.py` se lance-t-il sans signaler de divergences ou de conflits de données ?

---

## 4. Cohérence des Pièces & Dates (Q31–Q40)

31. Quelle est la date de la plainte complémentaire figurant dans son corps de texte (17 juillet ou 20 juillet 2026) ?

32. La date de dépôt déclarée de la plainte complémentaire dans la Requête 145 CPC est-elle cohérente avec la date réelle de rédaction de l'acte ?

33. Le bordereau de la plainte complémentaire au commissariat comporte-t-il bien 8 pièces jointes numérotées ?

34. Le bordereau de la Requête 145 CPC comporte-t-il 17 pièces numérotées ?

35. Le témoin TAVELLA (pièce n°17) est-il cité de manière identique dans le corps et le bordereau de la requête 145 ?

36. Les 4 LRAR du 29 juin 2026 possèdent-elles des numéros de suivi réels cohérents avec la `PIECES MAP.md` ?

37. Les montants financiers (15 € Wero, 790,23 € chirurgie, 15 000 € provision) sont-ils identiques dans tous les documents et conformes à `STRICT VARIABLES.md` ?

38. L'astreinte de 150 € par jour demandée dans la Requête 145 est-elle cohérente avec les conclusions au fond ?

39. La CPAM est-elle créditée d'un dossier de Recours contre Tiers sous la même référence dans tous les actes ?

40. Les orthographes des noms réelles (GRAZIDE, BENNOURINE, BERGUIGA, SORROCHE) sont-elles exemptes de coquilles (ex: "Sorrock-") ?

---

## 5. Navigation, Liens & Hook de Commit (Q41–Q50)

41. L'audit d'intégrité des README (`audit_readme_integrity.py`) signale-t-il des fichiers absents ou non listés ?

42. Le hook `.dev/hooks/pre-commit` bloque-t-il le commit en raison de liens 404 dans les fichiers modifiés ?

43. Les liens vers `Prefecture.md` et `SIE URSSAF Mutualisation.md` dans `STATUS.md` ont-ils été corrigés avec un chemin relatif correct ?

44. Le lien vers `RAPPORT_AUDIT_RISQUES.md` a-t-il été purgé de `STATUS.md` et `TODO.md` ?

45. Les dossiers de rapports orphelins (ex: `85_Coherence_2026-07-15/`) ont-ils leur README.md d'indexation ?

46. L'audit des citations (`audit_citation_links.py`) montre-t-il des citations non liées dans les fichiers de production ?

47. Tous les hyperliens Légifrance vers JURITEXT et LEGIARTI pointent-ils vers des URL valides ?

48. Le protocole JURITEXT en 2 étapes (Légifrance-prod puis OpenLegi) a-t-il bien été consigné dans `JURITEXT_PROTOCOL.md` ?

49. Les fichiers réels générés sont-ils exclus du pre-commit hook pour éviter les fausses alertes ?

50. La note globale de conformité du dépôt dépasse-t-elle désormais le seuil minimal de 95/100 après application de ces correctifs ?