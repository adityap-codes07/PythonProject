import pandas as pd
import numpy as np
import math


doc1 = "I want to start learning to charge something in life"
doc2 = "reading something about life no one else knows"
doc3 = "Never stop learning"
#query string
query = "life learning"

def termFrequency(term, document):
    normalizeDocument = document.lower().split()
    return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))

def compute_normalizedtf(documents):
    tf_doc = []
    for txt in documents:
        sentence = txt.split()
        norm_tf= dict.fromkeys(set(sentence), 0)
        for word in sentence:
            norm_tf[word] = termFrequency(word, txt)
        tf_doc.append(norm_tf)
        df = pd.DataFrame([norm_tf])
        idx = 0
        new_col = ["Normalized TF"]
        df.insert(loc=idx, column='Document', value=new_col)
        print(df)
    return tf_doc

tf_doc = compute_normalizedtf([doc1, doc2, doc3])

def inverseDocumentFrequency(term, allDocuments):
    num = 0
    for docs in range(0, len(allDocuments)):
        if term.lower() in allDocuments[docs].lower().split():
            num += 1
    if num > 0:
        return 1.0 + math.log(float(len(allDocuments)) / num)
    else:
        return 1.0

def compute_idf(documents):
    idf_dict = {}
    for doc in documents:
        sentence = doc.split()
        for word in sentence:
            idf_dict[word] = inverseDocumentFrequency(word, documents)
    print(idf_dict)
    return idf_dict

idf_dict = compute_idf([doc1, doc2, doc3])

compute_idf([doc1, doc2, doc3])

# tf-idf score across all docs for the query string("life learning")
def compute_tfidf_with_alldocs(documents, query):
    tf_idf = []
    index = 0
    query_tokens = query.split()
    df = pd.DataFrame(columns=['doc'] + query_tokens)
    for doc in documents:
        df['doc'] = np.arange(0, len(documents))
        doc_num = tf_doc[index]
        sentence = doc.split()
        for word in sentence:
            for text in query_tokens:
                if (text == word):
                    idx = sentence.index(word)
                    tf_idf_score = doc_num[word] * idf_dict[word]
                    tf_idf.append(tf_idf_score)
                    df.iloc[index, df.columns.get_loc(word)] = tf_idf_score
        index += 1
    df.fillna(0, axis=1, inplace=True)
    return tf_idf, df

documents = [doc1, doc2, doc3]
tf_idf, df = compute_tfidf_with_alldocs(documents, query)
print(df)