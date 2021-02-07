import streamlit as st
import pandas as pd
import statistics
import seaborn as sns
import matplotlib.pyplot as plt


st.title('AIを活用したクチコミ分析')
st.write('ファイルをアップロードすると評価一覧がみれます。')

uploaded_file = st.sidebar.file_uploader("ファイルをアップロード", type='csv')

if uploaded_file != None:
  st.header('「Ritz Carlton ロカンダ」の評価一覧')
  df = pd.read_csv(uploaded_file)
  df = df.drop(columns=df.columns[[0]])
  st.write(df)

  negaposi_df = df['negaposi']

  soukan_button = st.button('特徴毎の相関を見る')
  if soukan_button == True:
    soukan_df = df.drop(columns=df.columns[0])
    soukan_df = soukan_df.corr()
    st.write(soukan_df)
    fig, ax = plt.subplots(figsize=(10,10))
    soukan_df = sns.heatmap(soukan_df,  annot=True, ax=ax)
    st.subheader('相関をヒートマップで表示')
    st.pyplot(fig)

  ave_button = st.button('このお店のネガポジの平均点を表示する')
  if ave_button == True:
    ave_score = statistics.mean(negaposi_df)
    ave_score = str(round(ave_score, 2))
    st.header(f'平均点は{ave_score}点です')



compar_button = st.radio('平均点を比較する', ('イタリアン', '12,000円〜15,000円', '京都'))
if compar_button == 'イタリアン':
  st.subheader('イタリアンの平均点は0.43点です')
if compar_button == '12,000円〜15,000円':
  st.subheader('価格帯が12,000円から15,000円のお店の平均点は0.5点です')
if compar_button == '京都':
  st.subheader('京都の飲食店の平均点は0.52点です')
