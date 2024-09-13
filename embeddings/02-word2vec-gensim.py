from pdbwhereami import whereami
from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities

text_corpus = [
    "Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey",
]

STOPLIST_STR = 'for a of the and to in'

def get_stop_list():
    return set(STOPLIST_STR.split())

def get_documents():
    return text_corpus

def dump_docs_list(docs_list):
    print(f"docs_list: len ({len(docs_list)})")
    for row in docs_list:
        print(f"\t{row}")
    print()

def dump_stop_list(stop_list):
    print(f"stop_list frequent words len({len(stop_list)})")
    print(f"\t{stop_list}")
    print()

def dump_texts(texts):
    print(f"texts len({len(texts)})")
    for row in texts:
        print(f"\t{row}")
    print()

def count_word_frequency(texts):
    # Count word frequencies
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    return frequency

def dump_frequency(frequency):
    print(f"Word Frequency...len({len(frequency)})")
    print("\t", end="")
    tlist = list(dict(frequency).items())
    tlist.sort()
    for i, item in enumerate(tlist, 1):
        print(f"{item[0]:<15} : {item[1]:<5}", end="")
        
        if(i%3 == 0):
            print()
            print("\t", end="")
    print()
    print()

def dump_corpus_id(tstr, corpus):
    print(f"{tstr}....len({len(corpus)})")
    print("\t", end="")
    tlist = list(dict(corpus).items())
    tlist.sort()
    for i, item in enumerate(tlist, 1):
        print(f"{item[0]:<10} : {item[1]:<15}", end="")
        
        if(i%3 == 0):
            print()
            print("\t", end="")
    print()
    print()

def process_corpus(frequency, texts):
    new_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
    return new_corpus

def generate_id(corpus):
    print("Generating each word with integer ID (Embedding)...")
    id_corpus = corpora.Dictionary(corpus)
    
    return id_corpus

def vectorize_example(id_corpus):
    print("'bag-of-word': Based on above Tokens & IDs, Vecrorizing new document...")
    new_doc = "Human computer interaction system"
    tokens = new_doc.lower().split()
    tokens.sort()
    print(f"\tDocument :{new_doc}")
    print(f"\tTockens  :{tokens}")
    retval = id_corpus.doc2bow(tokens, return_missing=True)

    new_vec = retval[0]
    new_vec.sort()
    missing_tokens = retval[1]
    
    print(f"\tsparse representation of words  :{new_vec}")
    print(f"\tmissing_tokens :{missing_tokens}")
    print()

def corpus_to_vec(id_corpus, corpus):
    print("'bag-of-word': Vectorize entire original corpus...")

    bow_corpus = [id_corpus.doc2bow(text) for text in corpus]
    
    for i in range(len(corpus)):
        corpus[i].sort()
        bow_corpus[i].sort()
        
        print(f"\tDocument :{corpus[i]}, \n\ttext    :{bow_corpus[i]}\n")

    print()
    return bow_corpus

def create_tf_idf_model(bow_corpus):
    tfidf = models.TfidfModel(bow_corpus)
    return tfidf

def transform_test_string(id_corpus, tfidf_model):
    tstr = "system minors"
    print("Trnsforming string...")
    
    words = tstr.lower().split()
    # words.sort()
    print(f"\tDocument :{tstr}")
    print(f"\tWords    :{words}")
    
    tbow = id_corpus.doc2bow(words)
    # tbow.sort()
    print(f"\tFrom bow :{tbow}")
    print()
    
    print(f"From tfidf Model ID & Weight(s) are...")
    retval = tfidf_model[tbow]
    
    print(f"\t{retval}")
    print()
    
    return    

def index_and_similarity_query_copus(tfidf_model, id_corpus, bow):
    print(f"Query simulartiy search against every document in corpus...")
    index = similarities.SparseMatrixSimilarity(tfidf_model[bow], num_features=12)
   
    document = 'system engineering'
    query_document = document.split()
    # and to query the similarity of our query document ``query_document`` against every document in the corpus:
    print(f"\tDocument :{document}")
    print(f"\tQuery Document (words) :{query_document}")
    
    query_bow = id_corpus.doc2bow(query_document)
    print(f"\tQuery Bag of Words) :{query_bow}")
    print()

    print(f"\tFrom tfidf Model ID & Weight(s) are...")
    retval = tfidf_model[query_bow]
    print(f"\tRetval :{retval}")
    print()
    
    sims = index[retval]
    
    # print(f"\tSimilarity with every document in corpus and score...")
    # similars = list(enumerate(sims))
    # print(f"\tSimilars :{similars}")
    # print()
    
    # dict(id_corpus)
    search_word = dict(id_corpus)[query_bow[0][0]]
    print(f"Searching similar words against :'{search_word}'")
    for doc_num, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True):
        print(f"\t{id_corpus[doc_num]}({doc_num}) -->{score} (score)")

    print()
    
def main():
    stoplist = get_stop_list()
    docs_list = get_documents()
    
    dump_docs_list(docs_list)
    dump_stop_list(stoplist)
    
    texts = [[word for word in doc.lower().split() if word not in stoplist] for doc in docs_list]
    dump_texts(texts)
    
    frequency = count_word_frequency(texts)
    dump_frequency(frequency)
    
    new_corpus = process_corpus(frequency, texts)
    print(f"Only Words with Frequency is more than 1...")
    dump_texts(new_corpus)
    
    id_corpus = generate_id(new_corpus)
    dump_corpus_id("Id2Token", id_corpus)
    dump_corpus_id("Token2Id", id_corpus.token2id)
        
    vectorize_example(id_corpus)
    bow = corpus_to_vec(id_corpus, new_corpus)
    
    tfidf_model = create_tf_idf_model(bow)
    
    transform_test_string(id_corpus, tfidf_model)

    index_and_similarity_query_copus(tfidf_model, id_corpus, bow)

if __name__ == "__main__":
    main()
