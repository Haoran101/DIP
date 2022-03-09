from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import numpy as np
#import bcolz
import pickle


with open('vocabulary_full.pkl', 'rb') as f:
    vocab = pickle.load(f)

print(len(vocab))

with open('glove.840B.300d.txt', 'rb') as f:

    line_counter = 0

    for l in f:
        line = l.decode().split()
        word = line[0]
        assert(len(vect) == 300)
        if word in vocab.stoi.keys():
            line_counter +=1
            with open('glove.vocab.300d.txt','a') as handle:
                handle.write(line)
                handle.write("/n")

    print(line_counter)
    print(len(vocab))
