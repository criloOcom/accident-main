# RÈGLES PERMANENTES — Dossier Accident de la Main

## VÉRIFICATION API AVANT INTÉGRATION
- TOUTE nouvelle citation juridique (LEGIARTI, JURITEXT, n° pourvoi) DOIT être vérifiée via MCP Légifrance/Judilibre AVANT intégration
- Le checker exécute désormais cette vérification automatiquement
- Ne JAMAIS contourner cette règle — une jurisprudence fabriquée invalide tout le dossier

## VÉRIFICATION JURITEXT — PROTOCOLE STRICT (Règle n°10)
- **Lire** `/home/crilocom/accident-main/memory/JURITEXT_PROTOCOL.md` avant toute insertion/modification de JURITEXT
- **Vérification en 2 étapes OBLIGATOIRE** : `legifrance-prod_rechercher_jurisprudence` PUIS `openlegi_rechercher_jurisprudence_judiciaire` — les 2 doivent concorder
- **JAMAIS deviner** un JURITEXT — si introuvable, marquer "À VÉRIFIER" et signaler
- **JAMAIS se fier** à une coche "✓" dans un fichier — la coche ne prouve rien
- **Propagation** : si une JURITEXT est fausse, chercher et corriger TOUTES les occurrences dans le projet
- **Anti-pattern** : "Judilibre retourne 0, donc l'ID est probablement correct" → FAUX, utiliser Légifrance-prod

## #0 — RÉPERTOIRE SOUVERAIN LOCAL
- Le répertoire de travail local est et restera toujours **`/home/crilocom/accident-main/`**.
- Aucun agent, quel qu'il soit, ne peut travailler ailleurs. Aucune exception.
- La création de clones parallèles (tmp, backup, clonage dans `/tmp/opencode/`) est **interdite**.
- Toute opération git (pull, add, commit, push) se fait exclusivement depuis ce dossier.

## #1 — INTERDICTION DE POSER DES QUESTIONS AU CONDITIONNEL
- Tu ne demandes JAMAIS « est-ce que c'est déjà fait ? » ou « est-ce que je le fais ? ».
- Si l'information existe dans les fichiers, tu la lis et tu décides.
- Si une action est possible, tu l'exécutes, pas la demandes.
- La question à l'humain est le dernier recours quand l'information n'existe nulle part.

