import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# 標題
st.title('｜近6週熱門音樂｜')

# 上傳爬蟲資料
file_path = "final.xlsx"
df = pd.read_excel(file_path, index_col=0)

# 音樂類型
top_categories = ['請選一個類別'] + df['type'].value_counts().head(5).index.tolist()
selected_category = st.sidebar.selectbox("音樂類型🎸", top_categories)
selected_category_data = df[df['type'] == selected_category]

if selected_category == "請選一個類別":
    st.subheader("🏆 前5名的音樂類型")
    top5_categories = df['type'].value_counts().head(5)  # 只要前5種
    fig, ax = plt.subplots()
    ax.pie(top5_categories, labels=top5_categories.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
    st.markdown("")
    image_type = Image.open("type.png")
    st.image(image_type, caption="前5名類別播放次數與按讚數", use_column_width=True)
    image_wc = Image.open("WordCloud.jpg")
    st.image(image_wc, caption="留言文字雲", use_column_width=True)

else:
    music_count = len(selected_category_data)
    st.header(f"你選擇的是{selected_category} 總共有{music_count}首歌")

    # 計算出現最多次的創作者
    most_frequent_artist = selected_category_data['artist'].mode().iloc[0]
    most_frequent_artist_music = selected_category_data[selected_category_data['artist'] == most_frequent_artist]

    # 選擇歌手
    choose_artists = ['請選擇一位創作者'] + selected_category_data['artist'].unique().tolist()
    selected_artist = st.sidebar.selectbox("創作者🎤", choose_artists)
    selected_artist_music = selected_category_data[selected_category_data['artist'] == selected_artist]

    # 顯示出現最多次的創作者的上榜歌曲
    if selected_artist == '請選擇一位創作者' or len(selected_artist_music) == 0:
        st.subheader(f"{most_frequent_artist}出現最多次！")
        st.write(f"聽聽看他的歌吧🎧")

        displayed_songs = set()

        for i in range(len(most_frequent_artist_music)):
            col = st.columns(1)[0]

            if most_frequent_artist_music.iloc[i]["music"] not in displayed_songs:
                col.markdown(f'<div style="text-align: center;"><img src="{most_frequent_artist_music.iloc[i]["img"]}" use_column_width=True, width=200><br><a href="{most_frequent_artist_music.iloc[i]["link"]}" target="_blank">{most_frequent_artist_music.iloc[i]["music"]}</a></div>', unsafe_allow_html=True)
                displayed_songs.add(most_frequent_artist_music.iloc[i]["music"])
        st.text("")

    else:
        st.subheader(f"你選擇了{selected_artist}～")
        st.write(f"聽聽看他的歌吧🎧")

        displayed_songs = set()

        for i in range(len(selected_artist_music)):
            col = st.columns(1)[0]

            if selected_artist_music.iloc[i]["music"] not in displayed_songs:
                col.markdown(f'<div style="text-align: center;"><img src="{selected_artist_music.iloc[i]["img"]}" use_column_width=True, width=200><br><a href="{selected_artist_music.iloc[i]["link"]}" target="_blank">{selected_artist_music.iloc[i]["music"]}</a></div>', unsafe_allow_html=True)
                displayed_songs.add(selected_artist_music.iloc[i]["music"])
        st.text("")
