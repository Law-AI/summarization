import spacy
from spacy.attrs import ORTH
import re
import string

def custom_sentencizer(doc):
    ''' Look for sentence start tokens by scanning for periods only. '''
    split_lowercase = all(w.text.islower() for w in doc)
    
    for i, token in enumerate(doc[:-2]):  # The last token cannot start a sentence
        if token.text[0] == "." or token.text[-1] == ".":
            if not split_lowercase and (not doc[i+1].text[0].isupper() or doc[i+2].text[0] == '.'):# or doc[i+1].text[0] == '.':
                    doc[i+1].is_sent_start = False  # Tell the default sentencizer to ignore this token
            # pass
        else:
            doc[i+1].is_sent_start = False  # Tell the default sentencizer to ignore this token
    return doc




def custom_splitter(text = None):
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe(custom_sentencizer, before = "parser")

    special_cases = {"Rs.": "rs.", "No.": "no.", "no.": "no.", "v.": "vs", "vs.": "vs", "i.e.": "i.e.", "viz.": "viz.", "M/s.": "m/s.", "Mohd.": "mohd.", "Ex.": "exhibit", "Art." : "article", "Arts." : "articles", "S.": "section", "s.": "section", "ss.": "sections", "u/s.": "section", "u/ss.": "sections", "art.": "article", "arts.": "articles", "u/arts." : "articles", "u/art." : "article", "hon'ble" : "honourable"}
    
    for case, orth in special_cases.items():
    	nlp.tokenizer.add_special_case(case, [{ORTH: orth}])
    
    
    if text is None: return nlp
    #text = text.strip()
    #print (text)
    text = text.replace('\n', ' ')
    #text = re.sub(' +', ' ', text)
    
    
    
    parsed = nlp(text)
    
    sentences = []
    
    for sent in parsed.sents:
        sentences.append(sent.text)
    
    return sentences, nlp




class custom_tokenizer:
        def __init__(self):
                # self.NLP = spacy.load('en_core_web_sm')
                self.NLP = custom_splitter()
                puncts = string.punctuation.replace('.', '').replace('-', '')
                self.trans = str.maketrans('.-','  ', puncts)
                
        def to_words(self, text):
                text = re.sub('\n', ' ', text.lower())
                text = re.sub('\s+', ' ', text).strip()
                
                words = [s.text.lower() if s.text[0] == "'" and len(s.text) == 2 else s.text.translate(self.trans).strip().lower() for s in self.NLP(text.strip()) if not s.is_punct]
                
                return words 
        
        def to_sentences(self, text):
                #remove extra dots
                text = re.sub('\.\s*\.\s*\.', '. ', text)
                text = re.sub('\.\s*\.', '. ', text)
                
                #remove dash
                text = re.sub('-', ' ', text)
                
                # remove extra whitespace
                text = re.sub('\n', ' ', text)
                text = re.sub('\s+', ' ', text).strip()
                
                
                
                sentences = [s.text for s in self.NLP(text).sents if len(s.text.strip()) > 5]
                # if re.match('\d+\.?.*', text):
                #         text = text[4:]
                
                return sentences
        
        def to_cleaned_sents(self, text):
                sents = self.to_sentences(text)
                words = [' '.join(self.to_words(s)) + '.' for s in sents]
                return words        
        
       
        
       
        
class simple_tokenizer:
        def to_words(self, s):
                s = s.strip().strip('.').strip()
                return s.split()
        
        def to_sentences(self, s):
                return [sent.strip() + '.' for sent in s.split('.') if len(sent.strip()) > 5]
