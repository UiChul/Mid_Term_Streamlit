import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.audio_manager import play_bgm_from_folder

from utils.auth import hash_pattern
from utils.data_manager import load_users

play_bgm_from_folder("basic_bgm")
st.set_page_config(page_title="로그인", page_icon="🔐")
st.title("🔐 로그인")
st.write("아이디 입력 후 설정하신 비밀번호를 클릭해 주세요.")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = ""
if 'login_code' not in st.session_state:
    st.session_state['login_code'] = []

if st.session_state['logged_in']:
    # 저장된 이름(current_user)으로 따뜻하게 맞이합니다.
    st.success(f"환영합니다, {st.session_state['current_user']}님! 성공적으로 로그인되었습니다.")
    st.info("👈 왼쪽 사이드바에서 퀴즈 페이지로 이동해 보세요!")
    
    if st.button("로그아웃"):
        st.session_state['logged_in'] = False
        st.session_state['current_user'] = ""
        st.rerun()
else:
    login_id = st.text_input("아이디 입력")
    st.write("---")
    st.subheader("📱 비밀번호 입력")
    
    pad_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']

    p_cols = st.columns(3)
    for i, key in enumerate(pad_keys):
        if p_cols[i % 3].button(key, key=f"login_btn_{key}"):
            st.session_state['login_code'].append(key)
            st.rerun()

    if st.session_state['login_code']:
        path_str = " ➡️ ".join(st.session_state['login_code'])
        st.write(f"입력 중: **[ {path_str} ]**")
    else:
        st.write("비밀번호를 입력해 주세요.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 재입력"):
            st.session_state['login_code'] = []
            st.rerun()
            
    with col2:
        if st.button("🔓 로그인", type="primary"):
            if not login_id:
                st.warning("아이디를 먼저 입력해 주세요.")
            elif not st.session_state['login_code']:
                st.warning("비밀번호를 입력해 주세요.")
            else:
                users = load_users()
                user = users.get(login_id)
                
                # password_hash로 키 값 변경 확인
                if user and user['password_hash'] == hash_pattern(st.session_state['login_code']):
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = user['name'] # 이름 저장!
                    st.session_state['login_code'] = [] 
                    st.rerun()
                else:
                    st.error("아이디가 존재하지 않거나 비밀번호가 일치하지 않습니다.")
                    st.session_state['login_code'] = []