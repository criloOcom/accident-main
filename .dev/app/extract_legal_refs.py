#!/usr/bin/env python3
"""Extract legal references from a document and generate Annexe B."""

import sys

# Legal references mapping from annuaire spreadsheet
LEGAL_REFS = {
    "Art.121-2": {"title": "Article 121-2 du Code pénal", "desc": "Responsabilité pénale des personnes morales", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006417204"},
    "Art.121-3": {"title": "Article 121-3 du Code pénal", "desc": "Faute caractérisée", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006417209"},
    "Art.1240": {"title": "Article 1240 du Code civil", "desc": "Responsabilité pour faute", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041571"},
    "Art.1242": {"title": "Article 1242 du Code civil", "desc": "Responsabilité du fait des choses et du commettant", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051786000"},
    "Art.145": {"title": "Article 145 du Code de procédure civile", "desc": "Référé-communication de pièces sous astreinte", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051869339"},
    "Art.1719": {"title": "Article 1719 du Code civil", "desc": "Obligation de délivrance paisible du bailleur", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000020459127"},
    "Art.1720": {"title": "Article 1720 du Code civil", "desc": "Obligation d'entretien et de réparations du bailleur", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006442784"},
    "Art.1844-8": {"title": "Article 1844-8 du Code civil", "desc": "Survie de la personnalité morale pour la liquidation", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006444186"},
    "Art.222-19": {"title": "Article 222-19 du Code pénal", "desc": "Blessures involontaires avec ITT supérieure à 3 mois", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000024042643"},
    "Art.222-20": {"title": "Article 222-20 du Code pénal", "desc": "Blessures involontaires avec ITT inférieure ou égale à 3 mois", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000024042640"},
    "Art.2226": {"title": "Article 2226 du Code civil", "desc": "Prescription de 10 ans pour le dommage corporel", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019017112"},
    "Art.475-1": {"title": "Article 475-1 du Code de procédure pénale", "desc": "Remboursement des frais d'avocat de la partie civile au pénal", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006576696/"},
    "Art.700": {"title": "Article 700 du Code de procédure civile", "desc": "Frais d'avocat au civil", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000045268436"},
    "Art.835": {"title": "Article 835 du Code de procédure civile", "desc": "Référé-provision pour obligation non sérieusement contestable", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042597284"},
    "Art.L113-2": {"title": "Article L113-2 du Code des assurances", "desc": "Déclaration sous 5 jours", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035731302"},
    "Art.L111-1": {"title": "Article L111-1 du Code de la consommation", "desc": "Obligation d'information précontractuelle", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048523650"},
    "Art.L124-3": {"title": "Article L124-3 du Code des assurances", "desc": "Action directe", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000017735449"},
    "Art.L217-1": {"title": "Article L217-1 du Code de la consommation", "desc": "Obligation de conformité du service", "url": "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069565/LEGISCTA000032227138/"},
    "Art.L227-8": {"title": "Article L227-8 du Code de commerce", "desc": "Responsabilité des dirigeants de SAS", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006227036/"},
    "Art.L421-3": {"title": "Article L421-3 du Code de la consommation", "desc": "Obligation générale de sécurité des services", "url": "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049464053"},
    "CCASS.00-82.066": {"title": "Cass. Ass. Plén., 14 décembre 2001, n° 00-82.066 (Arrêt Cousin)", "desc": "Responsabilité personnelle du préposé pour faute intentionnelle", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000007043322"},
    "CCASS.97-17.378": {"title": "Cass. Ass. Plén., 25 février 2000, n° 97-17.378 (Arrêt Costedoat)", "desc": "Immunité civile du préposé agissant dans les limites de sa mission", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000007043831"},
    "CCASS.13-80.849": {"title": "Cass. Crim., 27 mai 2014, n° 13-80.849", "desc": "Responsabilité pénale des personnes morales du fait de leurs préposés", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000029014493"},
    "CCASS.99-17.092": {"title": "Cass. Com., 20 mai 2003, n° 99-17.092 (Arrêt SATI)", "desc": "Faute détachable de ses fonctions du dirigeant", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000007047369"},
    "CCASS.20-16.463": {"title": "Civ. 1ère, 8 décembre 2021, n° 20-16.463", "desc": "Action directe recevable contre l'assureur d'une société dissoute", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000044482848"},
    "CCASS.22-19.307": {"title": "Civ. 2e, 4 avril 2024, n° 22-19.307", "desc": "Réparation intégrale et principe de libre disposition des fonds", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000049418278"},
    "CCASS.20-15.106": {"title": "Civ. 2e, 8 juillet 2021, n° 20-15.106", "desc": "Exigences probatoires rigoureuses pour l'indemnisation", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000043782126"},
    "CCASS.19-23.173": {"title": "Civ. 2e, 6 mai 2021, n° 19-23.173", "desc": "Incidence professionnelle (dévalorisation sociale, exclusion du monde du travail)", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000043489943"},
    "CCASS.18-12.766": {"title": "Civ. 2e, 4 avril 2019, n° 18-12.766", "desc": "Incidence professionnelle (devoir de recherche concrète)", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000038373596"},
    "CCASS.80-14.994": {"title": "Cass. Ass. Plén., 9 mai 1984, n° 80-14.994 (Arrêt Gabillet)", "desc": "Responsabilité du fait des choses de plein droit", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000007013792"},
    "CCASS.16-24.631": {"title": "Civ. 2e, 16 novembre 2017, n° 16-24.631", "desc": "Acte d'assistance spontané exclut la faute de la victime", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000036063717"},
    "CCASS.14-15.326": {"title": "Civ. 3e, 10 mars 2016, n° 14-15.326", "desc": "Défaut d'assurances professionnelles = faute détachable", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000032210878"},
    "CCASS.11-15.700": {"title": "Cass. Com., 10 mai 2012, n° 11-15.700", "desc": "Limite de la faute détachable", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000025859733"},
    "CCASS.21-14.197": {"title": "Civ. 2e, 15 juin 2023, n° 21-14.197", "desc": "Réparation intégrale et transactions", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000047700832"},
    "CCASS.19-15.659": {"title": "Civ. 2e, 28 mai 2020, n° 19-15.659", "desc": "Assiette de recours des tiers payeurs", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000041999264"},
    "CCASS.20-18-17.868": {"title": "Civ. 2e, 6 février 2020, n° 18-17.868", "desc": "Interruption de prescription par le référé-communication", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000041585779"},
    "CCASS.91-11.285": {"title": "Cass. Com., 26 janvier 1993, n° 91-11.285", "desc": "Survie de la personnalité morale d'une société dissoute pour les besoins de sa liquidation", "url": "https://www.legifrance.gouv.fr/juri/id/JURITEXT000007030228"},
}

def extract_legal_refs(text):
    """Extract legal references from document text."""
    found = {}
    text_lower = text.lower()
    
    # Check for specific references
    for ref_key, ref_data in LEGAL_REFS.items():
        # Check if the reference appears in the text
        title = ref_data["title"]
        # Simple check: look for key parts of the title
        if ref_key.startswith("Art."):
            art_num = ref_key.replace("Art.", "")
            if f"article {art_num}" in text_lower or f"art. {art_num}" in text_lower or f"art.{art_num}" in text_lower:
                found[ref_key] = ref_data
        elif ref_key.startswith("CCASS."):
            # For jurisprudence, check for case number
            case_num = ref_key.replace("CCASS.", "")
            if case_num in text:
                found[ref_key] = ref_data
    
    return found

def generate_annexe_b(found_refs):
    """Generate Annexe B markdown from found references."""
    if not found_refs:
        return ""
    
    lines = [
        "\n---\n",
        "# ANNEXE B — TEXTES DE LOI ET JURISPRUDENCE CITÉS\n",
        "Pour chaque référence, vous trouverez le titre complet, une explication en une phrase, et le lien officiel.\n",
    ]
    
    # Separate laws and jurisprudence
    laws = {k: v for k, v in found_refs.items() if k.startswith("Art.")}
    jurisprudence = {k: v for k, v in found_refs.items() if k.startswith("CCASS.")}
    
    if laws:
        lines.append("## Textes de loi\n")
        for key, data in sorted(laws.items()):
            lines.append(f"• **{data['title']}** — {data['desc']}")
            lines.append(f"  Lien : {data['url']}\n")
    
    if jurisprudence:
        lines.append("## Jurisprudence\n")
        for key, data in sorted(jurisprudence.items()):
            lines.append(f"• **{data['title']}** — {data['desc']}")
            lines.append(f"  Lien : {data['url']}\n")
    
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_legal_refs.py <document_text_file>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        text = f.read()
    
    found = extract_legal_refs(text)
    print(f"Found {len(found)} legal references")
    for ref in found:
        print(f"  - {ref}: {found[ref]['title']}")
    
    annexe_b = generate_annexe_b(found)
    print("\n--- Annexe B ---")
    print(annexe_b)
