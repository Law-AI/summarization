import os
import json
import argparse
from multiprocessing import Pool
import string
import shutil

# external libraries
from numpy import argmax
from rouge import Rouge
from tqdm import tqdm



def ROUGE(hypsumm, refsumm):
        rouge = Rouge()
        rouge.metrics = ['rouge-2']
        rouge.stats = ['r']
        
        ref = '\n'.join(refsumm)
        hyp = '\n'.join(hypsumm)
        if len(hyp.strip()) < 10: return 0
        if len(ref.strip()) < 10: return 0
                
        scores = rouge.get_scores(hyp, ref, avg = True)
        return scores['rouge-2']['r']


def AVGROUGE(hypsumm, refsumm):
        rouge = Rouge()
        rouge.stats = ['f']
        
        ref = '\n'.join(refsumm)
        hyp = '\n'.join(hypsumm)
        if len(hyp.strip()) < 10: return 0
        if len(ref.strip()) < 10: return 0
        
        scores = rouge.get_scores(hyp, ref, avg = True)
        val = scores['rouge-1']['f'] + scores['rouge-2']['f'] + scores['rouge-l']['f']
        return val / 3


###########################################################################
# This class selects 'num_sents' sentences from the full text
# for each sentence in the summary wrt the highest average ROUGE scores.
# Ref: Narayan et.al. NAACL 2018. "Ranking sentences for extractive
# summarization with reinforcement learning"
###########################################################################
class AVGROUGEscorer:
        def __init__(self, judgesents, summsents):
                self.judgesents = judgesents
                self.summsents = summsents
                
                self.labels = [False for sent in judgesents]
        
        
        def getLabels(self, num_sent = 3):
                # [facets: [support groups: [sent indices]]]
                for sent in self.summsents:
                        # get scores with all judgesents
                        scores = list(map(lambda x: AVGROUGE([sent], [x]), self.judgesents))
                        # mark top labels
                        for i in range(num_sent):
                                index = int(argmax(scores))
                                self.labels[index] = True
                                scores[index] = -1
                        
                return self.labels

 

###########################################################################
# This class selects greedily selects the maximal sentences from full text
# to maximize ROUGE scores wrt the summary. 
# Ref: Nallapati et. al. AAAI 2017. "SummaRuNNer: A Recurrent Neural Network
# based Sequence Model for Extractive Summarization of Documents"
###########################################################################
class ROUGEscorer:
        def __init__(self, judgesents, summsents):
                self.judgesents = judgesents
                self.summsents = summsents
                
                self.currsents = []
                self.labels = [False for sent in judgesents]
        
        def score(self, i):
                if self.labels[i]: return 0
                t = self.judgesents[i]
                if len(t.translate(t.maketrans('', '', string.punctuation + string.whitespace))) < 5: return 0
                
                new = self.currsents + [self.judgesents[i]]
                score = ROUGE(new, self.summsents)
                return score
                
        def getmaxscore(self):
                # with Pool(N_PROCESS) as p:
                #         scores = p.map(self.score, range(len(self.judgesents)))
                #         p.close()
                #         p.terminate()
                
                scores = list(map(self.score, range(len(self.judgesents))))
                index = argmax(scores)
                return index, scores[index]
        
        def getLabels(self, min_labels = 10):
                currscore = 0.0
                while True:
                        # select sent index which maximises ROUGE
                        index, maxscore = self.getmaxscore()
                        if maxscore <= currscore and len(self.currsents) >= min_labels: break
                        
                        currscore = maxscore
                        self.currsents.append(self.judgesents[index])
                        self.labels[index] = True
                
                #print(len(self.currsents), len(self.judgesents))
                return self.labels
                
     
               

def prepare(judgepath, summarypath):
        
        with open(judgepath) as fp: 
                judgesents = fp.read().splitlines()
        with open(summarypath) as fp:
                summsents = fp.read().splitlines()
        
        
        data = {}
        # prepare doc
        data['doc'] = '\n'.join(judgesents)
        # prepare summ
        data['summaries'] = '\n'.join(summsents)
        

        scorer = MODEL(judgesents, summsents)
        labels = scorer.getLabels()
        
        # prepare labels
        data['labels'] = '\n'.join(map(lambda x: str(int(x)), labels))
        return data
                        
                        
        
