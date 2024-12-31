import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction import text
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.language import Language
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from collections import Counter
import numpy as np
import json
import re

try:
    nltk_stopwords = stopwords.words('english')
except:
    print('NLTK stopwords missing, downloading now.')
    nltk.download('stopwords')
    nltk_stopwords = stopwords.words('english')
stopwords = set(list(nltk_stopwords) + list(text.ENGLISH_STOP_WORDS) + list(STOP_WORDS))
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
nlp = English()
tokenizer = Tokenizer(nlp.vocab)
from spacy.lang.en import English
nlp = English()

import progressbar
from emacscore.load_macd import *



@Language.component("emac_tokenizer")
def tokenizer(doc):
    
    """Performs minimal preprocessing on textual document.
    Steps include tokenization, lower-casing, and 
    stopword/punctuation/whitespace removal. 
    Returns list of processed tokens"""
    
    return [x.lower_ for x in doc if x.lower_ not in stopwords and not x.is_punct and not x.is_digit and not x.is_quote and not x.like_num and not x.is_space]



@Language.component("score_macd")
def score_macd(doc):
    
    doc = str(doc)
    doc = re.sub('\s+',' ',doc)
    doc = doc.lower().strip()
    
    macd_score = {k:0 for k in macd_domains}
    virtue_domain = [domain for token in macd_virtue.keys() if len(re.findall('\\b{}\\b'.format(token), doc)) == 1 for domain in macd_virtue[token]['domain']]
    
    vice_domain = [domain for token in macd_vice.keys() if len(re.findall('\\b{}\\b'.format(token), doc)) == 1 for domain in macd_vice[token]['domain']]
    
    moral_words = virtue_domain+vice_domain
    f_counts = Counter(moral_words)
    macd_score.update(f_counts)


    if len(moral_words) != 0:
        macd_score = {k: v/len(moral_words) for k,v in macd_score.items()}
        nonmoral_words = len(doc.split(' '))-len(moral_words)
        try:
            macd_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            macd_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    else:
        macd_score = {k: 0 for k in macd_domains}
        nonmoral_words = len(doc.split(' ')) - len(moral_words)
        try:
            macd_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            macd_score['moral_nonmoral_ratio'] = len(moral_words) / 1

    return macd_score


@Language.component("score_emac_all_sent")
def score_emac_all_sent(doc):
  
    emac_score = {k: 0 for k in probabilites+senti}
    moral_words = [emac[token] for token in doc if token in emac.keys()]
    
    for dic in moral_words:
        emac_score['fairness_p'] += dic['fairness_p']
        emac_score['group_p'] += dic['group_p']
        emac_score['deference_p'] += dic['deference_p']
        emac_score['heroism_p'] += dic['heroism_p']
        emac_score['reciprocity_p'] += dic['reciprocity_p']
        emac_score['family_p'] += dic['family_p']
        emac_score['property_p'] += dic['property_p']
        
        emac_score['fairness_sent'] += dic['fairness_sent']
        emac_score['group_sent'] += dic['group_sent']
        emac_score['deference_sent'] += dic['deference_sent']
        emac_score['heroism_sent'] += dic['heroism_sent']
        emac_score['reciprocity_sent'] += dic['reciprocity_sent']
        emac_score['family_sent'] += dic['family_sent']
        emac_score['property_sent'] += dic['property_sent']


    if len(moral_words) != 0:
        emac_score = {k: v/len(moral_words) for k, v in emac_score.items()}
        nonmoral_words = len(doc)-len(moral_words)
        try:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    else:
        emac_score = {k: 0 for k in probabilites_emac + senti_emac}
        nonmoral_words = len(doc) - len(moral_words)
        try:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    
    return emac_score


@Language.component("score_emac_single_sent")
def score_emac_single_sent(doc):
    
    """Scores documents with eMACD, where each word is assigned one probability and the associated average sentiment score."""

    # Initiate dictionary to store scores
    emac_score = {k: 0 for k in probabilites+senti}

    # Collect e-MACD data for all moral words in document
    moral_words = [emac_single_sent[token] for token in doc if token in emac_single_sent.keys()]
    
    for dic in moral_words:
        base_f = dic['foundation'].split('_')[0]
        emac_score[dic['foundation']] += dic['score']
        emac_score[base_f+'_sent'] += dic['sentiment']
        
      
    if len(moral_words) != 0:
        emac_score = {k: v/len(moral_words) for k, v in emac_score.items()}
        nonmoral_words = len(doc)-len(moral_words)
        try:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    else:
        emac_score = {k: 0 for k in probabilites + senti}
        nonmoral_words = len(doc) - len(moral_words)
        try:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    
    return emac_score



