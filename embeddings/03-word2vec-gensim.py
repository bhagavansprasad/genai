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

stoplist = 'for a of the and to in'

def get_stop_list():
    return set(stoplist.split())

def get_documents():
    return text_corpus

def dump_docs_list(docs_list):
    print(f"docs_list: len ({len(docs_list)})")
    for row in docs_list:
        print(f"\t{row}")
    print()

def dump_stop_list(stoplist):
    print(f"stoplist frequent words len({len(stoplist)})")
    print(f"\t{stoplist}")
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

def dump_corpus_id(tstr, dictionary):
    print(f"{tstr}....len({len(dictionary)})")
    print("\t", end="")
    tlist = list(dict(dictionary).items())
    tlist.sort()
    for i, item in enumerate(tlist, 1):
        print(f"{item[0]:<10} : {item[1]:<15}", end="")
        
        if(i%3 == 0):
            print()
            print("\t", end="")
    print()
    print()

def process_corpus(frequency, texts):
    processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
    return processed_corpus

def generate_id(corpus):
    print("Generating each word with integer ID (Embedding)...")
    dictionary = corpora.Dictionary(corpus)
    
    return dictionary

def vectorize_example(dictionary):
    print("'bag-of-word': Based on above Tokens & IDs, Vecrorizing new document...")
    new_doc = "Human computer interaction system"
    tokens = new_doc.lower().split()
    tokens.sort()
    print(f"\tDocument :{new_doc}")
    print(f"\tTockens  :{tokens}")
    retval = dictionary.doc2bow(tokens, return_missing=True)

    new_vec = retval[0]
    new_vec.sort()
    missing_tokens = retval[1]
    
    print(f"\tsparse representation of words  :{new_vec}")
    print(f"\tmissing_tokens :{missing_tokens}")
    print()

def corpus_to_vec(dictionary, processed_corpus):
    print("'bag-of-word': Vectorize entire original corpus...")

    bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
    
    for i in range(len(processed_corpus)):
        processed_corpus[i].sort()
        bow_corpus[i].sort()
        
        print(f"\tDocument :{processed_corpus[i]}, \n\ttext    :{bow_corpus[i]}\n")

    print()
    return bow_corpus

def create_tf_idf_model(bow_corpus):
    tfidf = models.TfidfModel(bow_corpus)
    return tfidf

def transform_test_string(dictionary, tfidf):
    tstr = "system minors"
    print("Trnsforming string...")
    
    words = tstr.lower().split()
    # words.sort()
    print(f"\tDocument :{tstr}")
    print(f"\tWords    :{words}")
    
    tbow = dictionary.doc2bow(words)
    # tbow.sort()
    print(f"\tFrom bow :{tbow}")
    print()
    
    print(f"From tfidf Model ID & Weight(s) are...")
    retval = tfidf[tbow]
    
    print(f"\t{retval}")
    print()
    
    return    

def index_and_similarity_query_copus(tfidf, dictionary, bow_corpus):
    print(f"Query simulartiy search against every document in corpus...")
    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=12)
   
    document = 'system engineering'
    query_document = document.split()
    # and to query the similarity of our query document ``query_document`` against every document in the corpus:
    print(f"\tDocument :{document}")
    print(f"\tQuery Document (words) :{query_document}")
    
    query_bow = dictionary.doc2bow(query_document)
    print(f"\tQuery Bag of Words) :{query_bow}")
    print()

    print(f"\tFrom tfidf Model ID & Weight(s) are...")
    retval = tfidf[query_bow]
    print(f"\tRetval :{retval}")
    print()
    
    sims = index[retval]
    
    # print(f"\tSimilarity with every document in corpus and score...")
    # similars = list(enumerate(sims))
    # print(f"\tSimilars :{similars}")
    # print()
    
    # dict(id_corpus)
    search_word = dict(dictionary)[query_bow[0][0]]
    print(f"Searching similar words against :'{search_word}'")
    for doc_num, score in sorted(enumerate(sims), key=lambda x: x[1], reverse=True):
        print(f"\t{dictionary[doc_num]}({doc_num}) -->{score} (score)")

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
    
    processed_corpus = process_corpus(frequency, texts)
    print(f"Only Words with Frequency is more than 1...")
    dump_texts(processed_corpus)
    
    dictionary = generate_id(processed_corpus)
    dump_corpus_id("Id2Token", dictionary)
    dump_corpus_id("Token2Id", dictionary.token2id)
        
    vectorize_example(dictionary)
    bow_corpus = corpus_to_vec(dictionary, processed_corpus)
    
    tfidf = create_tf_idf_model(bow_corpus)
    
    transform_test_string(dictionary, tfidf)

    index_and_similarity_query_copus(tfidf, dictionary, bow_corpus)

if __name__ == "__main__":
    main()
