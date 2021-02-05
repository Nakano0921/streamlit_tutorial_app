import streamlit as st
import pandas as pd
import subprocess


st.title('AIを活用したクチコミ分析')

uploaded_file = st.sidebar.file_uploader("ファイルをアップロード", type='csv')

start_scraping = st.button("Let's scraping")
if start_scraping == True:
  scraping_file = ["python", "main.py", "スクレイピング中"]
  proc = subprocess.Popen(scraping_file)
  st.write('ただいまデータを取得しています')
  proc.communicate()
  st.write('データの取得が終了しました')
  
restaurant_title = st.text_input('レストラン名：')
res_title = restaurant_title
res_scraping = st.button('このレストランでデータを取得する')
if res_scraping == True:
  scraping_file = ["python", "main.py", "スクレイピング中"]
  proc = subprocess.Popen(scraping_file)
  st.write('ただいまデータを取得しています')
  proc.communicate()
  st.write('データの取得が終了しました')
  



if uploaded_file != None:
  st.header('読み込み結果を表示')
  df = pd.read_csv(uploaded_file)
  st.write(df)

  st.header('グラフで結果を表示')
  df = df['negaposi']
  st.line_chart(df)