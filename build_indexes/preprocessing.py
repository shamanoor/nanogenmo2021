import os

def run():
    path = 'data/gutenberg/'
    for file in os.listdir(path):
        print(file)
        with open(path + file, "r", encoding="utf-8", errors='ignore') as f:
            txt_data = f.read()

        preprocessed_txt = preprocess(txt_data)
        preprocessed_path = 'preprocessed/gutenberg/'
        with open(preprocessed_path + file, 'w', encoding="utf-8") as f:
            f.write(preprocessed_txt)
        # print(preprocessed_txt)
    return

def preprocess(data):
    # Remove ***START OF THIS (...) ***
    idx1 = data.find("***") + 3

    # The index of the "***START OF"/"*** START OF" indicator
    idx1_end = data[idx1:].find('***') + 3 + idx1

    # Find index of "End of Project Gutenberg"/ "*** END OF"/"***END" indicator
    idx2 = data.rfind("End of Project Gutenberg")
    if idx2 < 0:
        idx2 = data.rfind("*** END OF")
    if idx2 < 0:
        idx2 = data.rfind("***END")

    # return gutenberg data with the majority of the gutenberg added information texts removed
    return data[idx1_end: idx2].strip()

if __name__ == "__main__":
    run()