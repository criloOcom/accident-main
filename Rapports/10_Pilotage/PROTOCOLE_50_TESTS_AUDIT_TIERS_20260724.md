# PROTOCOLE DE VÉRIFICATION ET AUDIT EXHAUSTIF (50 TESTS)
**Projet** : Accident de la Main (`criloOcom/accident-main`)  
**Commit de référence** : `ddf7b187` (Branche `main`)  
**Objectif** : Transmettre ce cahier de recettes (50 tests vérifiables par commandes ou inspection directe) à un **agent tiers indépendant ("blanc")** pour auditer la réalité, la conformité et l'absence d'hallucination du travail effectué.

---

## CONTEXTE ET PÉRIMÈTRE DE L'AUDIT

Le travail réalisé visait à :
1. **Résoudre les citations d'articles de loi litigieuses/douteuses** à l'aide de l'audit externe Doctrine.fr et de la vérification officielle Légifrance (API PISTE).

2. **Corriger l'article erroné 827 du Code de procédure civile** par la bonne référence juridique (Article 853 CPC).

3. **Étape 4 (Règle #11 durcie)** : Mettre en place un script et un pré-commit bloquant empêchant tout commit d'un nouveau document citant des articles de loi sans note de bas de page.

4. **Exploitation à 1000 % de la bibliothèque `Lois/` et du Google Sheet** (`ANNUAIRE Lois Et NotionsDeDroit`) : s'assurer qu'aucune information utile n'a été effacée et que les notes de bas de page renvoient vers la documentation locale.

5. **Résorption du stock de citations nues** et mise à jour synchronisée des 138 versions réelles (`Actes/Reel/`).

---

## LISTE DES 50 TESTS À EXÉCUTER PAR L'AGENT TIERS

### A. Intégrité des Commits et Synchronisation GitHub (Tests 1 à 5)
- [ ] **Test 01** : Vérifier que le dernier commit sur la branche `main` est `ddf7b187` avec le message `feat(legal): resorption des citations nues et fiabilisation de inject_footnotes_v2`.  
  *Commande* : `git log -1 --format="%H %s"`
- [ ] **Test 02** : Vérifier que la branche locale `main` est parfaitement synchronisée avec `origin/main` sans retard.  
  *Commande* : `git status`
- [ ] **Test 03** : Vérifier la présence du commit `fe53fda7` dédié à l'exploitation de la bibliothèque `Lois/` et du Sheet.  
  *Commande* : `git log --grep="exploitation à 1000%"`
- [ ] **Test 04** : Vérifier la présence du commit `31e2ad47` dédié au durcissement de l'Étape 4 et la correction de 827 CPC.  
  *Commande* : `git log --grep="Étape 4"`
- [ ] **Test 05** : S'assurer qu'aucun fichier non suivi ni conflit résiduel ne perturbe l'arbre de travail.  
  *Commande* : `git status --porcelain`

---

### B. Audit de l'Étape 4 — Pré-commit et Règle #11 Durcie (Tests 6 à 15)
- [ ] **Test 06** : Vérifier l'existence du script d'audit `.dev/app/audit_footnote_citations.py`.  
  *Vérification* : Existence du fichier sur le disque.
- [ ] **Test 07** : Vérifier l'intégration du contrôle dans l'orchestrateur `.dev/hooks/pre-commit`.  
  *Commande* : `grep -n "audit_footnote_citations.py" .dev/hooks/pre-commit`
- [ ] **Test 08** : Vérifier que l'audit `audit_footnote_citations.py` renvoie un code retour `0` ou `2` (aucun document non sourcé).  
  *Commande* : `python3 .dev/app/audit_footnote_citations.py`
- [ ] **Test 09 (Test d'Efficacité Bloquante)** : Créer un fichier de test temporaire `Actes/Token/Courriers/_test_blocage.md` citant `l'article 1240 du Code civil` sans note de bas de page, exporter `STAGED="Actes/Token/Courriers/_test_blocage.md"` et exécuter l'audit. Le script doit renvoyer **code exit 1** (BLOQUANT).

- [ ] **Test 10** : Supprimer le fichier de test temporaire et ré-exécuter l'audit pour confirmer le retour à l'état propre.

- [ ] **Test 11** : Vérifier la présence de la règle #11 mise à jour dans `Memory/RULES.md`.  
  *Commande* : `grep -n "Règle #11" Memory/RULES.md`
- [ ] **Test 12** : Vérifier la documentation du protocole dans `Memory/JURITEXT_PROTOCOL.md`.  
  *Vérification* : Consultation du fichier.
- [ ] **Test 13** : Inspecter `.dev/app/inject_footnotes_v2.py` pour s'assurer que la fonction `norm_code` effectue un matching exact sur les alias pour éviter les faux positifs.

- [ ] **Test 14** : Vérifier que `KEYWORDS` dans `inject_footnotes_v2.py` inclut `cpc`, `cpp`, `c. civ`, `c. com`, `crpa`, `csp`.

- [ ] **Test 15** : Confirmer que la fenêtre de contexte dans `inject_footnotes_v2.py` pour détecter le code s'étend à au moins 150/200 caractères.

---

### C. Vérification de la Correction de l'Article 827 CPC (Tests 16 à 20)
- [ ] **Test 16** : Vérifier l'absence totale du tag `article 827 [À VÉRIFIER] CPC` dans tout le dossier `Actes/Token/`.  
  *Commande* : `grep -rn "827" Actes/Token/`
- [ ] **Test 17** : Confirmer que l'article 853 du Code de procédure civile a bien remplacé l'article 827 dans `TJ_Foix_Conclusions_au_Fond.md`.  
  *Commande* : `grep -n "853" Actes/Token/Actes_proceduraux/Contentieux_civil/TJ_Foix_Conclusions_au_Fond.md`
- [ ] **Test 18** : Vérifier que l'article 853 CPC possède sa note de bas de page Légifrance valide (`LEGIARTI000044200291`).  
  *Commande* : `grep -A 5 "LEGIARTI000044200291" Actes/Token/Actes_proceduraux/Contentieux_civil/TJ_Foix_Conclusions_au_Fond.md`
- [ ] **Test 19** : Vérifier que l'article 853 CPC est également présent et synchronisé dans la version réelle `Actes/Reel/Actes_proceduraux/Contentieux_civil/TJ_Foix_Conclusions_au_Fond.md`.

- [ ] **Test 20** : Confirmer l'absence totale du tag `[À VÉRIFIER]` dans l'ensemble des dossiers sortants (`Actes/Token/Courriers`, `Actes/Token/Actes_proceduraux`, `Actes/Token/Analyses_juridiques`).  
  *Commande* : `grep -rn "À VÉRIFIER" Actes/Token/` (Résultat attendu : 0 occurrence).

---

### D. Exploitation de la Bibliothèque `Lois/` et du Google Sheet (Tests 21 à 35)
- [ ] **Test 21** : Vérifier la présence du rapport d'audit `Rapports/10_Pilotage/AUDIT_BIBLIOTHEQUE_LOIS_20260724.md`.

- [ ] **Test 22** : Vérifier la présence du rapport d'audit `Rapports/10_Pilotage/DOCTRINE_PROMPT_ARTICLES_DOUTEUX_20260724.md`.

- [ ] **Test 23** : Vérifier la présence du rapport `Rapports/10_Pilotage/DOCTRINE_REPONSE_EXTRAIT_20260724.md`.

- [ ] **Test 24** : Vérifier dans `AUDIT_BIBLIOTHEQUE_LOIS_20260724.md` la preuve de non-perte des données du Sheet (analyse comparative des 71 LEGIARTI et 39 JURITEXT).

- [ ] **Test 25** : Compter le nombre de notes de bas de page contenant une référence "📚 Bibliothèque locale :".  
  *Commande* : `grep -rn "Bibliothèque locale" Actes/Token/ | wc -l` (Résultat attendu : >= 80).
- [ ] **Test 26** : Vérifier qu'aucun lien markdown vers la bibliothèque locale `Lois/` n'est rompu (0 lien mort).  
  *Commande* : Exécution d'un script d'audit des liens locaux sur `Actes/Token/`.
- [ ] **Test 27** : Inspecter une note contenant un lien local dans `TJ_Foix_Conclusions_au_Fond.md` (ex: `Lois/Code/Code_civil/Article_1240...md`).

- [ ] **Test 28** : Vérifier que l'article L113-1 du Code des assurances pointe vers son fichier local dans `Lois/`.

- [ ] **Test 29** : Vérifier que l'article L124-3 du Code des assurances pointe vers son fichier local dans `Lois/`.

- [ ] **Test 30** : Vérifier que l'article L4121-1 du Code du travail pointe vers son fichier local dans `Lois/`.

- [ ] **Test 31** : Vérifier que la structure du dossier `Lois/` contient au moins 150 fichiers.  
  *Commande* : `find Lois/ -name "*.md" | wc -l`
- [ ] **Test 32** : Vérifier que les articles de la loi Badinter (29 et 31 de la loi n° 85-677) sont annotés correctement sans erreur de code rattaché.

- [ ] **Test 33** : Vérifier que les articles L252 et L274 du Livre des procédures fiscales sont maintenus sans faux tag d'erreur.

- [ ] **Test 34** : Vérifier que les articles L725-3 du Code rural sont conservés avec mention de leur statut.

- [ ] **Test 35** : S'assurer que tous les liens d'ancres internes dans les notes (`[^n1]`, etc.) sont équilibrés entre appels et définitions.

---

### E. Résorption du Stock et Conformité des Actes Sortants (Tests 36 à 45)
- [ ] **Test 36** : Vérifier que le fichier `CHIVA_Dossier_Medical_Demande.md` contient bien sa note de bas de page pour l'article L. 1111-7 du CSP.  
  *Commande* : `grep -A 5 "L1111-7" Actes/Token/Courriers/Medical/CHIVA_Dossier_Medical_Demande.md`
- [ ] **Test 37** : Vérifier que le fichier `CADA_Saisine_Modele.md` contient bien sa note pour l'article L300-1 du CRPA.

- [ ] **Test 38** : Vérifier l'équilibre des notes dans `TJ_Foix_Refere_Provision_Assignation.md`.

- [ ] **Test 39** : Vérifier l'équilibre des notes dans `TJ_Foix_CPC_145_Requete.md`.

- [ ] **Test 40** : Vérifier l'équilibre des notes dans `DJI_Foix_Partie_Civile_Constitution.md`.

- [ ] **Test 41** : Exécuter l'audit de cohérence globale inter-documents `.dev/app/check_consistency.py`.  
  *Commande* : `python3 .dev/app/check_consistency.py` (Doit afficher "Rien à signaler — tout est cohérent.").
- [ ] **Test 42** : Vérifier l'absence d'erreurs de syntaxe dans tous les scripts Python sous `.dev/app/`.  
  *Commande* : `python3 -m py_compile .dev/app/*.py`
- [ ] **Test 43** : Vérifier que la génération des versions réelles fonctionne sans avertissement.  
  *Commande* : `python3 .dev/app/generate_real_versions.py`
- [ ] **Test 44** : Compter le nombre de fichiers réels générés dans `Actes/Reel/` (Résultat attendu : 138 fichiers).  
  *Commande* : `find Actes/Reel/ -name "*.md" | wc -l`
- [ ] **Test 45** : Vérifier qu'aucune donnée anonymisée (`[TOKEN_...]`) ne fuite de manière inattendue dans `Actes/Reel/`.

---

### F. Gouvernance et Respect des Règles Générales (Tests 46 à 50)
- [ ] **Test 46** : Vérifier que la profession de la victime dans tous les actes récents est strictly **informaticien indépendant** (SIREN 500 474 457) conformément à la Règle #27.  
  *Commande* : `grep -ri "guitariste" Actes/` (Résultat attendu : 0 occurrence).
- [ ] **Test 47** : Vérifier qu'aucun chemin absolu local (ex: `/home/crilocom/...`) n'est utilisé dans les liens markdown conformément à la Règle #15.  
  *Commande* : `python3 .dev/app/audit_internal_links.py`
- [ ] **Test 48** : Vérifier que les listes à puces respectent le format loose (Règle #24).  
  *Commande* : `python3 .dev/app/normalize_list_spacing.py`
- [ ] **Test 49** : Vérifier que le fichier `AGENTS.md` à la racine est à jour et contient toutes les règles de gouvernance.

- [ ] **Test 50** : Vérifier que le fichier `README.md` principal reflète la structure exacte du dépôt.

---

## DIRECTIVES POUR L'AGENT TIERS ("BLANC")

Lorsqu'un agent tiers exécutera ce cahier de 50 tests :
1. Il doit cloner/ouvrir le dépôt `criloOcom/accident-main` au commit `ddf7b187`.

2. Il doit exécuter la liste des commandes fournies et consigner les résultats dans une grille d'audit `[PASS / FAIL]`.

3. Il pourra ainsi confirmer de manière totalement objective et autonome que l'ensemble du travail commandé a été exécuté sur le code et les documents réels, sans aucune hallucination.