## PRIORITÉ MCP — Toujours utiliser les outils MCP en premier
- Tout appel à Légifrance, Judilibre ou Google Docs DOIT passer par les outils MCP dédiés
- Ne JAMAIS utiliser webfetch, curl, HTTP requests ou scraping direct sur ces services (bloqués 403/anti-bot)
- Si un MCP crash (erreur d'import, timeout), le FIXER et RELANCER le serveur immédiatement — ne pas dériver vers des solutions alternatives sans MCP
- Les MCP sont gérés par le runtime opencode ; le fix du code source + redémarrage du processus est la seule procédure valide

## PROTOCOLE DE VACCINATION (OBLIGATOIRE — À FAIRE EN TOUT PREMIER)
- 🔴 **Lire et appliquer** `/home/crilocom/accident-main/memory/VACCIN.md` avant la
  moindre action — c'est le protocole de vaccination contre la médiocrité
- **Checklist VACCIN** : analyser 3 exemples existants avant d'en créer un
  nouveau, remplir TOUTES les colonnes, vérifier avec MCP avant de citer
- **Ne JAMAIS** livrer un travail partiellement complété (colonnes vides,
  champs absents, format incohérent avec l'existant)

## PROTOCOLE DE MÉMOIRE (OBLIGATOIRE EN DÉBUT DE SESSION)
- **Lire** `/home/crilocom/accident-main/AGENTS.md` en premier
- **Lire** TOUS les fichiers de `/home/crilocom/accident-main/memory/` avant toute action
- **Vérifier** que le STATUS.md est à jour ; si non, le corriger
- **Ne JAMAIS** poser à l'utilisateur une question dont la réponse existe déjà dans les fichiers mémoire ou le Drive

## INTERDICTIONS ABSOLUES
- **INTERDIT** toute automatisation par script sur les Google Docs (str.replace, re.sub, regex direct)
- **INTERDIT** `deleteContentRange` + `insertText` pour réécrire un doc (détruit formatage)
- **INTERDIT** d'insérer des fichiers .md, .txt dans le Drive (sauf ARCHIVES)
- **INTERDIT** d'inclure les annexes de correspondance (jeton ↔ identité réelle) dans les copies UNIFIE_ANONYME
- **INTERDIT** d'utiliser des numéros de pièce (Pièce n°X) sans validation explicite de l'utilisateur. Ce qui identifie une pièce est le triplet **(date, émetteur, objet)** — pas un numéro. Les colonnes N° du spreadsheet sont provisoires, non validées, et ne doivent pas être citées dans les documents ni dans PIECES MAP.md.

## MÉTHODE AUTORISÉE POUR L'ANONYMIZATION
1. `readDocument` → copier le texte localement dans `/tmp/`
2. Exécuter `batch_anonymize.py` local → fichier anonymisé
3. Vérifier manuellement les noms résiduels (prénoms seuls, casse mixte)
4. Convertir en markdown structuré (titre #, sections ##, listes)
5. `replaceDocumentWithMarkdown` sur la copie UNIFIE_ANONYME
6. `applyParagraphStyle` → JUSTIFIED sur tout le document

## RÈGLES D'ANONYMIZATION
- Personnes physiques/morales → jetons en bon français avec articles (`**[La Victime]**`, `**[L'Exploitant du Commerce (La SAS)]**`)
- Toute donnée localisante (adresse, ville, email, SIREN, CPAM, PV police) → token descriptif en bon français
- Pas de `[ ... ]` générique (sauf pour cacher des références procédurales)
- Pas de civilité devant un token (supprimer "Monsieur/Madame/Dr" avant les tokens)
- Numéros de département `(31)` `(09)` supprimés
- Le document doit rester lisible en bon français

## INTERDICTION D'INVENTER UN STATUT JURIDIQUE
- **INTERDIT** d'affirmer un statut juridique (liquidation, dissolution, radiation, cessation d'activité) d'une entreprise sans source vérifiable (KBIS, extrait RCS, INPI, décision de justice)
- Si le statut est inconnu, le formuler comme une incertitude : "À ce jour, le statut exact de **[l'entreprise]** demeure incertain"
- Ne pas extrapoler l'absence de réponse à un courrier comme une preuve de liquidation

## SÉPARATION STRICTE TOKENS ↔ CORRESPONDANCE RÉELLE
- **Tout document de travail** (actes/, analyses, courriers en rédaction) est rédigé exclusivement en tokens anonymes (`**[La Victime]**`, `**[L'Exploitant du Commerce (La SAS)]**`, etc.)
- **Un dossier de correspondance réelle séparé** est créé au moment de l'envoi uniquement, par substitution des tokens → identités réelles
- **Ne JAMAIS** mélanger tokens et identités réelles dans un même fichier
- **Ne JAMAIS** créer de document « mixte » — soit 100% tokens, soit 100% réél
- **Objectif** : permettre aux agents IA de travailler sur la structure du dossier sans exposer les données personnelles, et garder un seul point de vérité pour le mapping (TOKEN MAP.md)
- Ce comportement est **permanent et non négociable** pour tout le cycle de vie du dossier

## VÉRIFICATION OBLIGATOIRE AVANT FINALISATION (DOUBLE-PASS)
- Avant de finaliser l'écriture de tout document, extraire toutes les dates, montants et identifiants
- Comparer UN PAR UN avec le fichier `memory/STRICT VARIABLES.md`
- Si une seule donnée diffère, CORRIGER le document avant de le présenter
- Ne JAMAIS inventer une date, un montant ou un identifiant — utiliser uniquement les valeurs de STRICT VARIABLES.md

## ANTI-RÉGRESSION — VÉRIFICATION CROSS-DOCUMENT OBLIGATOIRE
- Après TOUTE modification d'un fichier dans `actes/`, `memory/`, ou `annexes/`, lancer impérativement : `python3 app/check_consistency.py`
- Ce script vérifie : liens internes valides, tokens connus, LEGIARTI/JURITEXT joignables, frontmatter cohérent
- Ne JAMAIS commit/push sans vérification préalable — une régression (lien mort, token inconnu, donnée contradictoire) invalide tout le dossier
- Les fichiers `actes/archives/STRATEGIE_Contentieux_Civil.md` et `actes/archives/STRATEGIE_Contentieux_Penal.md` sont les portes d'entrée — leur mise à jour est prioritaire

## STRUCTURE DES DOCUMENTS UNIFIE_ANONYME (voir aussi DESIGN.md)
- Titre du document en TITLE (20pt, CENTER, BOLD — PAS le 36pt par défaut)
- Sections principales en HEADING_1 (14pt, MAJUSCULES, BOLD, souligné)
- Sous-sections en HEADING_2 (12pt, 1ère CAP only, BOLD, souligné)
- Sous-sous-sections en HEADING_3 (10pt, BOLD)
- Paragraphes en NORMAL_TEXT (11pt, JUSTIFIED)
- Police : **Arial exclusivement** sur tout le document
- **NE PAS inclure** d'annexes avec correspondance des acteurs
- Si des références légales sont citées, les lier via applyTextStyle + linkUrl
- Tokens d'anonymisation en **bold** dans le body
- Se référer à `memory/DESIGN.md` pour le détail complet de la charte

## #13 — NOTEBOOKLM MCP — SOURCE DE CONTEXTE PROJET
- **NotebookLM** est une source de contexte supplémentaire : les sources du projet sont chargées dans le notebook `accident-main`
- Tout agent doit utiliser `notebooklm_ask_question(notebook_id="accident-main")` pour obtenir des réponses contextuelles ancrées dans ces sources
- Le `session_id` retourné doit être conservé et réutilisé pour les questions de suivi (conversation contextuelle)
- **Ne pas utiliser NotebookLM comme unique source de vérité** juridique — les vérifications JURITEXT/LEGIARTI via Légifrance/Judilibre restent obligatoires (Règle #10)
- NotebookLM complète la recherche juridique existante : il peut synthétiser et recouper les sources du projet
- Voir la section dédiée dans `AGENTS.md` pour les détails de configuration

## #12 — CYCLE DE VIE DES SESSIONS JULES — RÈGLE ABSOLUE
- **TOUTE session Jules doit être conclue par un message de clôture** explicite (pas seulement abandonnée).
- Une session qui a terminé son travail (rapport reçu, PR créé, mission accomplie) reçoit un message de type : « Mission terminée, tu peux archiver cette session. » ou « Rapport reçu, tu peux clôturer. »
- Une session bloquée qui a reçu une réponse de déblocage doit être informée que la réponse a été envoyée.
- **NE JAMAIS laisser une session Jules en plan** sans message de conclusion — cela laisse des agents en attente indéfiniment et pollue la file d'exécution.
- L'API REST Jules ne dispose pas de méthode `delete` ou `archive` — l'envoi d'un message de clôture est le SEUL moyen de marquer proprement la fin d'une session.
- Ce message de clôture est le signal pour l'agent que son travail est terminé et accepté ; Google archivera automatiquement les sessions clôturées côté serveur.
