import streamlit as st
import pandas as pd
import statistics


st.title('AIを活用したクチコミ分析')
st.write('ファイルをアップロードすると評価一覧がみれます。')

uploaded_file = st.sidebar.file_uploader("ファイルをアップロード", type='csv')

if uploaded_file != None:
  st.header('「Ritz Carlton 水暉」の評価一覧')
  df = pd.read_csv(uploaded_file)
  df = df.drop(columns=df.columns[[0]])
  st.write(df)

  negaposi_df = df['negaposi']

  ave_button = st.button('ネガポジの平均点を表示する')
  if ave_button == True:
    ave_score = statistics.mean(negaposi_df)
    ave_score = str(round(ave_score, 2))
    st.header(f'平均点は{ave_score}点です')

compar_button = st.radio('平均点を比較する', ('和食', '12,000円〜15,000円', '京都'))
if compar_button == '和食':
  st.subheader('和食店の平均点は0.43点です')
if compar_button == '12,000円〜15,000円':
  st.subheader('価格帯が12,000円から15,000円のお店の平均点は0.5点です')
if compar_button == '京都':
  st.subheader('京都の飲食店の平均点は0.52点です')