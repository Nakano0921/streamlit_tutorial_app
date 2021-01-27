import streamlit as st
import pandas as pd



st.title('分析アプリverStreamlit')

uploaded_file = st.sidebar.file_uploader("ファイルをアップロード", type='csv')

st.header('読み込み結果を表示')
if uploaded_file != None:
  df = pd.read_csv(uploaded_file)
  st.write(df)

  st.header('グラフで結果を表示')
  df = df['negaposi']
  st.line_chart(df)