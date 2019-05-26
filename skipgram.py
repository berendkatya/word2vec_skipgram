import torch
import torch.nn as nn
import torch.nn.functional as F


class SkipGramModel(nn.Module):
    def __init__(self, emb_size, emb_dimension):
        super(SkipGramModel, self).__init__()
        self.emb_size = emb_size
        self.emb_dimension = emb_dimension
        self.w_embeddings = nn.Embedding(2 * emb_size - 1, emb_dimension, sparse=True)
        self.v_embeddings = nn.Embedding(2 * emb_size - 1, emb_dimension, sparse=True)

        initrange = 0.5 / self.emb_dimension
        self.w_embeddings.weight.data.uniform_(-initrange, initrange)
        self.v_embeddings.weight.data.uniform_(-0, 0)

    def forward_pass(self, pos_w, pos_v,neg_w, neg_v):
        emb_w = self.w_embeddings(torch.LongTensor(pos_w))  
        neg_emb_w = self.w_embeddings(torch.LongTensor(neg_w))
        emb_v = self.v_embeddings(torch.LongTensor(pos_v))
        neg_emb_v = self.v_embeddings(torch.LongTensor(neg_v)) 
        score = torch.mul(emb_w, emb_v).squeeze()
        score = torch.sum(score, dim=1)
        score = F.logsigmoid(-1 * score)
        neg_score = torch.mul(neg_emb_w, neg_emb_v).squeeze()
        neg_score = torch.sum(neg_score, dim=1)
        neg_score = F.logsigmoid(neg_score)
        loss = -1 * (torch.sum(score) + torch.sum(neg_score))
        
        return loss