
import pickle


'''
------------------------------------------------------------------------------------------------------
Example of loading train/val/test data
'''

def print_img_gt(data, num=10, distinct_images=True):
    count = 0
    image_ids = data['image_id']
    gt_sents = data['gold_sents']
    printed = []
    for img, gt in zip(image_ids, gt_sents):
        if distinct_images and img in printed:
            continue
        print("{}\t{}".format(img, gt))
        printed.append(img)
        count += 1
        if count >= num:
            break

ifile = 'DIP/val.spacy.sim.pkl'
# load the pickle file
data = pickle.load(open(ifile, 'rb'))
# data type: DataFrame

# print all keys
data.keys()

# print image id and the groundtruth review
print_img_gt(data, 20, distinct_images=True)

'''
------------------------------------------------------------------------------------------------------
read the dictionary file 
'''
from gensim.corpora.dictionary import Dictionary

# 1. import Dictionary: from gensim.corpora.dictionary import Dictionary
# 2. Load the file
dfile = 'DIP/dict_top10k.dict'
dict = Dictionary().load(dfile)
# get index of a word
idx = dict.token2id['pizza']
print(idx)
# get the word of an index
print(dict[371])

'''
------------------------------------------------------------------------------------------------------
load the pretrained word embeddings 
'''
from gensim.models import KeyedVectors
we_file = 'DIP/glove.840B.300d.top10k.word2vec'
embeddings = KeyedVectors.load_word2vec_format(we_file)

# getting the embeddings for the word "pizza"
pizza = embeddings['pizza']

'''
------------------------------------------------------------------------------------------------------
load json file 
'''
import json

img_file = 'DIP/img2link.json'
img2link = json.load(open(img_file, 'r'))
print(img2link['stZHnsIVVC1sFhLIYLVzzQ'])


