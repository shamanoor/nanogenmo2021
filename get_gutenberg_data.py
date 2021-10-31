from bs4 import BeautifulSoup
import requests
import time
import pickle
import re

def retrieve_txt_links(base_url, all_ebook_sublinks):
    txt_links = []
    for bookdirectory in all_ebook_sublinks:
        # Retrieve HTML of first page with books
        response = requests.get(base_url + bookdirectory)
        html = response.content

        if response.status_code != 200:
            print(f"Issue with retrieving data from url {base_url + bookdirectory}. Status code was not 200.")
            continue
        soup = BeautifulSoup(html, 'html.parser')

        # Check if book is in english, we only want english books
        language = soup.find("table", "bibrec").find("tr", {"property":"dcterms:language"}).find("td").text

        # Check if book is sound, if it is, continue to the next one as we want text only
        category = soup.find("table", "bibrec").find("td", {"property": "dcterms:type"}).text
        print(language, category)

        if not (language == "English" and category == "Text"):
            print(f"The book language is {language}, the category is {category}. This does not match the requirements"
                  f"and hence the book link will not be stored to build the dataset.")
            continue

        # Retrieve the url to the .txt file and add it to the list of txt links
        txt_link = soup.find("table").find(text=re.compile('.txt'))

        if 'readme' in txt_link:
            print(f"The .txt link for book with url {base_url + bookdirectory} was a readme file. For this reason it is "
                  f"not added to the list of final txt_links, and hence will not be downloaded.")
            continue
        txt_links.append(txt_link)
        print(f"Retrieved from bookdirectory {bookdirectory}")
        time.sleep(3)

    return txt_links


def download_txts_from_links(txt_links):
    for txt_link in txt_links:
        # Retrieve.txt data
        response = requests.get(txt_link)
        txt_data = response.content

        # Just in case something went wrong with extracting the url to the .txt file
        if (response.status_code != 200):
            print(f'No correct .txt file found for {txt_link}')
            continue

        # Give the file name the name of the book-id
        gutenberg_file_name = txt_link.split('/')[-1]

        # get the file name before .txt
        file_name = gutenberg_file_name[:gutenberg_file_name.index('.txt')]
        path = 'data/gutenberg'

        with open(path + '/' + file_name + '.txt', "wb") as f:
            print(file_name)
            f.write(txt_data)


def get_ebook_sublinks(base_url, subdirectories):
    '''
    :param base_url: the base url of the project gutenberg website
    :param subdirectories: the subdirectories that each link to a page of a bookshelf, in this specific project it
    links to each page of the Detective Fiction bookshelf
    :return: all_ebook_sublinks[] : list of subdirectories/sublinks of each ebook from the bookshelf pages. This list
    will later be used to retrieve all .txt files. It stores all detective fiction's ebook subdirectories.
    '''

    # This list will
    all_ebook_sublinks = []

    # Continue processing pages until we reach the final page
    for subdirectory in subdirectories:
        # Retrieve HTML of first page with books
        response = requests.get(base_url + subdirectory)
        html = response.content

        print(f"Subdirectory: {base_url + subdirectory}")

        if response.status_code == 200:
            # Parse HTML page to make it searchable with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Retrieve all book page links
            all_ebook_sublinks += [link.a['href'] for link in soup.find_all("li", "booklink")]
        else:
            print(f"Did not receive status 200 for page {base_url + subdirectory}")

        # Wait a bit to not overburden the website
        time.sleep(5)

    return all_ebook_sublinks


def get_base_url():
    return "https://www.gutenberg.org"


def get_subdirectories():
    return ["/ebooks/bookshelf/30", "/ebooks/bookshelf/30?start_index=26",
            "/ebooks/bookshelf/30?start_index=51", "/ebooks/bookshelf/30?start_index=76",
            "/ebooks/bookshelf/30?start_index=101"]


def write_to_pickle(data, file_name):
    '''
    Pickle the data so we can reuse it without having to re-scrape it
    :param data:
    :param file_name:
    '''
    with open(file_name + ".pkl", "wb") as f:
        pickle.dump(data, f)


def open_from_pickle(file_name):
    with open(file_name, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    # Project gutenberg detective fiction bookshelf URL
    base_url = get_base_url()
    subdirectories = get_subdirectories()

    ebook_sublinks = get_ebook_sublinks(base_url, subdirectories)
    # ebook_sublinks = open_from_pickle("ebook_sublinks.pkl")

    txt_links = retrieve_txt_links(base_url, ebook_sublinks)
    download_txts_from_links(txt_links)