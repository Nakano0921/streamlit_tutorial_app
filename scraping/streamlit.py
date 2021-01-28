import streamlit as st
import pandas as pd
import subprocess


st.title('分析アプリverStreamlit')

uploaded_file = st.sidebar.file_uploader("ファイルをアップロード", type='csv')

start_scraping = st.button("Let's scraping")
if start_scraping == True:
  scraping_file = ["python", "main.py", "スクレイピング中"]
  proc = subprocess.Popen(scraping_file)
  st.write('ただいまデータを取得しています')
  proc.communicate()
  st.write('データの取得が終了しました')
  
  
st.header('読み込み結果を表示')
if uploaded_file != None:
  df = pd.read_csv(uploaded_file)
  st.write(df)

  st.header('グラフで結果を表示')
  df = df['negaposi']
  st.line_chart(df)