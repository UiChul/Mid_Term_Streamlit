import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.audio_manager import play_bgm_from_folder


import pandas as pd
from utils.data_manager import get_rankings

play_bgm_from_folder("ranking_bgm")

st.set_page_config(page_title="명예의 전당", page_icon="🏆")

st.title("🏆 명예의 전당 ")
st.write("최고의 포켓몬 마스터는 누구일까요? 지금까지의 기록을 확인해 보세요.")

# 1. 랭킹 데이터 불러오기
rankings = get_rankings()

if not rankings:
    st.info("아직 등록된 랭킹이 없습니다. 첫 번째 전설의 트레이너가 되어보세요!")
    if st.button("게임 시작하러 가기"):
        st.switch_page("pages/3_quiz.py")
else:
    # 2. 상위 3명 강조 (Metric 활용)
    st.subheader("🥇 Top 3 트레이너")
    top_3 = rankings[:3]
    
    # 상위 3명을 가로로 배치
    cols = st.columns(3)
    medals = ["🥇 1st", "🥈 2nd", "🥉 3rd"]
    
    for i in range(3):
        if i < len(top_3):
            with cols[i]:
                st.metric(label=medals[i], value=f"{top_3[i]['count']}마리")
                st.write(f"**{top_3[i]['id']}** 트레이너")
        else:
            with cols[i]:
                st.write(f"{medals[i]}")
                st.caption("주인 없음")

    st.write("---")

    # 3. 전체 순위 리스트 (데이터 프레임 활용)
    st.subheader("📊 전체 순위")
    
    # Pandas를 사용하여 데이터 정제
    df = pd.DataFrame(rankings)
    df.index = df.index + 1  # 인덱스를 1부터 시작 (순위 표시)
    df.columns = ["아이디", "맞춘 개수"]
    
    # 테이블 형태로 깔끔하게 출력
    st.table(df)

    # 4. 부가 기능
    st.write("---")
    col_home, col_game = st.columns(2)
    
    with col_home:
        if st.button("🏠 홈 화면으로", use_container_width=True):
            st.switch_page("app.py")
            
    with col_game:
        if st.button("🎮 다시 도전하기", type="primary", use_container_width=True):
            st.switch_page("pages/3_quiz.py")