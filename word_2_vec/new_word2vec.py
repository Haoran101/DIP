from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

# load in existed glove file
glove_file = datapath(r'C:\Users\Christina\Documents\DIP\Week10\glove.vocab.300d.txt')

# trasform it into word2vec file
tmp_file = get_tmpfile(r'C:\Users\Christina\Documents\DIP\Week10\train_300d.word2vec')

#output the file
glove2word2vec(glove_file, tmp_file)




