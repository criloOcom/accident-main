---
uid: ctQaGVEN2
title: "RÈGLES PERMANENTES — Dossier Accident de la Main"
description: "- **INTERDICTION D'INVENTER** : Il est interdit d'inventer des faits, des dates, des montants financiers ou des citations juridiques. Tout fait écrit doit s'appuyer strictement sur les données locales du projet (Memory/STRICT VARIABLES.md ou `🧠_M"
type: memory
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Memory](./README.md)*
<hr>
<!-- /Breadcrumb -->

# RÈGLES PERMANENTES<br>Dossier Accident de la Main

## 🛑 PROTOCOLE ANTI-HALLUCINATION STRICT (ZÉRO INVENTIONS)
- **INTERDICTION D'INVENTER** : Il est interdit d'inventer des faits, des dates, des montants financiers ou des citations juridiques. Tout fait écrit doit s'appuyer strictement sur les données locales du projet ([Memory/STRICT VARIABLES.md](STRICT%20VARIABLES.md) ou [Memory/KNOWLEDGE_GRAPH.json](KNOWLEDGE_GRAPH.json)).

- **LE DOUTE SYSTÉMATIQUE** : Si une information (statut de l'entreprise, décision, nom, date) n'est pas explicitement documentée, l'agent doit indiquer que la donnée est "inconnue en l'état" au lieu de l'extrapoler ou de la deviner.

- **RÈGLE DU DOUBLE-PASS (RELECTURE)** : Avant de finaliser une action ou de proposer un document, l'agent doit relire son propre travail en extrayant individuellement toutes les dates, sommes et citations pour les comparer une par une avec les variables de référence.

## VÉRIFICATION SUR PIÈCES SOURCE AVANT TOUTE RÉDACTION (Règle n°14)
- **RÈGLE ABSOLUE** : Avant de rédiger ou modifier un acte, courrier ou email mentionnant une date, un lieu, un numéro de PV ou une information procédurale, l'agent DOIT retrouver et vérifier l'information sur la pièce source originale dans [Actes/Preuves officielles](../Actes/Preuves%20officielles/README.md)

- **Ne JAMAIS** reproduire une information procédurale (date de plainte, lieu de dépôt, numéro de PV, date de chirurgie) depuis une version antérieure d'un document sans la recouper avec la pièce source

- **Mécanisme concret** : pour chaque donnée factuelle dans le document en rédaction, tracer sa provenance : quelle pièce source, quel drive_id, quel numéro de page

- **Sanction** : une information erronée reproduite sans vérification est une faute professionnelle immédiate

## VÉRIFICATION API AVANT INTÉGRATION
- TOUTE nouvelle citation juridique (LEGIARTI, JURITEXT, n° pourvoi) DOIT être lue et vérifiée via MCP Légifrance (`consulter_article` ou `rechercher_code` via MCP Légifrance) AVANT intégration

- Le checker exécute désormais cette vérification automatiquement

- Ne JAMAIS contourner cette règle — une jurisprudence fabriquée invalide tout le dossier

## VÉRIFICATION JURITEXT — PROTOCOLE STRICT (Règle n°10)
- **Lire** [/home/crilocom/accident-main/Memory/JURITEXT_PROTOCOL.md](/home/crilocom/accident-main/Memory/JURITEXT_PROTOCOL.md) avant toute insertion/modification de JURITEXT

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

- Si une action me permet d'éditer ou de consulter des fichiers de travail, tu l'exécutes de plein droit.

- La question à l'humain est le dernier recours quand l'information n'existe nulle part.

## #29 — PROTOCOLE STRICT DE PERMISSIONS & INTERDICTION DE SUPPRESSION EN MASSE
- **MODIFICATIONS COURANTES** : Pour la consultation de fichiers, la mise à jour, la création ou l'édition de documents de travail en local, tu disposes de plein droit pour exécuter les scripts et commandes nécessaires sans interrompre inutilement l'utilisateur.

- **INTERDICTION STRICTE DE SUPPRESSION EN MASSE ET COMPORTEMENT DESTRUCTEUR** :
  1. Il est **STRICTEMENT INTERDIT** d'exécuter des commandes de suppression en masse (`rm -rf`, nettoyage massif de dossiers, suppression de fichiers importants sur le local ou sur le Google Drive) sans demander **EXPLICITEMENT** une confirmation préalable avec le détail précis des fichiers impactés.
  2. Toute action destructrice sur des données distantes (Google Drive, Google Docs, APIs externes) nécessitant la suppression définitive de ressources doit obligatoirement faire l'objet d'une validation utilisateur explicite.
  3. En cas de doute sur la portée d'une commande de nettoyage ou de suppression, la prudence et le contrôle par l'utilisateur prévalent toujours.

## PRIORITÉ MCP — Toujours utiliser les outils MCP en premier
- Tout appel à Légifrance, Judilibre ou Google Docs DOIT passer par les outils MCP dédiés

- Ne JAMAIS utiliser webfetch, curl, HTTP requests ou scraping direct sur ces services (bloqués 403/anti-bot)

- Si un MCP crash (erreur d'import, timeout), le FIXER et RELANCER le serveur immédiatement — ne pas dériver vers des solutions alternatives sans MCP

- Les MCP sont gérés par le runtime opencode ; le fix du code source + redémarrage du processus est la seule procédure valide

- **Documentation :** Voir [Lois/EXEMPLES_REQUETES_MCP.md](../Lois/EXEMPLES_REQUETES_MCP.md) pour des exemples concrets et testés d'utilisation des MCP Légifrance et Judilibre.

## PROTOCOLE DE VACCINATION (OBLIGATOIRE — À FAIRE EN TOUT PREMIER)
- 🔴 **Lire et appliquer** [/home/crilocom/accident-main/Memory/VACCIN.md](/home/crilocom/accident-main/Memory/VACCIN.md) avant la
  moindre action — c'est le protocole de vaccination contre la médiocrité
- **Checklist VACCIN** : analyser 3 exemples existants avant d'en créer un
  nouveau, remplir TOUTES les colonnes, vérifier avec MCP avant de citer
- **Ne JAMAIS** livrer un travail partiellement complété (colonnes vides,
  champs absents, format incohérent avec l'existant)

## PROTOCOLE DE MÉMOIRE (OBLIGATOIRE EN DÉBUT DE SESSION)
- **Lire** [`AGENTS.md`](../AGENTS.md) en premier

- **Lire** TOUS les fichiers de [/home/crilocom/accident-main/Memory](/home/crilocom/accident-main/Memory/README.md) avant toute action

- **Vérifier** que le STATUS.md est à jour ; si non, le corriger

- **Ne JAMAIS** poser à l'utilisateur une question dont la réponse existe déjà dans les fichiers mémoire ou le Drive

## INTERDICTIONS ABSOLUES

## #28 — INTERDICTION D'ASSOCIER FOIX AU DÉPÔT INITIAL DE PLAINTE
- La plainte initiale du 2 juin 2026 a été déposée auprès du **Service Local de Sécurité Publique de Toulouse Rive Droite** (23 Boulevard de l'Embouchure, 31300 Toulouse), **PAS** au Commissariat de Foix.

- Le dossier a ensuite été transmis pour compétence territoriale au Commissariat de Foix (PV n° 2026/015967).

- Toute mention associant « Commissariat de Foix » au **dépôt initial** de plainte du 2 juin 2026 est une erreur factuelle.

- Cette règle est permanente et non négociable. Voir `STRICT VARIABLES.md` § DEPOT_PLAINTE_LIEU.


- **INTERDIT** toute automatisation par script sur les Google Docs (str.replace, re.sub, regex direct)

- **INTERDIT** `deleteContentRange` + `insertText` pour réécrire un doc (détruit formatage)

- **INTERDIT** d'insérer des fichiers .md, .txt dans le Drive (sauf ARCHIVES)

- **INTERDIT** d'inclure les annexes de correspondance (token ↔ identité réelle) dans les copies UNIFIE_ANONYME

- **INTERDIT** d'utiliser des numéros de pièce (Pièce n°X) sans validation explicite de l'utilisateur. Ce qui identifie une pièce est le triplet **(date, émetteur, objet)** — pas un numéro. Les colonnes N° du spreadsheet sont provisoires, non validées, et ne doivent pas être citées dans les documents ni dans PIECES MAP.md.

## MÉTHODE AUTORISÉE POUR L'ANONYMIZATION
1. `readDocument` → copier le texte localement dans `/tmp/`

2. Exécuter `batch_anonymize.py` local → fichier anonymisé

3. Vérifier manuellement les noms résiduels (prénoms seuls, casse mixte)

4. Convertir en markdown structuré (titre #, sections ##, listes)

5. `replaceDocumentWithMarkdown` sur la copie UNIFIE_ANONYME

6. `applyParagraphStyle` → JUSTIFIED sur tout le document

## RÈGLES D'ANONYMIZATION
- Personnes physiques/morales → tokens en bon français avec articles (`[**[La Victime]**](../Memory/Tokens/token-victime-nom-complet.md)`, `[**[L'Exploitant du Commerce (La SAS)]**](../Memory/Tokens/token-exploitation-raison-sociale.md)`)

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
- **Tout document de travail** (Actes/, analyses, courriers en rédaction) est rédigé exclusivement en tokens anonymes (`[**[La Victime]**](../Memory/Tokens/token-victime-nom-complet.md)`, `[**[L'Exploitant du Commerce (La SAS)]**](../Memory/Tokens/token-exploitation-raison-sociale.md)`, etc.)

- **Un dossier de correspondance réelle séparé** est créé au moment de l'envoi uniquement, par substitution des tokens → identités réelles

- **Ne JAMAIS** mélanger tokens et identités réelles dans un même fichier

- **Ne JAMAIS** créer de document « mixte » — soit 100% tokens, soit 100% réél

- **Objectif** : permettre aux agents IA de travailler sur la structure du dossier sans exposer les données personnelles, et garder un seul point de vérité pour le mapping (TOKEN MAP.md)

- Ce comportement est **permanent et non négociable** pour tout le cycle de vie du dossier

## VÉRIFICATION OBLIGATOIRE AVANT FINALISATION (DOUBLE-PASS)
- Avant de finaliser l'écriture de tout document, extraire toutes les dates, montants et identifiants

- Comparer UN PAR UN avec le fichier [Memory/STRICT VARIABLES.md](STRICT%20VARIABLES.md)

- Si une seule donnée diffère, CORRIGER le document avant de le présenter

- Ne JAMAIS inventer une date, un montant ou un identifiant — utiliser uniquement les valeurs de STRICT VARIABLES.md

## ANTI-RÉGRESSION — VÉRIFICATION CROSS-DOCUMENT OBLIGATOIRE
- Après TOUTE modification d'un fichier dans [Actes](../Actes/README.md), [Memory](README.md), ou `annexes/`, lancer impérativement : `python3 app/check_consistency.py`

- Ce script vérifie : liens internes valides, tokens connus, LEGIARTI/JURITEXT joignables, frontmatter cohérent

- Ne JAMAIS commit/push sans vérification préalable — une régression (lien mort, token inconnu, donnée contradictoire) invalide tout le dossier

- Les fichiers [Actes/Token/Archives/Archive - Stratégie Contentieux Civil.md](../Actes/Token/Archives/Archive%20-%20Strat%C3%A9gie%20Contentieux%20Civil.md) et [Actes/Token/Archives/Archive - Stratégie Contentieux Pénal.md](../Actes/Token/Archives/Archive%20-%20Strat%C3%A9gie%20Contentieux%20P%C3%A9nal.md) sont les portes d'entrée — leur mise à jour est prioritaire

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

- Se référer à [Memory/DESIGN.md](DESIGN.md) pour le détail complet de la charte

## #13 — NOTEBOOKLM MCP — SOURCE DE CONTEXTE PROJET
- **NotebookLM** est une source de contexte supplémentaire : les sources du projet sont chargées dans le notebook `accident-main`

- Tout agent doit utiliser `notebooklm_ask_question(notebook_id="accident-main")` pour obtenir des réponses contextuelles ancrées dans ces sources

- Le `session_id` retourné doit être conservé et réutilisé pour les questions de suivi (conversation contextuelle)

- **Ne pas utiliser NotebookLM comme unique source de vérité** juridique — les vérifications JURITEXT/LEGIARTI via Légifrance/Judilibre restent obligatoires (Règle #10)

- NotebookLM complète la recherche juridique existante : il peut synthétiser et recouper les sources du projet

- Voir la section dédiée dans [`AGENTS.md`](../AGENTS.md) pour les détails de configuration

## AVENANT JURIDIQUE — FIABILISATION DE LA NOMENCLATURE DES STATUTS D'ENVOI (Règle n°15)

### PRINCIPE DE SÉPARATION STRICTE : Document rédigé ≠ Acte expédié

Il est formellement interdit de qualifier un document de « Envoyé » sur le seul fait de sa finalisation technique (statut YAML `final`) ou de sa présence sur le stockage partagé (Google Drive `source: drive`). Un document juridique rédigé ne constitue pas une preuve de notification ou d'expédition.

### MATRICE DE QUALIFICATION D'UN STATUT (applicable à tous les agents)

| Statut déclaré | Conditions matérielles strictes |
|----------------|--------------------------------|
| 🟢 **ENVOYÉ / DÉPOSÉ** | Preuve externe annexée au dossier : numéro de suivi LRAR valide, accusé de réception signé par le destinataire, récépissé de dépôt de greffe, ou confirmation d'email expédié (capture d'écran). |
| 🟡 **PROJET / BROUILLON** | Fichier sans preuve postale/judiciaire, texte comportant des balises non complétées (`[À compléter]`, `[Adresse]`, `[...]`), ou document sur le Drive uniquement. |
| 🟠 **PRÊT POUR ENVOI** | Fichier finalisé (`statut: final`), balises remplies, adresse complète, mais pas encore expédié (aucune preuve LRAR/email). |
| 🔴 **GABARIT** | Modèle type, formulaire Cerfa vierge, ou structure de document non personnalisée, destiné à être rempli puis expédié. |

### JURISPRUDENCE DES CAS LITIGIEUX (classement définitif — vérifié par lecture directe des fichiers)

| N° Document | Statut réel | Raison |
|:-----------:|:-----------:|--------|
| **04** ([Action directe assureur](../Actes/Token/Courriers/%F0%9F%93%9C%20Mises%20en%20demeure/SAS%20-%20Courrier%20Assureur.md)) | 🟡 PROJET | `[A compléter]` dans l'adresse — assureur non identifié. Statut YAML `final` erroné. |
| **05** ([Mise en demeure propriétaire](../Actes/Token/Courriers/%F0%9F%93%9C%20Mises%20en%20demeure/Propri%C3%A9taire%20-%20Courrier.md)) | 🟡 PROJET | `[A compléter]` dans l'adresse. Statut YAML `final` erroné. |
| **06** ([Mise en demeure dirigeants](../Actes/Token/Courriers/%F0%9F%93%9C%20Mises%20en%20demeure/SAS%20-%20Pr%C3%A9sident%20-%20Courrier.md)) | 🟡 PROJET | Adresses complètes mais pas de numéro LRAR ni preuve d'envoi. Statut YAML `final` erroné. |
| **06 V2** ([Relance dirigeants](../Actes/Token/Courriers/%F0%9F%94%84%20Relances/SAS%20-%20Dirigeants%20-%20Courrier%20-%20Relance.md)) | 🟢 ENVOYÉS (échec PND) | 3 LRAR : 87001424863012T (SAS PND), 87001424721856G (retour), 87001424862879J (attente). **Seul fichier avec preuve matérielle.** |
| **07** ([Demande consolidation](../Actes/Token/Courriers/%F0%9F%94%84%20Relances/%E2%9C%89%EF%B8%8F%F0%9F%94%84%20Consolidation.md)) | 🟡 BROUILLON | `[A compléter]` adresse Dr DJERBI. Accident 29/05, état non consolidé (suivi ~1 an). |
| **08** ([Suivi Mairie TAVELLA](../Actes/Token/Courriers/%F0%9F%94%84%20Relances/Mairie%20-%20Tavella%20-%20Courrier%20-%20Relance.md)) | 🟡 BROUILLON | `[Adresse de la Mairie]` non renseigné. |
| **09** ([Inspection Travail](../Actes/Token/Courriers/%F0%9F%9A%A8%20Signalements/DDETS%20-%20Signalement.md)) | 🟡 PROJET | `[A compléter]` adresse DDETS. Texte au conditionnel : « Je me réserve le droit... » |
| **10** ([CPC Doyen TJ](../Actes/Token/Actes_proceduraux/Contentieux_civil/TJ%20Foix%20-%20CPC%20145%20-%20Requ%C3%AAte.md))  | 🟡 PROJET | `[Adresse Tribunal Judiciaire]` non renseigné. |
| **11 à 21** (INPI, URSSAF, Préf., CODAF, SIE, CD09, CPAM, SDIS, FGTI, Police, CPAM) | 🟡 PROJETS | Tous les 11 fichiers ont des `[A compléter]` dans les adresses. Statut YAML `final` erroné. Aucune preuve LRAR ou email dans aucun fichier. |
| **22-24** (Attestations témoins) | 🔴 GABARITS | Modèles Cerfa vierges, à compléter avant transmission. |
| **25-28** (Emails relances) | 🟡 BROUILLONS | Statut YAML `brouillon`, emails des destinataires inconnus. |
| **32** ([Mutualisation SIE/URSSAF](../Actes/Token/Courriers/%F0%9F%93%9D%20Proc%C3%A9dure/SIE%20URSSAF%20-%20Mutualisation%20-%20Courrier.md)) | 🟡 PROJET | Statut YAML `projet`, pas sur Drive. |
| **33** ([Constat huissier 145 CPC](../Actes/Token/Courriers/Archivé/Requ%C3%AAte%20-%20Constat%20Huissier%20Archive.md)) | 🟡 PROJET | Statut YAML `projet`, aucun huissier contacté. |
| **34** ([Email Maire Foix Police](../Actes/Token/Courriers/%F0%9F%93%9D%20Proc%C3%A9dure/Mairie%20-%20ERP%20Tavella%20-%20Courrier.md)) | 🟠 PRÊT POUR ENVOI | Fichier finalisé, envoi prévu le 11/07/2026 8h00. |

### CONSIGNES D'AUDIT POUR LES AGENTS

1. **Interdiction de l'alignement aveugle** : Ne jamais valider le statut d'une pièce en se basant uniquement sur un fichier déclaratif ([`STATUS.md`](STATUS.md), [`TODO.md`](TODO.md)). Seule l'existence d'une preuve matérielle d'expédition fait foi (numéro LRAR, AR signé, preuve de dépôt en greffe, email expédié).

2. **Exigence de complétude** : Tout fichier portant le statut YAML `final` mais dont le corps comporte des crochets non résolus (`[À compléter]`, `[Adresse]`) ou des adresses manquantes doit être rétrogradé au statut 🟡 PROJET/BROUILLON.

3. **Preuve matérielle obligatoire** : Un document est juridiquement « ENVOYÉ » uniquement si le dossier contient :

   - Un numéro de suivi LRAR La Poste valide (format : `870014XXXXXXXXX`)
   - Un accusé de réception signé par le destinataire
   - Un récépissé de dépôt de greffe (TJ, TC, etc.)
   - Une confirmation d'email expédié (capture d'écran ou trace dans les fichiers)
   
   En l'absence de ces preuves, tout document, même finalisé, est considéré comme 🟡 PROJET ou 🟠 PRÊT POUR ENVOI.

4. **Les vrais envois confirmés** (preuves matérielles dans le dossier) :

   - **03** (SAS) : LRAR 87001424863012T
   - **05** (Propriétaire) : AR signé par le bailleur (M. Romain Delrieu)
   - **06** (Dirigeants) : LRAR 87001424721856G + 87001424862879J
   - **06 V2** (Relance) : Preuve dépôt LRAR 870014282662911 + facture Z0132713629
   - **10** (CPC Doyen) : Déposé au TJ Foix

5. **Correction dans STATUS.md** : Les documents 04, 07, 09, 11-16, 17, 18, 19, 20, 21 ne sont pas « Envoyés » mais « Projets/Brouillons » (sauf preuve matérielle à retrouver dans les pièces).

## #12 — SESSIONS JULES — PARAMÈTRES OBLIGATOIRES ET CYCLE DE VIE

### #12.0 — Connexion au dépôt (OBLIGATOIRE)
- Tout appel à `jules_create_session` DOIT impérativement inclure :

  - `repo` : `"criloOcom/accident-main"`
  - `branch` : `"main"` (branche de base existante sur le remote — Jules crée sa propre branche de PR en interne)
  - `autoPr` : `true`
- Sans ces paramètres, Jules démarre en mode "repoless" (sans dépôt) et ne peut ni créer de branche, ni soumettre de PR, ni éditer le code.

- Lire Memory/JULES_MCP_GUIDELINES.md avant tout appel à Jules.

### #12.1 — Clôture de session (RÈGLE ABSOLUE)
- **TOUTE session Jules doit être conclue par un message de clôture** explicite (pas seulement abandonnée).

- Une session qui a terminé son travail (rapport reçu, PR créé, mission accomplie) reçoit un message de type : « Mission terminée, tu peux archiver cette session. » ou « Rapport reçu, tu peux clôturer. »

- Une session bloquée qui a reçu une réponse de déblocage doit être informée que la réponse a été envoyée.

- **NE JAMAIS laisser une session Jules en plan** sans message de conclusion — cela laisse des agents en attente indéfiniment et pollue la file d'exécution.

- L'API REST Jules ne dispose pas de méthode `delete` ou `archive` — l'envoi d'un message de clôture est le SEUL moyen de marquer proprement la fin d'une session.

- Ce message de clôture est le signal pour l'agent que son travail est terminé et accepté ; Google archivera automatiquement les sessions clôturées côté serveur.

## #13 — SYSTÈME DE STATUTS — CONVENTION

Tout fichier `.md` dans Actes DOIT avoir un champ `statut` dans son YAML front matter, ainsi que les champs de cross-reference :

### Champs YAML standardisés

```yaml
---
titre: Mon Document
statut: final           # ← obligatoire
reel_path: ../../Reel/{subdir}/{fichier}.md  # ← dans les fichiers token
token_path: ../../Token/{subdir}/{fichier}.md  # ← dans les fichiers reel
---
```

### Échelle des statuts

| Valeur | Signification |
|--------|---------------|
| `brouillon` | En cours de rédaction, pas prêt pour relecture |
| `projet` | Version projet, en attente de relecture/validation |
| `preparation` | En préparation (checklists, plannings, suivis) |
| `final` | Document finalisé, envoyé, ou prêt à l'emploi |
| `fusionné_dans_01` | Fusionné avec un autre document (préciser lequel) |
| `archive` | Document historique conservé pour référence |

### Dossier /Status/

Le dossier `/Status/` à la racine contient 3 index classés par statut :

| Index | Statuts YAML | Critère |
|-------|-------------|---------|
| [`01_PREPARATION.md`](../Status/01_PREPARATION.md) | `brouillon`, `projet`, `fusionné_dans_01` | En cours |
| [`02_PRET_POUR_ENVOI.md`](../Status/02_PRET_POUR_ENVOI.md) | `final`, `preparation` | Finalisé mais `proof_delivery: null` |
| [`03_ENVOYE.md`](../Status/03_ENVOYE.md) | `envoye` | `proof_delivery` rempli |

### Liens croisés token↔reel

- Dans `Token/` : `reel_path` pointe vers le fichier réel correspondant dans `Reel/`

- Dans `Reel/` : `token_path` pointe vers le fichier tokenisé correspondant dans `Token/`

- Les liens sont des chemins relatifs (fonctionnent depuis GitHub)

- `proof_delivery` : champ YAML optionnel contenant le numéro LRAR/AR/preuve

- Gérés automatiquement par `.dev/app/update_status_system.py` et `.dev/app/update_proof_delivery.py`

## #14 — FORMAT DES FILS D'ARIANE (BREADCRUMBS) — RÈGLE STRICTE

### Format imposé
- Le **front matter YAML est sur la LIGNE 1** du fichier (bloc `--- ... ---`), suivi du fil d'Ariane dans un **commentaire HTML** `<!-- ... -->`, puis le contenu.

- ORDRE CANONIQUE : `---` (YAML) en ligne 1 → fil d'Ariane (commentaire HTML) → titre `#` et contenu.

- Raison : la prévisualisation GitHub des fichiers .md ne rend le YAML comme front matter QUE s'il est en première ligne. Un commentaire HTML devant le YAML empêche GitHub de le parser.

- Le fil d'Ariane utilise `[🏠](../README.md)` (emoji maison comme lien) — PAS le mot "Accueil"

- Exemple :
  ```html
  ---
  title: "..."
  description: "..."
  type: "..."
  ---

  <!-- Breadcrumb -->
  [🏠](../Actes/Token/README.md) › ...
  <!-- /Breadcrumb -->

  # Titre du document
  ```

### Règles
1. **Un seul fil d'Ariane par fichier** — toute duplication est une erreur

2. **Toujours APRÈS le bloc YAML** (ligne 1 = `---`), avant tout titre `#` de contenu

3. **Format commentaire HTML** pour détection facile par script

4. **Généré automatiquement** par `.dev/app/generate_breadcrumbs.py`

5. **Ne JAMAIS ajouter** de breadcrumb à la main — toujours passer par le script

6. **Ne JAMAIS laisser** de scripts .py ni de fichiers orphelins à la racine du projet — tout va dans `.dev/app/`

7. **Ne JAMAIS laisser** de fichiers Rapport*.md à la racine — tout va dans [Rapports](../Rapports/README.md)

8. **Ne JAMAIS laisser** de `__pycache__` ou `.pytest_cache` traîner — supprimer après exécution de scripts

## #15 — INTERDICTION FORMELLE DES LIENS ABSOLUS EN INTERNE

1. **Tout lien interne** (pointant vers un fichier du dépôt) DOIT être un **chemin relatif** — jamais `file://`, jamais `/chemin/absolu/depuis/la/racine`

2. **Seuls les liens externes** (Légifrance, Judilibre, sites web) peuvent être des URL absolues `https://...`

3. **Sanction** : un fichier contenant un lien interne absolu (`file://` ou `/Actes/...`) est considéré comme cassé et doit être corrigé immédiatement

4. **Vérification** : tout script d'audit ou de vérification doit signaler les liens absolus internes comme des erreurs bloquantes

## #16 — PRINCIPE DE PRÉCISION ABSOLUE (RÈGLE PERMANENTE)

- **La précision l'emporte sur la vitesse en toutes circonstances. Aucun compromis.**

- Aucune approximation tolérée : pas de « assez bon », pas de « on verra plus tard », pas de déduction sans source.

- Si une donnée est incertaine → lire la source originale ou marquer explicitement « inconnu en l'état ».

- Le temps nécessaire à l'exactitude est toujours du temps bien investi. La rapidité n'est jamais une excuse pour l'inexactitude.

- Cette règle s'applique à tous les agents, scripts, et processus automatisés du projet.

- Toute proposition de « solution plus rapide mais moins précise » doit être rejetée par principe.

- **Rappel** : l'objectif du dossier est la production de documents juridiques — une erreur peut invalider un acte ou coûter des droits à la victime.

## #17 — LIENS OBLIGATOIRES SUR TOUTE CITATION INTERNE (RÈGLE PERMANENTE)

- **Toute citation d'un dossier ou d'un fichier interne au dépôt DOIT être un lien relatif cliquable** (Markdown `[texte](chemin.md)`), jamais un simple texte entre backticks sans lien.

- **Citation de DOSSIER** : le lien doit pointer vers le `README.md` de ce dossier (ex. [Actes/Token/Actes_proceduraux](../Actes/Token/Actes_proceduraux/README.md) → `[01 Actes procéduraux](../Actes/Token/Actes_proceduraux/README.md)`).

- **Citation de FICHIER** : le lien doit pointer directement vers le fichier (ex. `[RAPPORT_X](Rapports/RAPPORT_X.md)`).

- Le texte du lien doit être lisible (nom du dossier/fichier cité), pas un chemin illisible sauf si le contexte l'exige.

- **Interdiction** : écrire `` `Rapports/RAPPORT_X.md` `` sans le transformer en lien. Idem pour les dossiers.

- **Scripts de référence** :

  - `.dev/app/linkify_citations.py` — transforme automatiquement les citations backtick internes non liées en liens (dossier→README, fichier→fichier). Dry-run par défaut, `--apply` pour écrire.
  - `.dev/app/audit_citation_links.py` — vérifie qu'aucune citation interne n'est laissée en texte brut non lié (signale comme avertissement).
- **Objectif** : la navigation entre tous les fichiers du dépôt doit être totale — aucun fichier ni dossier cité ne doit être inaccessible par un clic. C'est une règle de non-régression qualité : chaque agent intervenant sur le projet doit la respecter.

- **Exception** : les chemins purement illustratifs/historiques pointant vers des cibles inexistantes (ex. anciennes conventions `{token,reel}`) doivent être soit corrigés vers la cible réelle, soit supprimés — jamais laissés comme texte mort non lié sans signalement.
## #18 — PRÉSENTATION : LISTES PRÉFÉRÉES AUX TABLEAUX, MERMAID POUR LA CARTOGRAPHIE (RÈGLE PERMANENTE)

- **Les tableaux Markdown à colonne de numéros (`#`, `N°`, `01`, `02`...) sont INTERDITS pour les listes de fichiers/dossiers/documents.** Ils sont illisibles sur la prévisualisation GitHub (mobile notamment) et la colonne de numéros n'apporte rien à la lecture humaine.

- **Format imposé pour un listing de fichiers** : liste à puces Markdown, une entrée par fichier, sous la forme :
  `- **[Nom lisible](chemin/relatif.md)** — *Fondement* — Résumé court.`
  Le chemin du lien doit être le **vrai nom de fichier** (jamais une URL encodée type `03%20%F0%9F%94%8D%20...md` — toujours décoder via `urllib.parse.unquote`).
- **Les tableaux de DONNÉES** (comparaisons chiffrées, montants, dates croisées) restent autorisés quand ils apportent une valeur de lecture réelle.

- **Cartographie interactive** : tout README de dossier/hub de navigation DOIT inclure un diagramme **Mermaid** (bloc ```` ```mermaid ````) représentant l'arborescence ou les relations des fichiers à lire. Cela donne une vue interactive (cliquable sur GitHub) de « quoi lire ».

- **Scripts de référence** :

  - `.dev/app/convert_tables_to_lists.py` — convertit automatiquement les tableaux de listing en listes à puces (décode les liens URL-encodés). Dry-run par défaut, `--apply` pour écrire, `--path` pour cibler un dossier.
- **Raison** : lisibilité humaine et mobile-first. Les tableaux à numéros cassent la lecture ; les listes et le Mermaid la fluidifient.
## #19 — MINI-CHARTE CITATION JURIDIQUE (RÈGLE PERMANENTE — AJOUTÉE LE 12/07/2026)

- **Règle 19a — Vérification systématique** : toute citation d'un article de loi, code ou jurisprudence DOIT être lue et vérifiée sur Légifrance (`consulter_article` ou `rechercher_code` via MCP Légifrance) (MCP legifrance-prod puis openlegi) AVANT insertion dans un document. Ne JAMAIS citer un article de mémoire.

- **Règle 19b — Citations interdites (blacklist)** :

  - **L.310-1-1-2 Code des assurances** : ne concerne PAS l'affichage RC (porte sur les placements des assureurs). Ne plus jamais l'utiliser pour l'affichage RC. À la place : description factuelle ("aucun affichage de l'assurance RC dans les locaux").
  - **Art. 56-1 CPP** : ne concerne PAS les réquisitions de vidéosurveillance (porte sur les perquisitions chez les avocats). Ne plus jamais l'utiliser pour les vidéos. À la place : demande simple à l'OPJ, ou si besoin Art. 60-1/77-1-1 CPP sous contrôle avocat.
- **Règle 19c — Précision et proportion des citations** :

  - Citer l'article seul suffit (« conformément à l'article L.XXXX-X du Code X »). N'insérer un extrait blockquote que si vraiment utile, et court.
  - Privilégier le positionnement « signalement aux fins de vérification » (faits objectifs + demande) plutôt que l'affirmation accusatoire.
  - L'URL Légifrance est un plus pour le suivi interne, pas une obligation dans le courrier.
- **Règle 19d — Bloc verrouillé** : les 12 articles suivants sont validés comme corrects et peuvent être réutilisés : L.4121-1, L.4321-1, R.4323-58, L.8221-5, R.4121-1, L.8271-1-2 CT ; L.124-3 C. assur. ; L.376-1 CSS ; Art. 40 CPP ; L.311-1 CRPA ; L.123-1 CCH ; Cass. 2e civ. 4 avril 2024 n°22-19.307.

- **Origine** : audit avocat du 12/07/2026 sur le batch J+37 — cf. [`Rapports/PROMPT_AVOCAT_REVUE_J37.md`](../Rapports/90_TODO_Prompts/PROMPT_AVOCAT_REVUE_J37.md) pour le détail complet.

## #21 — CONVENTIONS DE FORMATAGE UNIFIÉES — SÉPARATEURS DE SECTION (RÈGLE PERMANENTE)

- **Tout fichier `.md` du projet** DOIT respecter les conventions définies dans [Memory/CONVENTIONS.md](CONVENTIONS.md) : ordre canonique des éléments, hiérarchie H1–H4, séparateurs `<hr><hr>`, citations, etc.

- **Séparateur de section unique** : `<hr><hr>` — placé **avant** chaque section de premier niveau (tout `##`, ou `###` avec chiffre romain ou mot-clé : EXPOSÉ, PAR CES MOTIFS, PIÈCES JOINTES, etc.), à l'exception de la 1ère section.

- **Interdiction** d'utiliser `---` comme séparateur dans le corps d'un fichier (réservé au YAML front matter). Tout `---` dans le corps DOIT être remplacé par `<hr><hr>`.

- **Interdiction** d'utiliser `<hr>` solitaire — DOIT être `<hr><hr>` partout, sauf dans le commentaire HTML du breadcrumb (détecté automatiquement).

- **Pipeline de normalisation** : après toute modification structurelle d'un fichier `.md`, exécuter :

  1. `python3 .dev/app/normalize_sections.py --apply --token` (Token)
  2. `python3 .dev/app/generate_real_versions.py` (sync Reel)
  3. `python3 .dev/app/normalize_sections.py --apply --reel` (Reel)
  4. `python3 .dev/app/check_consistency.py` (vérification)
- **Script** : `.dev/app/normalize_sections.py` — applique la convention `<hr><hr>` en 3 phases (Phase 1 : `---`→`<hr><hr>`, Phase 2 : séparateur avant chaque section, Phase 3 : `<hr>`→`<hr><hr>` + dédup).

- **Sous-titres `## (Note ...)`** après H1 ne sont PAS traités comme des sections de premier niveau — exclus automatiquement par l'algorithme.

- **Exceptions** : les fichiers `Preuves_officielles/` (231 fichiers sans YAML) sont exclus de toutes les corrections automatiques.

## #20 — LIEN CLIQUABLE GOOGLE DRIVE SUR TOUT `drive_id` (RÈGLE PERMANENTE)

- Tout fichier dont le YAML contient un champ `drive_id: <ID>` DOIT exposer un **lien cliquable** vers la source Google Drive dans son corps (le front matter YAML n'est pas rendu cliquable sur GitHub).

- Format imposé (ligne juste après le bloc YAML, avant le titre `#`) :
  `> 🔗 Source Google Drive : [<ID court>](https://drive.google.com/open?id=<ID>)`
- L'URL absolue `https://drive.google.com/open?id=<ID>` est un lien EXTERNE — elle est autorisée par la Règle #15 (seuls les liens internes doivent être relatifs).

- **Script de référence** : `.dev/app/add_drive_links.py` — ajoute automatiquement le lien cliquable pour tout `drive_id` du YAML ne l'ayant pas encore. Dry-run par défaut, `--apply` pour écrire.

- **Objectif** : ouvrir la pièce source d'un clic depuis la prévisualisation GitHub, sans copier/coller l'ID.

## #23 — PRE-COMMIT HOOK : AUDIT OBLIGATOIRE DES LIENS INTERNES AVANT COMMIT (RÈGLE PERMANENTE)

- **Tout commit** déclenche automatiquement 3 audits via le hook pre-commit versionné dans `.dev/hooks/pre-commit` :

  1. `.dev/app/audit_readme_integrity.py` — vérifie l'intégrité des README.md
  2. `.dev/app/audit_internal_links.py` — vérifie qu'aucun lien `.md`→`.md` n'est cassé
  3. `.dev/app/audit_citation_links.py` — vérifie que toute citation interne est un lien cliquable
- **Exit codes** : `audit_internal_links.py` → 0 = OK, 1 = liens cassés. `audit_readme_integrity.py` → 0 = OK, 1 = erreurs bloquantes, 2 = avertissements non bloquants.

- **Correction assistée** : `.dev/app/fix_internal_links.py` cherche les fichiers cibles dans tout le projet par basename. Cas univoque (1 seul candidat) → correction automatique avec `--apply`. Cas ambigus (2+ candidats) → listés sans choix — l'agent analyse manuellement. Introuvables → signalés comme irrécupérables.

- **Contournement** : `git commit --no-verify` pour forcer le passage malgré les échecs d'audit.

- **Architecture** : le fichier source de vérité est `.dev/hooks/pre-commit` (versionné). `.git/hooks/pre-commit` est un trampoline de 5 lignes qui délègue au premier.

- **Fichiers exclus du scan** : `CONVENTIONS.md`, `VACCIN.md`, `DECISIONS.md`, `DESIGN.md`, `STRICT VARIABLES.md` (contiennent des exemples de liens volontaires).

- **Scripts de référence** : `.dev/app/audit_internal_links.py` (détection), `.dev/app/fix_internal_links.py` (correction), `.dev/hooks/pre-commit` (orchestrateur).

## #22 — VERROUILLAGE STRICTE DE LA STRATE REEL (ARTIFACT GÉNÉRÉ, JAMAIS À LA MAIN)

- **Principe non négociable** : toute création/édition de document se fait UNIQUEMENT en version **Token** (`Actes/Token/...`). Les versions **Reel** (`Actes/Reel/...`) sont des *artifacts* exclusivement produits par `.dev/app/generate_real_versions.py`.

- **INTERDICTION #1** : ne JAMAIS rédiger ni modifier le contenu d'un fichier Reel à la main (sauf si l'on a modifié le script de génération lui-même et qu'on applique sa sortie). Le Reel = sortie canonique du générateur, pas un document éditable.

- **INTERDICTION #2** : ne JAMAIS créer un fichier Reel sans son Token frère et sans que le Token déclare un `reel_path` pointant dessus. Un Reel sans Token = orphelin = interdit.

- **Lors d'un merge de PR** : si une PR contient des fichiers Reel, les traiter comme des build artifacts. Deux options seulement :

  1. les laisser passer s'ils sont strictement cohérents avec le Token + la sortie attendue du générateur actuel ;
  2. sinon, relancer `generate_real_versions.py` et commiter le résultat — mais ne jamais toucher aux Reel « à la main » pour « corriger » du contenu.
- **Régularisation d'un Reel orphelin (présent sur disque mais non tracké)** — procédure obligatoire avant `git add` :

  1. vérifier qu'un Token correspondant existe avec un `reel_path` pointant dessus ;
  2. vérifier la cohérence du contenu (aucune fuite de vraie PII, respect des conventions du projet) ;
  3. seulement après, `git add` + commit en tant que régularisation (jamais comme nouveau document).
- **En cas de doute sur une action touchant la strate Reel** (suppression, création, modification) : s'abstenir et soit ouvrir un TODO documenté dans STATUS.md / `TODO_*.md`, soit demander une validation explicite — jamais deviner.

- **Pipeline canonique après toute modification Token** : `generate_real_versions.py` → `check_consistency.py` (cf. Règle #21). Le Reel doit toujours pouvoir être régénéré à l'identique depuis le Token.

- **Convention de message de commit/log (OBLIGATOIRE)** : dans tout commit ou log touchant la strate Reel, indiquer explicitement la provenance, au format : `Reels régénérés par generate_real_versions.py à partir de [chemin Token], aucun édit manuel.` Aucun message ne doit laisser croire à une édition manuelle du Reel. (Note : le commit `5ab96ca` du 15/07/2026 précède cette convention — il a bien régularisé un Reel généré, sans édit manuel, mais ne portait pas cette mention.)

- **Rappel de maturité du dépôt** : ce dépôt n'est pas un bac à sable. Le dossier accident-main est déjà très avancé (volets pénal, civil, assurance, inspection, Dintilhac, 15 rapports multi-angle, note stratégique, conclusions au fond). Le rôle de l'agent est de faire converger le dépôt, NON de réinventer la manière dont on gère les Reel.

- **INTERDICTION #3 — README d'index dans Reel** : aucun README.md d'index ou de documentation n'est maintenu dans [Actes/Reel](../Actes/Reel/README.md). Les README d'index vivent exclusivement côté `Token/` (source de vérité). Le Reel est un artefact de build, pas un dossier documenté.

## #24 — FORMAT LOOSE DES LISTES À PUCES (RÈGLE PERMANENTE)

- **Principe** : toute liste à puces (`- `, `* `, `- [ ]`, `- [x]`) DOIT être en format **loose**, c'est-à-dire avec **une ligne vide entre chaque item de même niveau d'indentation**.

  ```markdown
  # 🔴 VALIDE (loose)
  - Premier item

  - Second item

  - Troisième item

  # ❌ INVALIDE (tight)
  - Premier item
  - Second item
  - Troisième item
  ```

- **Sous-listes indentées** : la même règle s'applique — chaque sous-item DOIT être séparé du suivant par une ligne vide :

  ```markdown
  - Parent item

    - Sous-item 1

    - Sous-item 2

  - Parent item 2
  ```

- **Script de correction automatique** : `.dev/app/normalize_list_spacing.py --apply` normalise l'ensemble du dépôt (dry-run par défaut, `--apply` pour appliquer).

- **Audit pré-commit** : le hook `.dev/hooks/pre-commit` vérifie la présence de listes tight dans les fichiers modifiés (via `normalize_list_spacing.py --check`) et bloque le commit si des violations sont détectées.

- **Dérogation** : aucune. La règle s'applique à TOUS les fichiers `.md` du projet, sans exception. Les listes de tâches (`[ ]` / `[x]`) sont également concernées.

## #26 — GOOGLE CALENDAR — PIÈCE MAÎTRISE DU PROCESSUS (RÈGLE PERMANENTE)

### Statut
Le calendrier Google partagé (`[AM] Accident Main`) est une **pièce maîtresse du processus** au même titre que les fichiers du dépôt. Tous les événements clés du projet y sont enregistrés avec leurs liens vers les documents Google Drive/Docs associés.

- **ID calendrier** : `b79938b56860c8d121009802e68294f74709483faf8ca0d1c7a23b97c84e7ac5@group.calendar.google.com`

- **URL** : [Voir le calendrier](https://calendar.google.com/calendar/u/0?cid=Yjc5OTM4YjU2ODYwYzhkMTIxMDA5ODAyZTY4Mjk0Zjc0NzA5NDgzZmFmOGNhMGQxYzdhMjNiOTdjODRlN2FjNUBn)

- **Préfixe** : tous les événements sont prefixés `[AM]` (Accident Main)

### Règles

1. **Lecture obligatoire en début de session** : tout agent DOIT consulter le calendrier Google (via `listEvents` avec timeMin approprié) AVANT toute action, au même titre que la lecture de VACCIN.md et STATUS.md.

2. **Mise à jour systématique** : toute création ou modification d'un document fixant une date (courrier, acte, rendez-vous, échéance) DOIT être accompagnée de la création ou mise à jour de l'événement Google Calendar correspondant.

3. **Double lien document↔calendrier** : les événements du calendrier contiennent en description les liens vers les Google Docs/Drive pertinents. Réciproquement, tout document mentionnant une date importante devrait idéalement référencer le calendrier.

4. **Modification de date** : si la date d'un événement change (report d'audience, nouvelle échéance, rendez-vous décalé), l'agent DOIT :

   - Mettre à jour l'événement existant avec `updateEvent` (conserver l'ID pour l'historique)
   - Si l'ancienne date doit rester tracée, ajouter une note dans la description (ex: « Initialement prévu le XX/YY »)

5. **Description structurée** chaque événement DOIT contenir :

   - `[AM]` en tête de résumé
   - Résumé de l'action en description
   - Liens vers les Google Docs/Drive concernés
   - Statut : ✅ Fait / ❌ À FAIRE / 🟡 PROJET / 📅 Date fixe

6. **Pas de suppression sans trace** : ne JAMAIS supprimer un événement sans le remplacer par un événement de mise à jour. Le calendrier est une chronologie — les dates passées restent visibles.

7. **Anti-régression** : après toute modification de date dans les fichiers du dépôt (STRICT VARIABLES.md, STATUS.md, TODO.md, courriers, actes), vérifier si l'événement calendrier correspondant est à jour.

8. **Événements flottants** : les actions sans date fixe (TODO items) doivent être créées comme événements avec une date estimée raisonnable, marquées `❌ À FAIRE`.

## #25 — INTERDICTION DES LIENS MARKDOWN DANS LE YAML (RÈGLE PERMANENTE)

## #27 — VÉRIFICATION DE LA PROFESSION ET DES ACTIVITÉS — INTERDICTION ABSOLUE D'INVENTER (RÈGLE PERMANENTE)

### Principe
- **INTERDICTION ABSOLUE** d'inventer ou d'extrapoler une profession, une activité de loisir, ou un statut professionnel pour la victime ou tout acteur du dossier.

- La profession de la victime est **informaticien indépendant** (auto-entrepreneur, SIREN 500 474 457). Aucune autre profession (guitariste, musicien, artisan, etc.) ne doit être mentionnée.

- Les activités de loisir de la victime sont exclusivement le **codage / développement informatique personnel**. Aucun autre loisir (guitare, bricolage, gaming intensif, sport) ne doit être présenté comme un fait établi sans preuve matérielle dans les pièces source.

### Règle de vérification obligatoire
1. **Avant toute rédaction** mentionnant la profession ou les activités de la victime, l'agent DOIT consulter :

   - Les pièces URSSAF (token-victime-id-professionnel)
   - Le token token-victime-profession (s'il existe)
   - Le fichier [Memory/STRICT VARIABLES.md](STRICT VARIABLES.md)
   - Les pièces source dans `Actes/Preuves_officielles/`

2. **En cas de doute** sur la profession ou une activité : ne pas deviner, ne pas extrapoler. Marquer explicitement `[PROFESSION À VÉRIFIER]` ou `[LOISIR À CONFIRMER SUR PIÈCES]`.

3. **Sanction** : toute mention d'une profession ou activité non vérifiée sur pièce source constitue une **faute professionnelle grave**. L'erreur "guitariste" (6 occurrences sur 4 fichiers) a nécessité une purge complète du dépôt — ne pas reproduire.

### Propagation
Si une profession ou activité erronée est découverte dans un fichier :
1. Chercher TOUTES les occurrences dans le projet (grep sur le terme)

2. Corriger TOUTES les occurrences (Token + Reel)

3. Vérifier les documents Google Drive correspondants

4. Ajouter une règle dans RULES.md pour empêcher la récidive


- **Principe** : le YAML front matter (`---`...`---`) est un format de données, pas un rendu Markdown. Les liens `[texte](url)` sont soit ignorés par le parseur YAML, soit le cassent (les `:` dans les URLs sont ambigus).

- **Interdiction absolue** : aucun lien Markdown `[texte](url)` n'est autorisé dans les blocs YAML (`title`, `description`, ou tout autre champ).

- **Correction** : remplacer `[texte](url)` par le `texte` nu dans le YAML.

- **Script de correction** : `.dev/app/strip_yaml_links.py --apply` (dry-run par défaut).

- **Audit** : `.dev/app/audit_yaml_links.py` — intégré au pre-commit hook (Règle #23).

- **Anti-exemple** (YAML interdit) :
  ```yaml
  ---
  description: Procès-verbal de [La Victime](token.md)  # ❌ lien interdit
  ---
  ```

- **Exemple correct** :
  ```yaml
  ---
  description: Procès-verbal de La Victime  # ✅ texte seul
  ---
  ```

## #29 — FORMATAGE VISUEL DES COURRIERS (LIGNES HORIZONTALES ET BALISES D'ACTEURS) (RÈGLE PERMANENTE)
- **Principe** : Afin de rendre les previews Markdown plus structurées et visuellement confortables pour un lecteur humain, tous les fichiers de type `courrier` doivent suivre une structure stricte de démarcation.

- **Lignes horizontales (`---`) autour de l'Objet** : Placer une ligne horizontale (`---`) immédiatement avant et immédiatement après le bloc contenant l'Objet et le N° LRAR.

- **Balises de commentaires HTML pour l'Auteur, le Destinataire, la Date, les Pièces Jointes et les Sources** :

  - Entourer le bloc adresse de l'expéditeur avec `<!-- Auteur -->` au début et `<!-- /Auteur -->` à la fin.
  - Entourer le bloc adresse du destinataire avec `<!-- Destinataire -->` au début et `<!-- /Destinataire -->` à la fin.
  - Entourer la ligne de date et lieu avec `<!-- Date -->` au début et `<!-- /Date -->` à la fin.
  - Entourer la section Pièces Jointes avec `<!-- PJ -->` (avant `## PIECES JOINTES`) et `<!-- /PJ -->` (à la fin de la liste des PJ).
  - Entourer la section des notes législatives avec `<!-- Source -->` (avant `## Sources Législation`) et `<!-- /Source -->` (à la fin de la liste de sources).

  - **INTERDICTION ABSOLUE** : ne JAMAIS fusionner les blocs Auteur + Destinataire + Date sous un seul `<!-- Auteur -->`. Chaque métadonnée DOIT avoir son propre bloc distinct (`<!-- Auteur -->...<!-- /Auteur -->`, `<!-- Destinataire -->...<!-- /Destinataire -->`, `<!-- Date -->...<!-- /Date -->`), séparés par une ligne vide. Voir CONVENTIONS.md §XIII.

- **Exemple de structure type** :
  ```markdown
  <!-- Auteur -->
  [**[La Victime]**](...)  
  [**[L'Adresse de la Victime]**](../Memory/Tokens/token-victime-adresse.md)  
  [**[L'Email de la Victime]**](../Memory/Tokens/token-victime-email.md)
  <!-- /Auteur -->

  <!-- Destinataire -->
  Monsieur le Directeur  
  GHT des Pyrénées Ariégeoises CHIVA  
  Chemin de la Plaine  
  09000 Saint-Jean-de-Verges
  <!-- /Destinataire -->

  <!-- Date -->
  **[Foix]**, le 18 juillet 2026
  <!-- /Date -->

  ---

  **Objet : Demande de communication...**  
  **N° LRAR : [**[N° LRAR CHIVA]**](...)**

  ---

  Monsieur le Directeur,

  ...

  <!-- PJ -->
  ## PIECES JOINTES

  - **[Certificat médical initial](...)** — Constatation des blessures
  <!-- /PJ -->

  <!-- Source -->
  ## Sources Législation

  [^1]: [Article L. 124-3...](url)
  <!-- /Source -->
  ```

## #30 — GOUVERNANCE YAML FRONTMATTER (RÈGLE PERMANENTE)

- **Principe** : tout fichier `.md` dans le périmètre (`Actes/Token`, `Actes/Reel`, `Lois`, `Memory`, `Rapports`) DOIT avoir un YAML frontmatter valide avec un `type` canonique.

- **Types canoniques** : définis dans `CANONICAL_TYPES` (`yaml_utils.py`). Tout type hors liste est une violation. Voir [CONVENTIONS.md §II](CONVENTIONS.md#ii--yaml-front-matter) pour la liste exhaustive.

- **Champs obligatoires** : `title` (string) et `type` (canonique). Tout fichier sans ces champs est en violation.

- **Champs enrichis recommandés** : `subtitle`, `objective`, `summary`, `key_points`, `recipient`, `jurisdiction`, `legal_basis`, `urgence`, `tags` — voir CONVENTIONS.md §II.

- **`description`** : ne doit PAS contenir `auteur`, `destinataire` ou d'autres métadonnées de rôle. Usage exclusif : description libre du contenu.

- **Quotes YAML** : toute valeur contenant `: ` (deux-points-espace), `#`, `{`, `}`, `[`, `]`, `,`, `&`, `*`, `?`, `|`, `<`, `>`, `!`, `` ` `` DOIT être entre quotes. Privilégier les single quotes `'...'` (doubler les apostrophes : `'L''exemple'`).

- **Validation** : `.dev/app/yaml_validator.py` vérifie automatiquement types, statuts, dates, et liens cassés. Intégré au pre-commit hook.

- **Schéma JSON** : `.dev/app/yaml_schema.json` décrit la structure complète. Utilisable par les IDE pour l'autocomplétion.

- **Sanctions** : toute modification qui introduit une violation YAML sera bloquée par le pre-commit hook. Pour passer outre : `git commit --no-verify` (déconseillé).

## #31 — NORMES DE SECRÉTARIAT ET DE TYPOGRAPHIE GOOGLE DOCS (RÈGLE PERMANENTE)

- **Taille des titres de section majeurs** : La taille de police des titres majeurs est fixée à **16 pt** (en **gras**). Il est formellement interdit d'utiliser des polices démesurées (comme 26 pt ou plus).
- **Aération et sauts de ligne d'en-tête (Shift+Entrée / Line Breaks)** :
  1. Au sein d'un même bloc (Expéditeur, Destinataire), utiliser des **retours à la ligne simples / sauts de ligne doux (Shift+Entrée)** (2 espaces en fin de ligne en Markdown) afin que le bloc conserve un interlignage compact d'adresse.
  2. Entre les différents blocs distincts (Expéditeur, Destinataire, Date, Objet), séparer par des sauts de paragraphe/ligne nets (`&nbsp;` en Markdown).
- **Couleurs d'hyperliens par défaut** : Ne JAMAIS forcer de couleur personnalisée (ex. bleu forcé) sur les hyperliens. Laisser la couleur par défaut de Google Docs s'appliquer automatiquement lors de la création d'un lien.
- **Notes de bas de page natives** : Utiliser exclusivement la fonctionnalité native de notes de bas de page de Google Docs (`createFootnote` avec segment dédié), et ne jamais créer de sections factices "Sources" en simple texte en bas de document.
- **Hyperliens de pièces officielles (ex. N° PV Police)** : Lors de la conversion de tokens de preuves officielles (ex. `[N° PV Police]` $\rightarrow$ `2026/015967`), la valeur réelle citée dans le corps du texte DOIT être transformée en **hyperlien cliquable en Bleu Lien Google + Gras + Souligné** pointant vers la pièce officielle hébergée sur Google Drive (ex. `1YXaJE81FFPTKcrcShg9DI5jUZ82T988V`).
- **Conservation stricte des mots en gras issus du Markdown** : Les passages mis en gras dans le document Markdown source (notamment les intitulés ou débuts d'éléments de listes à puces ou numérotées, ex. `1. **Le rapport...**`) DOIVENT impérativement être restitués en **GRAS** dans le Google Doc final.
- **Formatage des Listes à Puces et Numérotées NATIVES** : Il est formellement INTERDIT de simuler des puces par du texte brut (ex. écrire `1. Le rapport...` ou `- Si l'inspection...` en début de paragraphe). Chaque liste du Markdown doit être convertie via la commande API Google Docs `createParagraphBullets` :
  - **Listes numérotées** (`1.`, `2.`, `3.`) $\rightarrow$ `bulletPreset: NUMBERED_DECIMAL_ALPHA_ROMAN`
  - **Listes à puces** (`- `) $\rightarrow$ `bulletPreset: BULLET_DISC_CIRCLE_SQUARE` (ou `BULLET_ARROW_DIAMOND_DISC`)
- **Ligne d'adresse postale unique dans les en-têtes** : Dans les blocs d'en-tête Expéditeur et Destinataire, la rue et la ville/CP (ex. `10 Avenue de Purpan, 31700 Blagnac` ou `45 Cours Gabriel Fauré, 09000 Foix`) DOIVENT figurer sur une **seule et même ligne** (séparées par une virgule), afin de maintenir une présentation compacte et harmonieuse.
- **Restitution NATIVE des séparateurs `<hr>` (Bordures de paragraphe)** : Il est strictement INTERDIT de simuler des lignes de séparation avec du texte (ex. suites de tirets `───`). Dans l'API Google Docs, les balises `<hr>` entourant des blocs (ex. Objet / Ref) DOIVENT être générées avec les propriétés natives de bordure de paragraphe `borderTop` et `borderBottom` (`updateParagraphStyle` avec `dashStyle: SOLID`, `width: 1PT`), qui tracent des lignes horizontales d'en-tête natifs parfaites et propres sans bricolage textuel.
- **Conformité multi-agents** : Cette norme de secrétariat me et est obligatoire pour tout agent intervenant sur le dossier.