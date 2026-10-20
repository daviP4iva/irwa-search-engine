from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def build_terms(line: str):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))

    line= line.lower()
    line= line.split()
    line=[word for word in line if word not in stop_words]
    line=[word for word in line if word.isalnum()]
    line=[stemmer.stem(word) for word in line]

    return line

def preprocess(corpus: dict, search_id: int):
    elements_text = [element.title + element.description for element in corpus.values()]
    lines = [text.strip().replace(' +', ' ') for text in elements_text]
    lines_terms = [build_terms(line) for line in lines]
    print(lines_terms)
    