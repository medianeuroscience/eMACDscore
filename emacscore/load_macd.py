import re, fnmatch
import warnings
import pandas as pd
import os
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define path for module to allow dict imports. 
fileDir = os.path.dirname(os.path.abspath(__file__))

# Load E-MAC
emac = pd.read_pickle(fileDir+'/dictionaries/emac_scoring.pkl')
probabilites = [c for c in emac.columns if c.endswith('_p')]
domains = ['fairness','group','deference','heroism', 'reciprocity', 'family', 'property']
senti = [c for c in emac.columns if c.endswith('_sent')]
emac = emac.T.to_dict()


# Load eMAC-all-vice-virtue
emac_all_vice_virtue = pd.read_pickle(fileDir+'/dictionaries/emac_all_vice_virtue.pkl')

# Load eMAC-single-vice-virtue
emac_single_vice_virtue = pd.read_pickle(fileDir+'/dictionaries/emac_single_vice_virtue.pkl')

# Load eMAC-single-sent
emac_single_sent = pd.read_pickle(fileDir+'/dictionaries/emac_single_sent.pkl')



# load macd_virtue
macd_virtue_file = fileDir+'/dictionaries/macdvirtue.dic'
nummap = dict()
macd_virtue = dict()
wordmode = True
with open(macd_virtue_file, 'r') as f:
    for line in f.readlines():
        ent = line.strip().split()
        if line[0] == '%':
            wordmode = not wordmode
        elif len(ent) > 0:
            if wordmode:
                wordkey = ' '.join([e for e in ent if e not in nummap.keys()])
                macd_virtue[wordkey] = [[nummap[e] for e in ent if e in nummap.keys()]]
            else:
                nummap[ent[0]] = ent[1]

macd_virtue = pd.DataFrame.from_dict(macd_virtue).T
macd_virtue['domain'] = macd_virtue[0]
del macd_virtue[0]
macd_virtue = macd_virtue.T.to_dict()


# load macd_vice
macd_vice_file = fileDir+'/dictionaries/macdvice.dic'
nummap = dict()
macd_vice = dict()
wordmode = True
with open(macd_vice_file, 'r') as f:
    for line in f.readlines():
        ent = line.strip().split()
        if line[0] == '%':
            wordmode = not wordmode
        elif len(ent) > 0:
            if wordmode:
                wordkey = ' '.join([e for e in ent if e not in nummap.keys()])
                macd_vice[wordkey] = [[nummap[e] for e in ent if e in nummap.keys()]]
            else:
                nummap[ent[0]] = ent[1]

macd_vice = pd.DataFrame.from_dict(macd_vice).T
macd_vice['domain'] = macd_vice[0]
del macd_vice[0]
macd_vice = macd_vice.T.to_dict()

macd_virtue_domains = ['VirtueFamily', 'VirtueGroup', 'VirtueReciprocity', 'VirtueHeroism',
                      'VirtueDeference', 'VirtueFairness', 'VirtueProperty']
macd_vice_domains = ['ViceFamily', 'ViceGroup', 'ViceReciprocity', 'ViceHeroism',
                      'ViceDeference', 'ViceFairness', 'ViceProperty']
macd_domains = macd_virtue_domains + macd_vice_domains
    
