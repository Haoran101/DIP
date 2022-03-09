import torch
import numpy as np
import pickle
from gensim.models import KeyedVectors
from get_loader import get_loader


def get_emb(vocab, embed_size):

    we_file = 'glove.840B.300d.top10k.word2vec'
    embeddings = KeyedVectors.load_word2vec_format(we_file)


    vocab_size = len(vocab)
    weights_matrix = np.zeros((vocab_size, embed_size))
    words_found = 0
    target_vocab = list(vocab.stoi.keys())

    for i, word in enumerate(target_vocab):
        try: 
            weights_matrix[i] = embeddings[word]
            words_found += 1
        except KeyError:
            weights_matrix[i] = np.random.normal(scale=0.6, size=(embed_size, ))
    print("vocab_size", vocab_size)
    print("Words found", words_found)
    return weights_matrix

def test_params(**params):

    print(params["train_CNN"])

params = {
    "embed_size" : 300,
    "hidden_size" : 256,
    "train_CNN" : False,
    "dropout_p" : 0.5,
    "encoder" : 3,
    "fine_tune_embeddings" : False,
}

test_params(**params)






