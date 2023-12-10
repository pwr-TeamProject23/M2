def test_get_keywords(article):
    keywords = article["pdf"].get_keywords()
    assert keywords == article["data"]["keywords"]


def test_get_abstract(article):
    abstract = article["pdf"].get_abstract()
    assert abstract == article["data"]["abstract"]


def test_get_authors(article):
    authors = article["pdf"].get_authors()
    assert authors == article["data"]["authors"]


def test_get_emails(article):
    emails = article["pdf"].get_emails()
    assert emails == article["data"]["emails"]