@Language.component("score_emac_all_vice_virtue")
def score_emac_all_vice_virtue(doc):
    
    """Scores documents with the eMAC, where each word is assigned ten vice-virtue scores."""
    
    mac_domains = ['fairness.virtue', 'group.virtue', 'deference.virtue',
       'heroism.virtue','reciprocity.virtue', 'family.virtue', 'property.virtue',
       'fairness.vice', 'group.vice', 'deference.vice',
       'heroism.vice','reciprocity.vice', 'family.vice', 'property.vice']

    # Initiate dictionary to store scores
    emac_score = {k: 0 for k in mac_domains} ##define in load_py

    # Collect e-MACD data for all moral words in document
    moral_words = [emac_all_vice_virtue[token] for token in doc if token in emac_all_vice_virtue.keys()]
    
    for dic in moral_words:
        for f in mac_domains:
            if f != 'moral':
                emac_score[f] += dic[f]
        
    if len(moral_words) != 0:
        emac_score = {k: v/len(moral_words) for k, v in emac_score.items()}
        nonmoral_words = len(doc)-len(moral_words)
        try:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    else:
        emac_score = {k: 0 for k in mac_domains}
        nonmoral_words = len(doc) - len(moral_words)
        try:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    
    return emac_score


@Language.component("score_emac_single_vice_virtue")
def score_emac_single_vice_virtue(doc):
    
    """Scores documents with the eMACD, where each word is assigned one vice-virtue score."""
    
    mac_domains = ['fairness.virtue', 'group.virtue', 'deference.virtue',
       'heroism.virtue','reciprocity.virtue', 'family.virtue', 'property.virtue',
       'fairness.vice', 'group.vice', 'deference.vice',
       'heroism.vice','reciprocity.vice', 'family.vice', 'property.vice']

    # Initiate dictionary to store scores
    emac_score = {k:0 for k in mac_domains if k !='moral'}

    # Collect e-MACD data for all moral words in document
    moral_words = [emac_single_vice_virtue[token] for token in doc if token in emac_single_vice_virtue.keys()]
    
    for dic in moral_words:
        emac_score[dic['foundation']] += dic['score']

    if len(moral_words) != 0:
        emac_score = {k: v/len(moral_words) for k, v in emac_score.items()}
        nonmoral_words = len(doc)-len(moral_words)
        try:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    else:
        emac_score = {k: 0 for k in mac_domains}
        nonmoral_words = len(doc) - len(moral_words)
        try:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / nonmoral_words
        except ZeroDivisionError:
            emac_score['moral_nonmoral_ratio'] = len(moral_words) / 1
    
    return emac_score


