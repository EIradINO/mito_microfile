from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
import itertools
import numpy as np

# 要素を形態素解析し、名詞と形容詞をリストにまとめる
word_list = []
text = "どうして空は青いのかがが気になりました"
char_filters = [UnicodeNormalizeCharFilter()]
tokenizer = Tokenizer()
token_filters = [POSKeepFilter(['名詞', '形容詞'])]
analyzer = Analyzer(char_filters=char_filters,
                    tokenizer=tokenizer, token_filters=token_filters)
for token in analyzer.analyze(text):
    word_list.append(token.surface)

data_list = [["空の色が青い理由", "空の色が青い理由を解き明かします‼‼"],
             ["曇り空を見てみよう", "いろいろな形をした雲を紹介します"],
             ["赤・青・緑 - 光の三原色", "光の三原色とはなんでしょう"],
             ["葉っぱが緑色なのはなぜ？", "空が青い理由や葉っぱが緑色の理由、リンゴが赤く見える理由などを解説します"],
             ["なぜ空は青いのか？", "青い光は波長が短く、赤い光は波長が長いので、青い光ほど散乱される量が多いのです"],
             ["帰り道の空が気になる豆知識", "毎日の帰り道の空が気になる豆知識を紹介します。"]]

counter = [[], []]

# word_list内の単語とdata_listの文字列を突き合わせて、共通するものを単語ごとに書きだす
for i in range(2):
    # data_listi番目の要素を加工したリスト化する
    process_data_list = [data[i] for data in data_list]
    match_list = []
    for word in word_list:
        match_list.append([s for s in process_data_list if word in s])

# 単語ごとに紐づけられた文字列を4C2で総当たりで比べ、共通する単語がある場合はそれをfrequencyに格納する
    frequency = []
    for el in itertools.combinations(match_list, 2):
        common = set(el[0]) & set(el[1])
        if common:
            frequency.append(list(common))

# frequencyの中にどの文字列がどれくらい出てきたのかを数えて、counterに格納する。
    for count in process_data_list:
        counter[i].append(
            list(itertools.chain.from_iterable(frequency)).count(count))
# タイトルと説明文の一致点数をかける
sum_count = list(map(lambda x, y: x + y, counter[0], counter[1]))


# counterの上位25%を取り出す
criterion = np.percentile(sum_count, 75)
relation = np.percentile(sum_count, 50)


# data_list内の単語の出現回数が上位25%の場合出力する
process_data_list = [data[0] for data in data_list]
for i, results in enumerate(process_data_list):
    if sum_count[i] >= criterion:
        print("検索結果:" + results)
    elif sum_count[i] >= relation:
        print("関連情報:" + results)
