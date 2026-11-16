# ポジネガ判定

1. タスクを定義
2. 2手法で比べる
3. 誤りを考察
- データは自作の投稿10件以上
    - 公開データは使わない
    - 判断に迷う投稿を2件以上入れる
    - 今回は15件用意する

## 手順1. 定義してルールで解く
### `src/judge_by_rule.py`

1. タスクを定義: 入出力とラベルを定義し、10件以上に正解を付ける 
- 入力は投稿文
    - `data/posts.json`を受け取る
        - 形式は、{"投稿文": 正解ラベル}
        - 正解ラベルは見ず、投稿文だけをリストとして取得する
- 出力は投稿文を key に、判定ラベルを value にした json で返す
    - `output/`に保存する
- ラベルは、ポジティブならば pos とし、ネガティブならば neg とする
2. ルールで解く: 単語リストで判定し、正解数を数える
- 形態素解析器で入力の投稿文を分かち書きし、得られた原形をポジネガ辞書(pn_dict)を用いて判定する
    - pn_dict は 東北大学乾・岡崎研が2008年に公開した日本語評価極性辞書をもとに作成する
        - https://www.cl.ecei.tohoku.ac.jp/Open_Resources-Japanese_Sentiment_Polarity_Dictionary.html
    - pn_dict は key を語、 value をラベルとする
    - pn_dict の value は、語がポジティブならば 1 とし、ネガティブならば -1 とし、それ以外ならば 0 とする
- 今回のルールでは、重みは考えない
- 原形を最初から順に確認し、出現した原形を key に、以下のルールによってつけられる値を value にした辞書(token_dict)を作る 
    - 確認した原形が pn_dict に含まれる key と一致し、その value が 1 であれば token_dict の value を 1 にする
    - 確認した原形が pn_dict に含まれる key と一致し、その value が -1 であれば　token_dict の value を -1 にする
    - 確認した原形が pn_dict に含まれる key と一致するが、その value が 0 であれば token_dict の value を 0 にする
    - 確認した原形が pn_dict のいずれの key とも一致しなければ token_dict の value を 0 にする
- 作った token_dict の value の合計(score)によってポジネガを判定する
    - score >= 0 ならば pos を返す
    - score < 0 ならば neg を返す
- 投稿文が key で、判定したラベルが value となる辞書(result)を作り、 json に変換して保存する
    - `output/result_by_rule.json`

## 手順2. LLMで解いて比べる
### `src/judge_by_llm.py`

3. LLMで解く: 同じデータをLLMで判定し、正解数を数える
- 日本語に対応した軽量なLLMを読み込み、 zero-shot で判定させる
- 判定に使用するモデルは、 Qwen/Qwen2.5-1.5B-Instruct を採用する
- 投稿文を1つずつ判定させ、ポジティブならば pos を、ネガティブならば neg を返す
- 投稿文が key で、判定ラベルが value となる辞書(result)を作り、 json に変換して保存する
    - `output/result_by_llm.json`
4. 比べて考える: 各手法の誤りを1件ずつ選び、理由を書く
- `report.md`に記載