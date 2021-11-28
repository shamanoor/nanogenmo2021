import pickle
from random import randrange
import wikipediaapi


if __name__=="__main__":
    # load the gutenberg index, which is a dict with key the keywords, and index the paragraphs where the keywords
    # appeared in
    with open('gutenberg_index.pkl', 'rb') as f:
        gutenberg_index = pickle.load(f)

    # load the tifu_index, which is a dict with the key the keywords, and with index the paragraphs where the keywords
    # appeared in
    with open('tifu_index.pkl', 'rb') as f:
        tifu_index = pickle.load(f)

    # Initialize story. It will be a list of paragraphs that at the end will be joined to one long story.
    story = []

    # initialize wiki object to do wiki searches with
    wiki_wiki = wikipediaapi.Wikipedia('en')

    while len((' '.join(story)).split()) < 50000:
        # randomly select a paragraph from a project gutenberg detective story
        candidate_paragraphs = gutenberg_index[list(gutenberg_index.keys())[randrange(len(gutenberg_index))]]
        selected_paragraph = candidate_paragraphs[randrange(len(candidate_paragraphs))]

        # add the paragraph to the story
        story.append(selected_paragraph)

        # get the latest paragraph from our story (this will be the story we added above, i.e. a project gutenberg
        # paragraph.
        # from this paragraph we are going to extract the keywords
        separate_words = story[-1].split()

        # one of the keywords that are collected here will be used to pick the next paragraph, from reddit tifu
        keywords = [word for word in separate_words if word in tifu_index.keys()]

        # select from the collected keywords a random keyword
        try:
            random_keyword = keywords[randrange(len(keywords))]
        except ValueError:
            continue

        # collect the candidate posts that have the selected keyword
        candidate_posts = tifu_index[random_keyword]

        # select a random post
        post = candidate_posts[randrange(len(candidate_posts))]
        candidate_posts.remove(post)

        # as some of the reddit tifu posts are very long, we only want to select the sentence in which they appear
        # to do this we look for the index of the keyword and search backwards to the first period to get the sentence's
        # start index, and then look forward from the keyword index to find the last period
        idx_keyword = post.find(random_keyword)
        start_idx = post[:idx_keyword].rfind('.') + 1
        end_idx = post[idx_keyword:].find('.')

        # the part of the reddit post that we will use will fall between the two periods, inclusive for the end period
        tifu_sentence = post[start_idx: idx_keyword + end_idx + 1]

        # we are aiming to append sentences that have at most 150 characters
        # in case the first selected tifu_sentence from the post is not this length, we move on to another post
        # in case we exhausted our candidate_posts list, we opt for another reddit post
        while len(tifu_sentence) > 150:
            print("candidate_posts length: ", len(candidate_posts))
            if len(candidate_posts) == 0:
                print("didnt find short enough sentence for keyword: ", random_keyword)
                # now we need to pick a different keyword
                random_keyword = keywords[randrange(len(keywords))]
                candidate_posts = tifu_index[random_keyword]
                print("new random keyword: ", random_keyword)
            if len(candidate_posts) == 1:
                post = candidate_posts[0]
            else:
                post = candidate_posts[randrange(len(candidate_posts))]

            candidate_posts.remove(post)

            idx_keyword = post.find(random_keyword)
            start_idx = post[:idx_keyword].rfind('.') + 1
            end_idx = post[idx_keyword:].find('.')

            tifu_sentence = post[start_idx: idx_keyword + end_idx + 1]



        tifu_sentence = tifu_sentence.strip()
        tifu_sentence = tifu_sentence[0].upper() + tifu_sentence[1:]

        # add the tifu_sentence to our story
        story.append(tifu_sentence)

        # lastly we try to get a wikipedia explanation of our keyword
        page_py = wiki_wiki.page(random_keyword)
        if page_py.exists():
            wiki_explanation_sentence = page_py.text[:page_py.text.find('\n')]

            if 'may refer to' not in wiki_explanation_sentence:
                # if a definition was found directly, append it to our story
                story.append(wiki_explanation_sentence)

        print("Story has ", len((' '.join(story)).split()), " words")


    with open('final_story.txt', 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(story))