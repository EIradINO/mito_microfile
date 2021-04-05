from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import itertools
import numpy as np

word_list = []
text = "どうして空は青いのかがが気になりました"
char_filters = [UnicodeNormalizeCharFilter()]
tokenizer = Tokenizer()
token_filters = [POSKeepFilter(['名詞', '形容詞'])]
analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)
for token in analyzer.analyze(text):
    word_list.append(token.surface)
#print(word_list)

data_list = ["空の色が青い理由",
             "曇り空を見てみよう",
             "赤・青・緑 - 光の三原色",
             "葉っぱが緑色なのはなぜ？",
             "なぜ空は青いのか？",
             "帰り道の空が気になる豆知識"]

results = []
for word in word_list:
    results.append([s for s in data_list if word in s])

#print(results)

kekka = []
for xx in itertools.combinations(results, 2):
    kyotu = set(xx[0]) & set(xx[1])
    if kyotu:
        kekka.append(list(kyotu))
#print(list(itertools.chain.from_iterable(kekka)))

a = []
for count in data_list:
    a.append(list(itertools.chain.from_iterable(kekka)).count(count))

#print(a)
b = np.percentile(a, 75)
#print(np.percentile(a, 75))

for final in data_list:
    if list(itertools.chain.from_iterable(kekka)).count(final) >= b:
        print(final)
