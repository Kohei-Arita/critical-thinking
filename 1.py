import streamlit as st
import openai
import os

# 環境変数からAPIキーを取得
# APIキーの設定
# APIキーを環境変数から取得
api_key = os.environ.get("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")
openai.api_key = api_key


# Streamlitアプリの設定
st.title('AIクリティカルシンキングアシスタント')

# セッション内で使用するモデルが指定されていない場合のデフォルト値
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

# セッション内のメッセージが指定されていない場合のデフォルト値
if "messages" not in st.session_state:
    st.session_state.messages = []

# ユーザーからの新しい入力を取得
user_input = st.text_input("セントラルクエスチョンを入力してください:")

# ユーザーが入力を行った場合の処理
if user_input:
  with st.spinner('回答を考えています...'):
    # プロンプトの設定

    prompt = """
#命令書
あなたには今からイシューツリーを作ってもらいます。
作り方は下記の例を参考にしてください。

#制約条件
・ユーザーがセントラルクエスチョンを入力するのでそれに対するイシューツリー(論点構造)を作成してください。
・フォーマットは必ず出力例に従ってください。必ず、1, 1-1,1-1-1,・の粒度まで作成してください。
・サブ論点は3つ設定してください。
・出力する時は出力例に倣って、一行づつ改行をしてください。

#入力例
Fundoxが事業を成長させるためにはどうすればいいか？

#出力例
セントラルクエスチョン:

Foodboxが事業を成功させるためにはどうすればいいか？

サブ論点1:

利用顧客数を増やすにはどうすればいいか？

1-1. デマンドをどうすればいいか？
1-1-1. プロダクトをどのように改善するか？
・顧客のペインポイントは何か
・競合はどのような機能を提供しているか
・自社の差別化要素は何か
1-1-2. どの集客チャネルに注力するべきか？
・直接獲得の効率性はどの程度か？
・関連機能を通じた獲得の効率性はどの程度か？
1-1-3. 最適な価格設定は？
・顧客の価格弾力性は？
・支払サイト別にどう設定するか？
1-1-4.最適なプロモーションは？
・マーケターゲットは？
・チャネルは？

1-2.サプライをどう増やすか？
1-2-1.資金力をどう増やすか？
・エクイティとデットのバランスは？
・どのように調達するか？
・調達コストの上限は？

サブ論点2:平均利用金額を増やすにはどうすればいいか？
1-1. 定量指標で分解するとどこが良いか？
1-1-1. 売り上げ規模別にどこがいいか？
・10億円以下
・10億円~100億円
・100億円以上
1-1-2. 売上債権本回転率別にどこが良いか？
・~10%
・10%~50%
・50%以上
1-2.定性指標で分解するとどこがいいか？
1-2-1.業態別にどこがいいか？
・製造業
・卸売業
・IT関連
1-2-2.会社のステージ別にどこがいいか？
・スタートアップ
・中小企業
・大企業

#ユーザーの入力:
 """ + user_input

    response = openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )

    # APIからのレスポンスを表示
    if response.choices:
        assistant_message = response.choices[0].message.get('content')
        st.write("AIの分析結果: ", assistant_message)
    else:
        st.write("エラーが発生しました。")

# チャット履歴をクリアするボタンが押されたら、メッセージをリセット
if st.button('チャット履歴をクリア'):
    st.session_state.messages = [] # メッセージのリセット
    st.experimental_rerun() # 画面を更新
