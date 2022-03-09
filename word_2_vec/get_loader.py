import os #when loading file paths
import pandas as pd
import spacy
import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset
from PIL import Image # Load img
import torchvision.transforms as transforms

spacy_eng = spacy.load("en_core_web_sm")

# We want to convert text -> numerical values
# 1. We need a Vocabulary mapping each word to an index
# 2. We need to setup a Pytorch dataset to load the data
# 3. Setup padding of every batch (all examples should be of same seq_len and setup dataloader)
class Vocabulary:
    def __init__(self, freq_threshold):
        self.itos = {0:"<PAD>", 1:"<SOS>", 2:"<EOS>", 3:"<UNK>"}
        self.stoi = {"<PAD>":0, "<SOS>":1, "<EOS>":2, "<UNK>":3}
        self.freq_threshold = freq_threshold

    def __len__(self):
        return len(self.itos)

    @staticmethod
    def tokenizer_eng(text):
        return [tok.text.lower() for tok in spacy_eng.tokenizer(text)]
#"I love peanuts" -> ["i", "love", "peanuts"]
    def build_vocabulary(self, sentence_list):
        frequencies = {}
        idx = 4

        for sentence in sentence_list:
            for word in self.tokenizer_eng(sentence):
                if word not in frequencies:
                    frequencies[word] = 1
                else:
                    frequencies[word] +=1

                if frequencies[word] == self.freq_threshold:
                    self.stoi[word] = idx
                    self.itos[idx] = word
                    idx +=1

    def numericalize(self, text):
        tokenized_text = self.tokenizer_eng(text)

        return [
            self.stoi[token] if token in self.stoi else self.stoi["<UNK>"]
            for token in tokenized_text
        ]

class FlickrDataset(Dataset):
    def __init__(self, root_dir, captions_file, freq_threshold, transform = None, ):
        self.root_dir = root_dir
        self.df = pd.read_csv(captions_file)
        self.transform = transform

        # Get img, caption columns
        self.imgs = self.df["image_file"]
        self.captions = self.df["gold_sents"]

        # Initialize vocabulary and build vocab
        self.vocab = Vocabulary(freq_threshold)
        self.vocab.build_vocabulary(self.captions.tolist())

    def __len__(self):
        return len(self.df)

    def __getitem__(self,index):
        caption = self.captions[index]
        img_id = self.imgs[index]
        img = Image.open(os.path.join(self.root_dir, img_id)).convert("RGB")


        if self.transform is not None:
            img = self.transform(img)

        numericaled_caption = [self.vocab.stoi["<SOS>"]]
        numericaled_caption += self.vocab.numericalize(caption)
        numericaled_caption.append(self.vocab.stoi["<EOS>"])
        
        #print(img_id, caption)

        return img, torch.tensor(numericaled_caption)


class MyCollate:
    def __init__(self, pad_idx):
        self.pad_idx = pad_idx

    def __call__(self, batch):
        imgs = [item[0].unsqueeze(0) for item in batch]
        imgs = torch.cat(imgs, dim=0)
        targets = [item[1] for item in batch]
        targets = pad_sequence(targets, batch_first = False, padding_value = self.pad_idx)

        return imgs, targets

def get_loader(
    root_folder,
    annotation_file,
    transform,
    batch_size = 32,
    num_workers = 8,
    freq_threshold = 5,
    shuffle = True,
    pin_memory = True,):  
    dataset = FlickrDataset(root_folder, annotation_file, freq_threshold,transform = transform,  )
    pad_idx = dataset.vocab.stoi["<PAD>"]
    loader = DataLoader(
        dataset = dataset,
        batch_size = batch_size,
        num_workers = num_workers,
        shuffle = shuffle,
        pin_memory = pin_memory,
        collate_fn = MyCollate(pad_idx = pad_idx),
    )
    return loader, dataset

def main():
    transform = transforms.Compose(
        [
            transforms.Resize((224,224)),
            transforms.ToTensor(),
        ]
    )
    dataloader , dataset = get_loader("DIP_images/train/", annotation_file="Review_datasets/ext_train_exclude.csv", transform = transform)
    for idx, (imgs,captions) in enumerate(dataloader):
        print(imgs.shape)
        print(captions.shape)

if __name__ == "__main__":
    main()