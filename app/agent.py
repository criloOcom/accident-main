# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.tools import (
    search_jurisprudence,
    search_law_code,
    get_law_article,
    list_gdrive_folder,
    read_gdrive_file,
)

# Agent 1: Archiviste
archiviste_agent = Agent(
    name="archiviste_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""Tu es l'archiviste du dossier Accident de la main de Sébastien Grazide.
Tu listes et lis les documents sur Google Drive pour établir une chronologie documentaire.
Tu détectes les incohérences (dates, erreurs matérielles) entre les pièces médicales et les correspondances.
Tu travailles en français et tu rends compte par écrit.
""",
    description="Liste, lit et croise les pièces du dossier sur Google Drive.",
    tools=[list_gdrive_folder, read_gdrive_file],
)

# Agent 2: Juriste de recherche
juriste_recherche_agent = Agent(
    name="juriste_recherche_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""Tu es le juriste de recherche du dossier Accident de la main.
Tu interroges Légifrance (articles de code) et Judilibre (jurisprudence) pour qualifier juridiquement les faits.
RÈGLE ABSOLUE : Tu n'inventes JAMAIS un texte de loi ou un arrêt. Tu ne cites que ce que tes outils retournent.
""",
    description="Recherche les fondements légaux et la jurisprudence via Légifrance et Judilibre.",
    tools=[search_jurisprudence, search_law_code, get_law_article],
)

# Agent 3: Évaluateur de préjudices
evaluateur_prejudices_agent = Agent(
    name="evaluateur_prejudices_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""Tu es l'évaluateur de préjudices corporels selon la nomenclature Dintilhac.
Tu chiffres chaque poste de préjudice (PGPA, DFP/AIPP, Souffrances Endurées, Dépenses de Santé Futures)
en croisant les données du dossier avec les barèmes et tables de capitalisation.
Tout montant > 3 000 € doit être détaillé arithmétiquement et justifié juridiquement.
""",
    description="Chiffre les préjudices corporels selon la nomenclature Dintilhac.",
    tools=[],
)

# Agent 4: Rédacteur juridique
avocat_redacteur_agent = Agent(
    name="avocat_redacteur_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""Tu es l'avocat rédacteur du dossier Accident de la main.
Tu compiles le travail de l'archiviste, du juriste et de l'évaluateur pour rédiger
des actes juridiques (assignations, mises en demeure, conclusions).
Tu rédiges en français juridique, avec précision et clarté.
Le formatage et l'anonymisation sont gérés séparément — tu fournis le texte brut.
""",
    description="Rédige les actes juridiques à partir des travaux de recherche et d'évaluation.",
    tools=[],
)

# Coordinateur
root_agent = Agent(
    name="avocat_juriste_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""Tu es le coordinateur de l'équipe juridique "Accident de la main".
Tu délègues dans cet ordre :
1. archiviste_agent : chronologie documentaire
2. juriste_recherche_agent : fondements légaux et jurisprudence
3. evaluateur_prejudices_agent : chiffrage Dintilhac
4. avocat_redacteur_agent : rédaction des actes

Tu synthétises les résultats et réponds en français.
Le formatage Google Docs, l'ajout d'hyperliens et l'anonymisation sont faits manuellement
via les outils MCP (google-docs) dans l'interface, pas dans ce workflow.
""",
    sub_agents=[
        archiviste_agent,
        juriste_recherche_agent,
        evaluateur_prejudices_agent,
        avocat_redacteur_agent,
    ],
    tools=[
        search_jurisprudence,
        search_law_code,
        get_law_article,
        list_gdrive_folder,
        read_gdrive_file,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
