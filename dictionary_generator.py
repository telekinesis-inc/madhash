import re
import hashlib
import json

import nltk
import pandas as pd
from nltk.corpus import wordnet as wn


nltk.download('brown')
tagged_words = nltk.corpus.brown.tagged_words()

with open('offensive.txt', 'r') as f:
    profanity = set(x.lower() for x in f.read().split('\n'))

value_counts = pd.Series((w.lower(), t) for w, t in tagged_words 
                         if len(w) == len(re.sub(r'[^a-zA-Z]','', w))
                         and len(w) > 2
                         and w.lower() not in profanity).value_counts()

df = pd.DataFrame(value_counts, columns=['count'])

tag_map = {
    'N': wn.NOUN,
    'J': wn.ADJ,
    'V': wn.VERB,
    'R': wn.ADV,
    'O': wn.NOUN
}

df['word'] = df.index.map(lambda x: x[0])
df['tag'] = df.index.map(lambda x: x[1])
df['type'] = df.tag.map(lambda x: x[0] if x[0] in tag_map else 'O')

lemmatize = nltk.stem.wordnet.WordNetLemmatizer().lemmatize

for typ in tag_map:
    df['lemma_'+ typ] = df.apply(lambda x: lemmatize(x.word, tag_map[typ]), axis=1)

for typ in tag_map:
    df['count_'+ typ] = df['lemma_'+ typ].map(df[df.type == typ].groupby('lemma_'+typ)['count'].sum()).fillna(0)

df['max_type'] = df.apply(lambda x: {x['count_'+t]: t for t in tag_map}[max(x['count_'+t] for t in tag_map)][-1], axis=1)
df['max_lemma'] = df.apply(lambda x: x['lemma_'+ x.max_type], axis=1)
df['max_count'] = df.apply(lambda x: x['count_'+ x.max_type], axis=1)

df_clean = df.groupby('max_lemma')[['max_type','max_count']].first().sort_values('max_count', ascending=False)

exp_map = {
    'N': 12,
    'V': 11,
    'J': 10,
    'R': 9
}

out = {t: sorted(list(df_clean[df_clean.max_type == t].head(2**exp_map[t]).index)) for t in exp_map}

with open('public/dictionary.json', 'w') as f:
    json.dump(out, f)
