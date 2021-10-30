from bs4 import BeautifulSoup
import requests
import time
import pickle
import re

# build dataset
def run():
    '''
        The url below links to the project gutenberg detective fiction shelf
    '''
    # Project gutenberg detective fiction bookshelf URL
    base_url = "https://www.gutenberg.org"
    subdirectories = ["/ebooks/bookshelf/30", "/ebooks/bookshelf/30?start_index=26",
                      "/ebooks/bookshelf/30?start_index=51", "/ebooks/bookshelf/30?start_index=76",
                      "/ebooks/bookshelf/30?start_index=101"]

    # This list will later be used to retrieve all .txt files. It stores all detective fiction's ebook subdirectories.
    all_ebook_sublinks = []

    # Continue processing pages until we reach the final page
    for subdirectory in subdirectories:
        # Retrieve HTML of first page with books
        html = requests.get(base_url + subdirectory).content

        # Parse HTML page to make it searchable with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # retrieve all book page links
        all_ebook_sublinks += [link.a['href'] for link in soup.find_all("li", "booklink")]

        time.sleep(5)
        continue

    # Each of the links can be find under the class named "booklink"

    # Pickle the result so we can reuse it
    with open("all_ebook_sublinks.pkl", "wb") as f:
        pickle.dump(all_ebook_sublinks, f)

    with open("all_ebook_sublinks.pkl", "rb") as f:
        all_ebook_sublinks = pickle.load(f)

    print(all_ebook_sublinks)

    # TODO: retrieve all book links from all pages
    # Next we retrieve all books' .txt files
    for bookdirectory in all_ebook_sublinks:
        # Retrieve HTML of first page with books
        html = requests.get(base_url + bookdirectory).content

        # # Parse HTML page to make it searchable with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the url to the .txt file
        txt_file_url = soup.find("table").find(text=re.compile('.txt'))

        # Retrieve.txt data
        response = requests.get(txt_file_url)
        txt_data = response.content

        # Just in case something went wrong with extracting the url to the .txt file
        if (response.status_code != 200):
            print(f'No correct file found for {bookdirectory}')

        # Give the file name the name of the book-id
        file_name = bookdirectory.split('/')[-1]
        path = 'data/gutenberg'
        with open(path + '/' + file_name + '.txt', "wb") as f:
            print(file_name)
            f.write(txt_data)

    return


if __name__ == "__main__":
    run()
    # TODO: split up above run() function into smaller functions