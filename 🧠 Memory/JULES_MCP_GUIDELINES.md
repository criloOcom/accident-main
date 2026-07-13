---
title: "Directives et Bonnes Pratiques d'Orchestration avec Google Jules MCP"
description: "Ce document consigne les règles permanentes apprises de la documentation de blog et des retours d'expérience sur la connexion des agents autonomes d'édition au dépôt Git."
type: memory
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › JULES MCP GUIDELINES*
<hr>
<!-- /Breadcrumb -->

# Directives et Bonnes Pratiques d'Orchestration avec Google Jules MCP

Ce document consigne les règles permanentes apprises de la documentation de blog et des retours d'expérience sur la connexion des agents autonomes d'édition au dépôt Git.

---

## 1. Règle absolue de connexion au Dépôt GitHub

Lors de l'appel à l'outil `create_session` de Jules via MCP, les paramètres optionnels suivants sont **OBLIGATOIRES** dans notre environnement de production :
- `repo` : Toujours renseigner `"criloOcom/accident-main"`
- `branch` : Toujours spécifier une branche unique au format `jules/M[Numéro]-[Thématique]`
- `autoPr` : Toujours mettre à `true`

Si ces arguments sont omis, Jules démarre en mode **"repoless"** (sans dépôt), rendant impossible toute édition physique ou soumission de modifications de code dans le projet.

---

## 2. Cycle de vie et gestion des ressources

- **Suivi** : Utiliser `get_session_state` périodiquement pour récupérer le status de la tâche.
- **Clôture** : Envoyer obligatoirement un message explicite de clôture une fois la tâche finie via `send_reply_to_session` afin de libérer les ressources côté serveur.