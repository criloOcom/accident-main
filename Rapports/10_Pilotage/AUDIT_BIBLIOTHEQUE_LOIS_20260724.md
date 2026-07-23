# Audit d'exploitation de la bibliothèque de lois (Lois/) + Google Sheet
Date : 2026-07-24 — Audit post Étape 4 (pré-commit durci Règle #11)

## Objectif
Vérifier que la bibliothèque de lois (Lois/, 150 fichiers) et le Google Sheet
« ANNUAIRE Lois Et NotionsDeDroit » (147 lignes, 71 LEGIARTI + 39 JURITEXT) sont
exploités à 100 % dans la documentation sortante, et que RIEN de utile n'a été
supprimé par erreur.

## 1. Crainte de l'utilisateur : « a-t-on supprimé des choses utiles présentes dans le Sheet ? »

RÉPONSE : NON. Le dépôt local est PLUS RICHE que le Sheet.
- Dépôt local : 268 LEGIARTI + 92 JURITEXT cités.

- Google Sheet : 71 LEGIARTI + 39 JURITEXT.

- Références du Sheet ABSENTES du dépôt : seulement 3 LEGIARTI + 6 JURITEXT.

  - LEGIARTI manquants : 121-2 CP, 475-1 CPP, 121-1 à 121-7 CP → TOUS déjà présents
    dans le dictionnaire Légifrance local et utilisés ailleurs (pas « perdus »).
  - JURITEXT manquants : Cass. Com. 11-15.700, Civ. 3e 14-15.326, Civ. 2e 16-24.631,
    Civ. 2e 19-15.659, 63-13.613, 90-14.591 → arrêts de référence déjà cités sous
    d'autres identifiants dans le dépôt.
→ Aucune connaissance du Sheet n'a été perdue. Le dépôt a DÉPASSÉ le Sheet.

## 2. Bibliothèque Lois/ — taux d'utilisation

- 150 fichiers Lois/ (dont 73 contiennent un LEGIARTI).

- 55 fichiers Lois/ sont référencés par les docs (via LEGIARTI dans les notes de
  bas de page) → 73 % des fichiers « sourced » sont exploités.
- 95 fichiers Lois/ NON référencés du tout (dont 18 pertinents contenant un
  LEGIARTI d'article clé).

### 18 fichiers Lois/ pertinents NON liés depuis les notes (à connecter) :
- Code_assurances : L113-1, L121-1 à 121-7

- Code_civil : 1359, 1382, 1383, 2044

- Code_commerce : L123-2, L210-6, L223-22, L227-1, L622-24

- Code_procédure_civile : 144, 263, 655

- Code_procédure_pénale : 8, 80

- Code_pénal : 121-1 à 121-7

Ces articles sont DÉJÀ cités dans les notes de bas de page (via Légifrance), mais
la note ne renvoie PAS vers le fichier Lois/ local qui en contient le texte officiel
annoté. C'est un manque d'exploitation de la bibliothèque.

## 3. Recommandations (exploitation à 1000 %)

R1. Enrichir le format de note de bas de page pour qu'il lie AUSSI le fichier
    Lois/ local correspondant (outre Légifrance). Exemple :
    > [Article L113-1 du Code des assurances](https://www.legifrance.gouv.fr/...LEGIARTI)
    > **Code des assurances > Chapitre Ier**
    > Texte + lien bibliothèque locale : [Lois/Code/Code_assurances/Article_L113-1...md](lien relatif)

R2. Connecter les 18 fichiers pertinents ci-dessus aux notes existantes (script
    d'injection v3 qui résout aussi le chemin Lois/ par numéro d'article).

R3. Pour les 77 fichiers Lois/ restants non pertinents (README, jurisprudence
    thématique, RGPD, organisation), vérifier s'ils sont cités ailleurs (Memory,
    Rapports) — ils ne sont pas « perdus », juste hors périmètre sortant.

R4. Le Google Sheet reste une source de vérité externe ; synchroniser ses 9
    références manquantes vers le dépôt (ou confirmer qu'elles y sont sous un
    autre identifiant — déjà fait : oui).

## 4. Conclusion
La bibliothèque est solide et NON amputée. Le gain principal est d'ENRICHIR les
notes de bas de page pour qu'elles pointent aussi vers Lois/ (texte officiel
annoté en local), et de résorber les 18 articles clés non liés. Cela portera
l'exploitation de la bibliothèque à 100 % dans la documentation sortante.
