# RÈGLES PERMANENTES — Dossier Accident de la Main

## PRIORITÉ MCP — Toujours utiliser les outils MCP en premier
- Tout appel à Légifrance, Judilibre ou Google Docs DOIT passer par les outils MCP dédiés
- Ne JAMAIS utiliser webfetch, curl, HTTP requests ou scraping direct sur ces services (bloqués 403/anti-bot)
- Si un MCP crash (erreur d'import, timeout), le FIXER et RELANCER le serveur immédiatement — ne pas dériver vers des solutions alternatives sans MCP
- Les MCP sont gérés par le runtime opencode ; le fix du code source + redémarrage du processus est la seule procédure valide

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
- **INTERDIT** d'utiliser des numéros de pièce (Pièce n°X) sans validation explicite de l'utilisateur. Ce qui identifie une pièce est le triplet **(date, émetteur, objet)** — pas un numéro. Les colonnes N° du spreadsheet sont provisoires, non validées, et ne doivent pas être citées dans les documents ni dans PIECES_MAP.md.

## MÉTHODE AUTORISÉE POUR L'ANONYMIZATION
1. `readDocument` → copier le texte localement dans `/tmp/`
2. Exécuter `batch_anonymize.py` local → fichier anonymisé
3. Vérifier manuellement les noms résiduels (prénoms seuls, casse mixte)
4. Convertir en markdown structuré (titre #, sections ##, listes)
5. `replaceDocumentWithMarkdown` sur la copie UNIFIE_ANONYME
6. `applyParagraphStyle` → JUSTIFIED sur tout le document

## RÈGLES D'ANONYMIZATION
- Personnes physiques/morales → jetons en bon français avec articles (`[La Victime]`, `[L'Exploitant du Commerce]`)
- Toute donnée localisante (adresse, ville, email, SIREN, CPAM, PV police) → token descriptif en bon français
- Pas de `[ ... ]` générique (sauf pour cacher des références procédurales)
- Pas de civilité devant un token (supprimer "Monsieur/Madame/Dr" avant les tokens)
- Numéros de département `(31)` `(09)` supprimés
- Le document doit rester lisible en bon français

## INTERDICTION D'INVENTER UN STATUT JURIDIQUE
- **INTERDIT** d'affirmer un statut juridique (liquidation, dissolution, radiation, cessation d'activité) d'une entreprise sans source vérifiable (KBIS, extrait RCS, INPI, décision de justice)
- Si le statut est inconnu, le formuler comme une incertitude : "À ce jour, le statut exact de [l'entreprise] demeure incertain"
- Ne pas extrapoler l'absence de réponse à un courrier comme une preuve de liquidation

## VÉRIFICATION OBLIGATOIRE AVANT FINALISATION (DOUBLE-PASS)
- Avant de finaliser l'écriture de tout document, extraire toutes les dates, montants et identifiants
- Comparer UN PAR UN avec le fichier `memory/STRICT_VARIABLES.md`
- Si une seule donnée diffère, CORRIGER le document avant de le présenter
- Ne JAMAIS inventer une date, un montant ou un identifiant — utiliser uniquement les valeurs de STRICT_VARIABLES.md

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
