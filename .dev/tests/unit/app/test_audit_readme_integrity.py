import os
import importlib.util
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
APP = os.path.join(ROOT, '.dev', 'app', 'audit_readme_integrity.py')

spec = importlib.util.spec_from_file_location('audit_readme_integrity', APP)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

find_files_in_text = mod.find_files_in_text
has_lrar_proof = mod.has_lrar_proof
has_ar_proof = mod.has_ar_proof
has_depot_proof = mod.has_depot_proof
check_text_anomalies = mod.check_text_anomalies
check_statut_declared_sent = mod.check_statut_declared_sent
check_envoi_34_ready = mod.check_envoi_34_ready
check_alignment = mod.check_alignment

def test_find_files_in_text():
    content = """
    Texte avec [fichier.md] et un gras **autre.md**.
    Lien Markdown [texte](dossier/fichier2.md) et [autre](url.md).
    Un texte qui n'a rien.
    """
    bare, urls = find_files_in_text(content)
    assert bare == {"fichier.md", "autre.md"}
    assert urls == {"dossier/fichier2.md", "url.md"}

def test_has_lrar_proof():
    assert has_lrar_proof("Preuve LRAR: 86001234567891A")
    assert has_lrar_proof("Mon envoi 87009876543211")
    assert not has_lrar_proof("Ceci n'est pas un LRAR")
    assert not has_lrar_proof("85001234567891") # mauvais préfixe

def test_has_ar_proof():
    assert has_ar_proof("L'accusé de réception a été signé.")
    assert has_ar_proof("AR signé le 12 mai.")
    assert not has_ar_proof("Le courrier a été envoyé.")

def test_has_depot_proof():
    assert has_depot_proof("Il y a un dépôt au greffe.")
    assert has_depot_proof("déposé le 12")
    assert not has_depot_proof("le courrier est prêt")

def test_check_text_anomalies():
    results = []
    content = "Balise [À compléter]\nBalise [À completer]\nAdresse [Adresse de la mairie]\nTODO à faire"

    check_text_anomalies(content, "fake_readme.md", results)

    msgs = [r["msg"] for r in results]
    assert any("Balise '[À compléter]' non résolue (l. 1)" in msg for msg in msgs)
    assert any("Balise '[À compléter]' non résolue (l. 2)" in msg for msg in msgs)
    assert any("Mention 'TODO' résiduelle" in msg for msg in msgs)
    assert not any("Adresse de la mairie" in msg for msg in msgs) # Exclu car contient "mairie"

    # Test Adresse non exclue
    results2 = []
    check_text_anomalies("Adresse [Adresse du tribunal]", "fake_readme.md", results2)
    assert any("Balise '[Adresse...]' non résolue (l. 1)" in r["msg"] for r in results2)

def test_check_statut_declared_sent():
    content = """
    | 99 | ✅ Envoyé | Sans preuve



    | 98 | Envoyé | Avec LRAR 86001234567891A



    | 04 | Envoyé | brouillon, mais c'est le doc 04
    """
    results = []
    check_statut_declared_sent(content, "fake_readme.md", results)

    assert len(results) == 1
    assert results[0]["doc"] == "99"
    assert results[0]["type"] == "statut_sent_sans_preuve"

def test_check_envoi_34_ready():
    content = """
    N°34
    Voici un document pour le Maire Foix
    Il manque un truc: [À compléter]
    """
    results = []
    check_envoi_34_ready(content, results)
    assert len(results) == 1
    assert "N°34 contient encore des [À compléter]" in results[0]["msg"]

def test_check_alignment(tmp_path):
    # Créer un faux répertoire avec un README.md et des fichiers
    d = tmp_path / "dossier"
    d.mkdir()
    readme = d / "README.md"
    f1 = d / "fichier_existant.md"
    f1.write_text("Hello")
    f2 = d / "fichier_non_liste.md"
    f2.write_text("Hello")

    readme.write_text("Liens vers [fichier_existant.md] et [fichier_manquant.md]")

    results = []
    check_alignment(str(readme), results)

    msgs = [r["msg"] for r in results]

    # fichier_manquant.md est déclaré mais absent
    assert any("Fichier déclaré 'fichier_manquant.md' introuvable" in msg for msg in msgs)

    # fichier_non_liste.md est présent mais non déclaré
    assert any("Fichier 'fichier_non_liste.md' présent mais non listé" in msg for msg in msgs)
