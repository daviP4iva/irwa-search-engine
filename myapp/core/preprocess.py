from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import defaultdict

def build_terms(line: str):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    accepted_chars = ['/', '%', '.', ',']



    line= line.lower()
    line= line.split()
    line=[word for word in line if word not in stop_words]
    line = [''.join(ch for ch in word if ch.isalnum() or ch in accepted_chars) for word in line]
    line = [word for word in line if len(word) > 0]
    line=[stemmer.stem(word) for word in line]
    new_line = []
    for word in line:
        for i, char in enumerate(word):
            if (
                char in accepted_chars
                and i > 0
                and i < len(word) - 1
                and (word[i - 1].isalpha() or word[i + 1].isalpha())
            ):
                new_line.extend([word[:i], word[i + 1:]])
                break
        else:
            new_line.append(word)

    line = new_line

    return line

def create_index(corpus: dict):
    index = defaultdict(list)
    for element in corpus.values():

        element_text = element.title + element.description
        element_pid = element.pid
        element_text = element_text.strip()
        element_terms = build_terms(element_text)

        current_page_index = {}
        
        for position, term in enumerate(element_terms):
            try:
                current_page_index[term][1].append(position)
            except:
                current_page_index[term] = [element_pid, [position]]

        for term, term_info in current_page_index.items():
            index[term].append(term_info)

    return index

    