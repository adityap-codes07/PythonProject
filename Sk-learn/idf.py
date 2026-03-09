import math

doc1 = "I want to start learning to charge something in life"
doc2 = "reading something about life no one else knows"
doc3 = "Never stop learning"

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