from skipgram import SkipGramModel
from preprocessing import Preps
import torch.optim as optim
from tqdm import tqdm
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


SIZE_OF_WIN = 10  
SIZE_OF_BATCH = 100 
MIN_FREQ = 3  
LEN_OF_VEC = 300  
LEARNING_RATE = 0.02 


class Word2Vec:
  
    def fit(self, documents):
        self.data = Preps(documents, MIN_FREQ)
        self.model = SkipGramModel(self.data.word_count, LEN_OF_VEC)
        
        self.use_cuda = torch.cuda.is_available()
        self.device = torch.device("cuda" if self.use_cuda else "cpu")
        if self.use_cuda:
            self.model.cuda()
            
        self.lr = LEARNING_RATE
        self.optimizer = optim.SGD(self.model.parameters(), lr=self.lr)
        print("Количество уникальных слов: {}".format(self.data.word_count))
        print("cuda:", self.use_cuda)
        print(self.model)
        pairs_count = self.data.evaluate_pairs_count(SIZE_OF_WIN)
        batch_count = pairs_count / SIZE_OF_BATCH
        process_bar = tqdm(range(int(batch_count)), desc = "Обучение")
        for i in process_bar:
            pos_pairs = self.data.get_batch_pairs(SIZE_OF_BATCH, SIZE_OF_WIN)
            pos_pairs,neg_pairs = self.data.get_pairs(pos_pairs)
            pos_u = [pair[0] for pair in pos_pairs]
            pos_v = [int(pair[1]) for pair in pos_pairs]
            neg_u = [pair[0] for pair in neg_pairs]
            neg_v = [int(pair[1]) for pair in neg_pairs]
            self.optimizer.zero_grad()
            loss = self.model.forward_pass(pos_u, pos_v, neg_u,neg_v)
            loss.backward()
            self.optimizer.step()
            
        
    def get_words(self):
        self.full_dict = list(self.data.id2word_dict.values()) 
        return self.full_dict
    
    def get_emb(self, word):
        self.full_dict = self.get_words()
        try:
            embedding = self.model.w_embeddings.weight.data.numpy()[self.full_dict.index(word)]
        except:
            embedding = print('Слова ' +  word + ' нет в словаре')
        return embedding
    
    def get_similar(self, word, k):
        embedding = self.get_emb(word)
        if isinstance(embedding,np.ndarray):
            all_embeddings = []
            for another_word in self.full_dict:
                all_embeddings.append(self.get_emb(another_word))
            dict_with_sim = cosine_similarity(embedding.reshape(1, -1), all_embeddings)[0]
            dict_with_sim = zip(self.full_dict, dict_with_sim)
            dict_with_sim = sorted(dict_with_sim, key=lambda x: x[1], reverse=True)
            similar_words = list(dict(dict_with_sim[1:k+1]).keys())
        else:
            similar_words = None
        return similar_words
    
    def save_state(self, PATH):
        torch.save(self, PATH)
        
    def load_state(self, PATH):
        model = torch.load(PATH)
        return model