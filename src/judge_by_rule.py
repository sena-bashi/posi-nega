import json
from janome.tokenizer import Tokenizer

pn_dict = {}

# 東北大学乾・岡崎研究室の日本語評価極性辞書（用言編）ver.1.0（2008年12月版）
with open("data/wago.121808.pn", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue
        
        parts = line.split("\t")
        if len(parts) >= 2:
            polarity, word = parts[0], parts[1]
        word = word.replace(" ", "")

        if "ポジ" in polarity:
            pn_dict[word] = 1
        elif "ネガ" in polarity:
            pn_dict[word] = -1
        else:
            pn_dict[word] = 0

# 東北大学乾・岡崎研究室の日本語評価極性辞書（名詞編）ver.1.0（2008年12月版）
with open("data/pn.csv.m3.120408.trim", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        
        if not line:
            continue
        
        parts = line.split("\t")
        if len(parts) >= 2:
            word, polarity = parts[0], parts[1]

        if polarity == "p":
            pn_dict[word] = 1
        elif polarity == "n":
            pn_dict[word] = -1
        elif polarity == "e":
            pn_dict[word] = 0
        else:
            pn_dict[word] = 0

# ポジネガ分類器本体
def polarity_classifier_by_rule(posts, pn_dict) -> None:
    t = Tokenizer()
    result = {}

    with open(posts, "r", encoding="utf-8") as f:
        data = json.load(f)
        posts = list(data.keys())

    for post in posts:
        token_dict = {}
        score = 0

        for token in t.tokenize(post):
            base = token.base_form
            if base == "*":
                base = token.surface

            if base in pn_dict:
                token_dict[base] = pn_dict[base]

        for v in token_dict.values():
            score += v

        if score >= 0:
            label = "pos"
        elif score < 0:
            label = "neg"
        else:
            raise Exception("scoreが正しく処理されていません")

        result[post] = label

    with open("output/result_by_rule.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
if __name__ == "__main__":
    polarity_classifier_by_rule("data/posts.json", pn_dict)