def generateData(f):
        #print(f)
        try:
                d = prepare(os.path.join(JUDGEPATH, f), os.path.join(SUMMPATH, f))
                d['file'] = f
                assert len(d['doc'].splitlines()) == len(d['labels'].splitlines()), "INCORRECT Number of sentences and labels"
                with open(os.path.join(tmpdir, f), 'w') as fout:
                        json.dump(d, fout)
                        
                        
        except Exception as args:
                print("ERROR in", f)
                print(args)
        


#%% MAIN

if __name__ == '__main__':
        
        #PARAMS
        
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("base_dir", type=str, help="base directory where the other files and folders are present")
        
        parser.add_argument("--method", type=str, choices=['avg_rg', 'm_rg'], default="avg_rg", help="method to use for generating labels.")
        parser.add_argument("--separator", type=str, default="$$$", help="separator used in output docs, to separate between the text and labels.")
        parser.add_argument("--n_process", type=int, default=1, help="number of subprocesses to use (for parallel computation).")
        
        
        parser.add_argument("--judgement_dir", type=str, default="judgement", help="subdirectory containing the judgements.")
        parser.add_argument("--summary_dir", type=str, default="summary", help="subdirectory containing the summaries.")
        
        parser.add_argument("--tmp_dir", type=str, default="tmp", help="temporary directory where the files will be stored. This directory can be deleted after running.")
        parser.add_argument("--out_dir", type=str, default="labelled", help="subdirectory where the output will be stored.")
        parser.add_argument("--out_json", type=str, default="labelled.jsonl", help="json-line file where the output will be stored.")
        
        parser.add_argument("--remove_tmp", action='store_true', help="if given any existing files inside tmp_dir will be deleted first. Else they will be reused (they won't be calculated again).")
        
        
        args = parser.parse_args()
        BASE = args.base_dir
        
        JUDGEPATH = os.path.join(BASE, args.judgement_dir)
        SUMMPATH = os.path.join(BASE, args.summary_dir)
        
        OUTPATH_JSON = os.path.join(BASE, args.out_json)
        OUTPATH = os.path.join(BASE, args.out_dir)
        
        tmpdir = os.path.join(BASE, args.tmp_dir)
        
        METHOD = args.method
        
        if METHOD == 'avg_rg': MODEL = AVGROUGEscorer  
        elif METHOD == 'm_rg': MODEL = ROUGEscorer 
        
        SEP = args.separator
        
        KEEP_TMP = not args.remove_tmp
        N_PROCESS = args.n_process

        
        ###########################################################################
        # CODE STARTS
        
        if not KEEP_TMP:
                shutil.rmtree(tmpdir)
        
        if not os.path.exists(tmpdir): os.mkdir(tmpdir)
        
        files = set(next(os.walk(JUDGEPATH))[2])
        excludefiles = set(next(os.walk(tmpdir))[2])
        files = [f for f in (files - excludefiles)]# if int(f.split('.')[0]) <= 3500]
        
        
        if N_PROCESS > 1:
                with Pool(N_PROCESS) as p:
                        list(tqdm(p.imap_unordered(generateData, files), total = len(files)))
        
        else:
                list(tqdm(map(generateData, files), total = len(files)))
        
                

        files = next(os.walk(tmpdir))[2]
                
        if not os.path.exists(OUTPATH): os.mkdir(OUTPATH)
                        
        with open(OUTPATH_JSON, 'w') as fout:
                for f in tqdm(files):
                        with open(os.path.join(tmpdir, f)) as fp:
                                try: d = json.load(fp)
                                except: 
                                        os.system('rm ' + os.path.join(tmpdir, f))
                                        continue
                                
                                
                        with open(os.path.join(OUTPATH, f), 'w') as fout2:
                                for line, label in zip(d['doc'].split('\n'), d['labels'].split('\n')):
                                        print(line, SEP, label, sep = '', file = fout2)
                        
                        print(json.dumps(d), file = fout)
        