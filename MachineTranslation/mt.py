import numpy as np
import pdb
from scipy.sparse.sparsetools import csr_scale_rows
from scipy.sparse import csr_matrix
from scipy.sparse import find
from sklearn import preprocessing
import math
TRAIN = 0.8
class MT:
    def __init__(self, l1, l2, prefix):
        self.l1 = l1
        self.l2 = l2
        self.prefix = prefix

    def gen_vocab(self, vocab_file):
        vocab = {}
        with open(vocab_file) as fin:
            for line in fin:
                d = line.strip().split()
                vocab[d[1]] = int(d[0])
        vocab['^^'] = 0
        vocab['^^^'] = len(vocab)
        return vocab

    def emission(self, prob_file):
        probs = np.loadtxt(self.prefix + prob_file, dtype=np.float32)
        rows = probs[:,0]
        cols = probs[:,1]
        data = probs[:,2]
        table = csr_matrix((data, (rows, cols)), shape=(len(self.l1v), len(self.l2v)))
        return table.log1p()
    
    def transition(self, trg):
        d2 = self.l2v
        N = len(self.l2v)
        rows, cols, data = [], [], []
        with open(trg) as fin:
            for line in fin:
                l = line.strip().split()
                l = ['^^'] + l + ['^^^']
                for idx, w in enumerate(l):
                    if idx == 0:
                        continue
                    rows.append(d2[w])
                    cols.append(d2[l[idx-1]])
                    data.append(1)
        table = csr_matrix((data, (rows, cols)), shape=(N,N))
        table = preprocessing.normalize(table, norm = 'l1')
        return table.log1p()

    def search(self, sentence):
        emission = self.emission
        transition = self.transition
        N = transition.shape[0]
        d1, d2 = self.l1v, self.l2v
        pdb.set_trace()
        print(len(d1),len(d2))
        vector = [d1[w] for w in sentence]
        line = [d1['^^']] + vector + [d1['^^^']]
        seqscore = np.zeros((len(d2), len(line)), dtype=np.float32)
        backptr = np.zeros((len(d2), len(line)), dtype=np.int32)
        seqscore[0][0] = 1
        backptr[0][0] = d1['^^']
        for t, w in enumerate(line):
            wordindex = w
            em_row = emission.getrow(wordindex).toarray()
            if t == 0:
                continue
            for k1, v1 in d2.items():
                maxScore = 0
                # current word index
                idx1 = v1
                if not str(idx1).isdigit():
                    continue
                #locs = np.where(nonzero_r == idx1)
                #indices = nonzero_c[locs]
                #vals = nonzero_data[locs]
                tr_row = transition.getrow(idx1)
                rs, indices, vals = find(tr_row)
                for idx2, v2 in zip(indices, vals):
                    if em_row[0][idx1] == 0:
                        continue
                    score = seqscore[idx2][t-1] + v2 + em_row[0][idx1]
                    if score > maxScore:
                        #print(score)
                        maxScore = score
                        seqscore[idx1][t] = maxScore
                        backptr[idx1][t] = idx2
        i, score = 0, 0
        l2out = [0] * len(line)
        for j in range(len(d2)):
            if score < seqscore[j][-1]:
                score, i = seqscore[j][-1], j
        l2out[len(line)-1] = i
        for j in range(len(line)-2,-1,-1):
            l2out[j] = backptr[i][j+1]
            i = l2out[j]
        inv_d = {v: k for k, v in d2.items()}
        return [inv_d[w] for w in l2out]

    def train(self):
        self.l1v = self.gen_vocab(self.l1+'.vcb')
        self.l2v = self.gen_vocab(self.l2+'.vcb')
        self.emission = self.emission("t3.final")
        self.transition = self.transition("hi.low")
        sent = ["volume", "group", "to", "extend", ":"]
        res = self.search(sent)
        f=open('test', 'w')
        #w=sent[0]
        #i = self.l1v[w]
        #row=self.emission.getrow(i)
        #r,res,d = find(row)
        #d=np.log1p(d)
        #inv_d = {v: k for k, v in self.l2v.items()}
        #x=zip(res,d)
        #z=sorted(x, key=lambda x: x[1], reverse=True)
        #for w in z:
        #    f.write(inv_d[w[0]]+'\t'+str(w[1])+'\n')
        for w in res:
            f.write(w+' ')
        f.close()

def main():
    ob = MT("en.low", "hi.low", "117-04-05.150135.sumit.")
    ob.train()
main()
