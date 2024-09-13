import gensim
from gensim import models
from gensim.models import Word2Vec
from collections import defaultdict
import json
from gensim import corpora
import pprint
from pdbwhereami import whereami

def word2vec_tensim_basics():
    # Example corpus
    text_corpus = [
        "I love machine learning",
        "Word2Vec creates word embeddings",
        "Natural Language Processing is fun",
        "Text data is important in AI",
        "Machine learning is powerful"
    ]

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

    # Create a set of frequent words
    stoplist = set('for a of the and to in'.split(' '))
    # Lowercase each document, split it by white space and filter out stopwords
    texts = [[word for word in document.lower().split() if word not in stoplist]
            for document in text_corpus]

    print(f"stoplist (frequent words) :\n\t{stoplist}\n")

    print(f"Documents in lowercase after filter out stoplist...")
    for i in range(len(text_corpus)):
        print(f"\tDocument :{text_corpus[i]}, \n\ttext    :{texts[i]}\n")

    # Count word frequencies
    print(f"Word Frequency...")
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    # print(json.dumps(frequency, sort_keys=True, indent=4))
    print(f"\t{json.dumps(frequency, sort_keys=True)}")
    print()

    # Only keep words that appear more than once
    print(f"Only Words with Frequency is more than 1 ...")
    processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
    
    for text in processed_corpus:
        print(f"\t{text}")
    print()
    
    print("Generating each word with integer ID (Embedding)...")
    dictionary = corpora.Dictionary(processed_corpus)
    # print(dictionary)
    print(f"\t{json.dumps(dict(dictionary), sort_keys=True, indent=4)}")
    print()
    # pprint.pprint(json.dumps(dict(dictionary), sort_keys=True, indent=4))

    # print(dictionary.token2id)
    # print(json.dumps(dictionary.token2id, sort_keys=True, indent=4))
    # print(dictionary.id2token)

    new_doc = "Human computer interaction"
    # print(f"new_doc :{new_doc}")
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    # print(new_vec)
    # print()
    
    # print(f"processed_corpus :{processed_corpus}")
    bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]
    # print(f"bow_corpus :{bow_corpus}")
    
    for i in range(len(processed_corpus)):
        processed_corpus[i].sort()
        bow_corpus[i].sort()
        
        print(f"\tDocument :{processed_corpus[i]}, \n\ttext    :{bow_corpus[i]}\n")

    print("---")
    from gensim import models

    # train the model
    tfidf = models.TfidfModel(bow_corpus)

    # transform the "system minors" string
    words = "system minors".lower().split()
    whereami(f"words :{words}")
    # where(tfidf[dictionary.doc2bow(words)])
    tdwords = dictionary.doc2bow(words)
    
    whereami(f"tdwords      :{tdwords}")
    whereami(f"tfidf        :{tfidf}")
    whereami(f"tfidf type   :{type(tfidf)}")
    whereami(f"   num_nnz   :{tfidf.num_nnz}")
    whereami(f"   pivoit    :{tfidf.pivot}")
    whereami(f"   save      :{tfidf.save}")
    whereami(f"   slope     :{tfidf.slope}")
    whereami(f"   smartirs  :{tfidf.smartirs}")
    whereami(f"term_lengths :{tfidf.term_lengths}")
    whereami(f"    wglobal  :{tfidf.wglobal}")
    whereami(f"    wlocal   :{tfidf.wlocal}")

    sim_words = tfidf[tdwords]
    whereami(f"sim_words :{sim_words}")
    print("---")
    
    # for i in range(0, 28):
    #     tdwords = [(i, 1)]
    #     # tdwords = dictionary.doc2bow(words)
    #     sim_words = tfidf[tdwords]
    #     print(f"tdwords:sim_words: {tdwords} -- {sim_words}")
    # return

    from gensim import similarities

    index = similarities.SparseMatrixSimilarity(tfidf[bow_corpus], num_features=12)
    query_document = 'system engineering'.split()
    whereami(f"query_document :{query_document}")
    
    query_bow = dictionary.doc2bow(query_document)
    whereami(f"query_bow      :{query_bow}")
    
    tdwords = tfidf[query_bow]
    whereami(f"tdwords        :{tdwords}")
    
    # sim_words = index[tfidf[query_bow]]
    sim_words = index[tdwords]
    whereami(f"sim_words      :{sim_words}")
    # whereami(list(enumerate(sims)))

    for document_number, score in sorted(enumerate(sim_words), key=lambda x: x[1], reverse=True):
        print(document_number, score)
    
    return
    # print(bow_corpus)
    # Tokenize the corpus
    tokenized_corpus = [sentence.split() for sentence in text_corpus]

    print(f"tokenized_corpus...")
    # print(f"{tokenized_corpus}")
    for row in tokenized_corpus:
        print(f"\t{row}")
    print()
    
    return
    
    # Train Word2Vec model
    model = Word2Vec(sentences=tokenized_corpus, vector_size=2, window=3, min_count=1, workers=4)
    print(f"model...")
    # print(f"{model}")
    print(f"type :{type(model)}")
    # print(dir(model))
    
    # for item in dir(model):
    #     print(item)
    # print()
    

    # Find most similar words
    prompt = "machine"
    print(f"Similar words for...{prompt}")
    similar_words = model.wv.most_similar(prompt)
    print(similar_words)
    return

def main():
    word2vec_tensim_basics()
    

if __name__ == "__main__":
    main()
    