from app.batch_link_legifrance import link, apply_replacements, link_annexe_b_articles, fix_annexe_b_wrong_ids

def test_link():
    assert link("JURITEXT123", "Some case") == "[Some case](https://www.legifrance.gouv.fr/juri/id/JURITEXT123)"
    assert link("LEGIARTI123", "Some article") == "[Some article](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI123)"

def test_apply_replacements():
    replacements = [
        (r"foo", "bar"),
        (r"hello\s+world", "bye world")
    ]
    text = "foo baz hello world"
    expected = "bar baz bye world"
    assert apply_replacements(text, replacements) == expected

def test_link_annexe_b_articles():
    text = "**Article 1240 du Code civil** — some text"
    expected = "**[Article 1240 du Code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041571)** — some text"
    assert link_annexe_b_articles(text) == expected

    text = "**Article 1720 du Code civil** — no link"
    assert link_annexe_b_articles(text) == text # 1720 maps to None

    text = "Some regular text without bold article"
    assert link_annexe_b_articles(text) == text

    text = "**Article 1240 du Code civil**"
    expected = "**[Article 1240 du Code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041571)**"
    assert link_annexe_b_articles(text) == expected

def test_fix_annexe_b_wrong_ids():
    text = "[Lien](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019017112)"
    expected = "[Lien](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019017259)"
    assert fix_annexe_b_wrong_ids(text) == expected
