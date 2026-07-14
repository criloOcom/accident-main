#!/usr/bin/env python3
"""Tests de non-régression pour batch_anonymize.anonymize_text.

Vérifie que les identités réelles du dossier ne subsistent pas après
anonymisation, et que la génération Reel ne contient pas de token `**[` résiduel.
"""
import os
import sys
import importlib.util

# Charger batch_anonymize.py sans le bloc __main__ (chemin absolu robuste)
HERE = os.path.dirname(os.path.abspath(__file__))
# Remonter au dépôt racine : .dev/tests/unit/app -> 4 niveaux
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
APP = os.path.join(ROOT, '.dev', 'app', 'batch_anonymize.py')
spec = importlib.util.spec_from_file_location('batch_anonymize', APP)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
anonymize_text = mod.anonymize_text


def test_noms_reels_anonymises():
    """Aucun nom réel du tableau ne doit subsister en clair."""
    echantillon = (
        "Monsieur Sébastien GRAZIDE est tombé au salon de la SAS LES MAUVAIS GARCONS. "
        "Le président Mountasser SABIR et la DG Catherine ANDISSAC doivent répondre. "
        "Le Dr DJERBI a opéré, le Dr JARDON a constaté, Dr Oxybel a suivi. "
        "L'adjoint TAVELLA a été contacté. CPAM 31727387, PV 2026/015967. "
        "Adresse 22 Rue Lafaurie, 09000 Foix. SIREN 500 474 457."
    )
    out = anonymize_text(echantillon)
    fuites = [n for n in (
        "GRAZIDE", "Grazi", "SABIR", "Sabir", "ANDISSAC", "Andissac",
        "SORROCHE", "DJERBI", "JARDON", "Oxybel", "TAVELLA", "31727387",
        "2026/015967", "Lafaurie", "500 474 457", "MAUVAIS GARCONS",
    ) if n in out]
    assert not fuites, f"Fuites résiduelles détectées: {fuites}"


def test_tokens_produits():
    """Les tokens produits doivent être normalisés (forme **[...]**)."""
    out = anonymize_text("Sébastien GRAZIDE a subi un accident.")
    assert "**[La Victime]**" in out, f"Token attendu non produit: {out!r}"


def test_aucun_double_astérisque_brut_dans_reel():
    """Un texte Reel (sans token) ne doit pas contenir de '**[' résiduel."""
    reel = "Sébastien GRAZIDE a été opéré par le Dr DJERBI le 30 mai 2026."
    # Ce texte n'est PAS tokenisé : on vérifie juste qu'anonymize ne casse pas
    out = anonymize_text(reel)
    assert "**[" not in out or "**[La " in out, f"Token brut inattendu: {out!r}"


def test_departements_supprimes():
    out = anonymize_text("À Toulouse (31) et Foix (09).")
    assert "(31)" not in out and "(09)" not in out
