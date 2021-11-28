import wikipediaapi


def run():
    wiki_wiki = wikipediaapi.Wikipedia('en')

    page_py = wiki_wiki.page('knife')
    print("Page - Exists: %s" % page_py.exists())
    print(page_py.text[:page_py.text.find('\n')])


if __name__ == "__main__":
    run()