def score_docs(csv, dic_type, prob_map, score_type, out_metrics, num_docs):
    
    """Wrapper function that executes functions for preprocessing and dictionary scoring.
    dict_type specifies the dicitonary with which the documents should be scored.
    Accepted values are: [macd, emacd]"""

    if score_type == 'wordlist':
        widgets = [
            'Processed: ', progressbar.Counter(),
            ' ', progressbar.Percentage(),
            ' ', progressbar.Bar(marker='❤'),
            ' ', progressbar.Timer(),
            ' ', progressbar.ETA(),
        ]

        with progressbar.ProgressBar(max_value=num_docs, widgets=widgets) as bar:
            moral_words = []
            for i, row in csv[0].iteritems():
                if row in emac.keys():
                    moral_words.append(emac[row])
                else:
                    bar.update(i)
                    continue
        

            emac_score = {k: 0 for k in probabilites+senti}

            # Collect e-MAC data for all moral words in document
            for dic in moral_words:
                emac_score['fairness_p'] += dic['fairness_p']
                emac_score['group_p'] += dic['group_p']
                emac_score['deference_p'] += dic['deference_p']
                emac_score['heroism_p'] += dic['heroism_p']
                emac_score['reciprocity_p'] += dic['reciprocity_p']
                emac_score['family_p'] += dic['family_p']
                emac_score['property_p'] += dic['property_p']

                emac_score['fairness_sent'] += dic['fairness_sent']
                emac_score['group_sent'] += dic['group_sent']
                emac_score['deference_sent'] += dic['deference_sent']
                emac_score['heroism_sent'] += dic['heroism_sent']
                emac_score['reciprocity_sent'] += dic['reciprocity_sent']
                emac_score['family_sent'] += dic['family_sent']
                emac_score['property_sent'] += dic['property_sent']
                bar.update(i)

            emac_score = {k: v/len(moral_words) for k, v in emac_score.items()}
            emac_score['cnt'] = len(moral_words)
            df = pd.DataFrame(pd.Series(emac_score)).T
            df = df[['cnt']+probabilites+senti]
            return df

    nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser'])
    nlp.add_pipe("emac_tokenizer")
    
    if dic_type == 'emac':
        if (prob_map == 'all') & (out_metrics == 'sentiment'):
            nlp.add_pipe("score_emac_all_sent", last=True)
        elif (prob_map == 'all') & (out_metrics == 'vice-virtue'):
            nlp.add_pipe("score_emac_all_vice_virtue", last=True)
        elif (prob_map == 'single') & (out_metrics == 'sentiment'):
            nlp.add_pipe("score_emac_single_sent", last=True)
        elif (prob_map == 'single') & (out_metrics == 'vice-virtue'):
            nlp.add_pipe("score_emac_single_vice_virtue", last=True)
            
    elif dic_type == 'macd':
        nlp.remove_pipe("emac_tokenizer")
        nlp.add_pipe("score_macd", last=True)
    else:
        print('Dictionary type not recognized. Available values are: emac, macd')
        return 

    scored_docs = []
    widgets = [
        'Processed: ', progressbar.Counter(),
        ' ', progressbar.Percentage(),
        ' ', progressbar.Bar(marker='❤'),
        ' ', progressbar.Timer(),
        ' ', progressbar.ETA(),
    ]
    
    

    with progressbar.ProgressBar(max_value=num_docs, widgets=widgets) as bar:
        for i, row in csv[0].items():
            scored_docs.append(nlp(row))
            bar.update(i)


    df = pd.DataFrame(scored_docs)
    
    if dic_type == 'emac':
        if prob_map == 'all' and out_metrics == 'sentiment':
            df['f_var'] = df[probabilites].var(axis=1)
            df['sent_var'] = df[senti].var(axis=1)
        elif prob_map == 'single' and out_metrics == 'sentiment':
            df['f_var'] = df[probabilites].var(axis=1)
            df['sent_var'] = df[senti].var(axis=1)
        elif prob_map == 'all' and out_metrics == 'vice-virtue':
            mac_domains = ['fairness.virtue', 'group.virtue', 'deference.virtue',
                   'heroism.virtue','reciprocity.virtue', 'family.virtue', 'property.virtue',
                   'fairness.vice', 'group.vice', 'deference.vice',
                   'heroism.vice','reciprocity.vice', 'family.vice', 'property.vice']
            df['f_var'] = df[mac_domains].var(axis=1)
            #del df['moral']
        elif prob_map == 'single' and out_metrics == 'vice-virtue':
            mac_domains = ['fairness.virtue', 'group.virtue', 'deference.virtue',
                   'heroism.virtue','reciprocity.virtue', 'family.virtue', 'property.virtue',
                   'fairness.vice', 'group.vice', 'deference.vice',
                   'heroism.vice','reciprocity.vice', 'family.vice', 'property.vice']
            df['f_var'] = df[mac_domains].var(axis=1)
            
    if dic_type == 'macd':
        # Calculate variance
        mac_domains = ['VirtueFamily', 'VirtueGroup', 'VirtueReciprocity', 'VirtueHeroism',
                       'VirtueDeference', 'VirtueFairness', 'VirtueProperty',
                       'ViceFamily', 'ViceGroup', 'ViceReciprocity', 'ViceHeroism', 
                       'ViceDeference', 'ViceFairness', 'ViceProperty']
        
        df['f_var'] = df[mac_domains].var(axis=1)
        
    return df
