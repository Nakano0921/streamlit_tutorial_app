import streamlit as st
import pandas as pd
import statistics


st.title('AIを活用したクチコミ分析')
st.write('ファイルをアップロードすると評価一覧がみれます。')

uploaded_file = st.sidebar.file_uploader("ファイルをアップロード", type='csv')

if uploaded_file != None:
  st.header('読み込み結果を表示')
  df = pd.read_csv(uploaded_file)
  df = df.drop(columns=df.columns[[0]])
  st.write(df)

  negaposi_df = df['negaposi']

  ave_button = st.button('ネガポジの平均点を表示する')
  if ave_button == True:
    ave_score = statistics.mean(negaposi_df)
    ave_score = str(round(ave_score, 2))
    st.header(f'平均点は{ave_score}点です')
