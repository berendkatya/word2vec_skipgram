from collections import deque

class HuffmanNode:
    def __init__(self, word_id, frequency):
        self.word_id = word_id  
        self.frequency = frequency 
        self.left_child = None
        self.right_child = None
        self.father = None
        self.Huffman_code = [] 
        self.path = [] 


class HuffmanTree:
    def __init__(self, wordid_frequency_dict):
        self.word_count = len(wordid_frequency_dict) 
        self.wordid_code = dict()
        self.wordid_path = dict()
        self.root = None
        unmerge_node_list = [HuffmanNode(wordid, frequency) for wordid, frequency in
                             wordid_frequency_dict.items()] 
        self.huffman = [HuffmanNode(wordid, frequency) for wordid, frequency in
                        wordid_frequency_dict.items()]
 
        self.build_tree(unmerge_node_list)
 
        self.gen_huffman_code_and_path()

    def merge_node(self, node1, node2):
        sum_frequency = node1.frequency + node2.frequency
        mid_node_id = len(self.huffman)  
        father_node = HuffmanNode(mid_node_id, sum_frequency)
        if node1.frequency >= node2.frequency:
            father_node.left_child = node1
            father_node.right_child = node2
        else:
            father_node.left_child = node2
            father_node.right_child = node1
        self.huffman.append(father_node)
        return father_node

    def build_tree(self, node_list):
        while len(node_list) > 1:
            i1 = 0 
            i2 = 1  
            if node_list[i2].frequency < node_list[i1].frequency:
                [i1, i2] = [i2, i1]
            for i in range(2, len(node_list)):
                if node_list[i].frequency < node_list[i2].frequency:
                    i2 = i
                    if node_list[i2].frequency < node_list[i1].frequency:
                        [i1, i2] = [i2, i1]
            father_node = self.merge_node(node_list[i1], node_list[i2]) 
            if i1 < i2:
                node_list.pop(i2)
                node_list.pop(i1)
            elif i1 > i2:
                node_list.pop(i1)
                node_list.pop(i2)
            else:
                raise RuntimeError('i1 should not be equal to i2')
            node_list.insert(0, father_node)
        self.root = node_list[0]

    def gen_huffman_code_and_path(self):
        stack = [self.root]
        while len(stack) > 0:
            node = stack.pop()

            while node.left_child or node.right_child:
                code = node.Huffman_code
                path = node.path
                node.left_child.Huffman_code = code + [1]
                node.right_child.Huffman_code = code + [0]
                node.left_child.path = path + [node.word_id]
                node.right_child.path = path + [node.word_id]
       
                stack.append(node.right_child)
                node = node.left_child
            word_id = node.word_id
            word_code = node.Huffman_code
            word_path = node.path
            self.huffman[word_id].Huffman_code = word_code
            self.huffman[word_id].path = word_path
          
            self.wordid_code[word_id] = word_code
            self.wordid_path[word_id] = word_path

 
    def get_all_pos_and_neg_path(self):
        pos = [] 
        neg = []  
        for word_id in range(self.word_count):
            pos_id = []  
            neg_id = [] 
            for i, code in enumerate(self.huffman[word_id].Huffman_code):
                if code == 1:
                    pos_id.append(self.huffman[word_id].path[i])
                else:
                    neg_id.append(self.huffman[word_id].path[i])
            pos.append(pos_id)
            neg.append(neg_id)
        return pos, neg

class Preps:
    def __init__(self, documents, min_count):
        self.documents = documents
        self.min_count = min_count  
        self.wordId_frequency_dict = dict()  
        self.word_count = 0  
        self.word_count_sum = 0  
        self.sentence_count = 0 
        self.id2word_dict = dict()  
        self.word2id_dict = dict()  
        self._init_dict()  
        self.huffman_tree = HuffmanTree(self.wordId_frequency_dict) 
        self.huffman_pos_path, self.huffman_neg_path = self.huffman_tree.get_all_pos_and_neg_path()
        self.word_pairs_queue = deque()

    def _init_dict(self):
        word_freq = dict()
        for line in self.documents:

            self.word_count_sum += len(line)
            self.sentence_count += 1
            for word in line:
                try:
                    word_freq[word] += 1
                except:
                    word_freq[word] = 1
        word_id = 0
     
        for per_word, per_count in word_freq.items():
            if per_count < self.min_count: 
                self.word_count_sum -= per_count
                continue
            self.id2word_dict[word_id] = per_word
            self.word2id_dict[per_word] = word_id
            self.wordId_frequency_dict[word_id] = per_count
            word_id += 1
        self.word_count = len(self.word2id_dict)

    
    def get_batch_pairs(self, batch_size, window_size):
        self.documents = self.documents
        while len(self.word_pairs_queue) < batch_size:
            for i in range(len(self.documents)): 
                sentence = self.documents[i]
                if sentence is None or sentence == '':
                    continue
                wordId_list = [] 
                for word in sentence:
                    try:
                        word_id = self.word2id_dict[word]
                        wordId_list.append(word_id)
                    except:
                        continue
            
                for i, wordId_w in enumerate(wordId_list):
                    for j, wordId_v in enumerate(wordId_list[max(i - window_size, 0):i + window_size + 1]):
                        assert wordId_w < self.word_count
                        assert wordId_v < self.word_count
                        if i == j: 
                            continue
                        self.word_pairs_queue.append((wordId_w, wordId_v))
        result_pairs = []  
        for _ in range(batch_size):
            result_pairs.append(self.word_pairs_queue.popleft())
        return result_pairs

    def get_pairs(self, pos_pairs):
        neg_word_pair = []
        pos_word_pair = []
        for pair in pos_pairs:
            pos_word_pair += zip([pair[0]] * len(self.huffman_pos_path[pair[1]]), self.huffman_pos_path[pair[1]])
            neg_word_pair += zip([pair[0]] * len(self.huffman_neg_path[pair[1]]), self.huffman_neg_path[pair[1]])
        return pos_word_pair, neg_word_pair

  
    def evaluate_pairs_count(self, window_size):
        return self.word_count_sum * (2 * window_size - 1) - (self.sentence_count - 1) * (1 + window_size) * window_size