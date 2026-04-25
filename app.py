import streamlit as st
from utils.audio_manager import play_bgm_from_folder

play_bgm_from_folder("basic_bgm")

st.set_page_config(
    page_title="포켓몬 서바이벌 앱",
    page_icon="⚡",
    layout="centered"
)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = ""
    

# 메인 화면 UI 구성

st.title("⚡ 포켓몬 서바이벌 퀴즈 앱")
st.write("Python과 Streamlit을 활용하여 개발한 인터랙티브 웹 애플리케이션입니다.")

if st.session_state['logged_in']:
    st.success(f"현재 **{st.session_state['current_user']}**님으로 로그인되어 있습니다. 왼쪽 퀴즈 메뉴로 이동해 게임을 시작하세요!")
else:
    st.info("👈 왼쪽 메뉴에서 **회원가입** 또는 **로그인**을 먼저 진행해 주세요.")
    
st.write("---")

st.subheader("학번 : 2020803066")
st.subheader("이름 : 신의철 ")

