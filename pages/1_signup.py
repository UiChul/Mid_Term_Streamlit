import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from utils.auth import hash_pattern
from utils.data_manager import load_users, save_user

st.set_page_config(page_title="회원가입", page_icon="📝")
st.title("📝 회원가입")
st.write("정보를 입력하고 나만의 비밀번호를 설정해 주세요.")

if 'signup_code' not in st.session_state:
    st.session_state['signup_code'] = []

new_name = st.text_input("이름 (닉네임)", placeholder="홍길동")
new_id = st.text_input("아이디", placeholder="example123")

st.write("---")
st.subheader("📱 비밀번호 설정")
st.write("순서대로 버튼을 눌러 비밀번호를 만드세요. (중복 가능)")

pad_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#']

p_cols = st.columns(3)
for i, key in enumerate(pad_keys):
    if p_cols[i % 3].button(key, key=f"signup_btn_{key}"):
        st.session_state['signup_code'].append(key)
        st.rerun()

if st.session_state['signup_code']:
    path_str = " ➡️ ".join(st.session_state['signup_code'])
    st.write(f"현재 입력된 비밀번호: **[ {path_str} ]** (총 {len(st.session_state['signup_code'])}자리)")
else:
    st.write("버튼을 눌러 입력을 시작하세요.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔄 입력 초기화"):
        st.session_state['signup_code'] = []
        st.rerun()

with col2:
    if st.button("✅ 회원가입 완료", type="primary"):
        # 이름(new_name) 필수 입력 조건 추가
        if not new_name or not new_id or len(st.session_state['signup_code']) < 4:
            st.warning("이름과 아이디를 모두 입력하고 최소 4자리 이상의 비밀번호를 설정해 주세요.")
        else:
            users = load_users()
            if new_id in users:
                st.error("이미 존재하는 아이디입니다. 다른 아이디를 사용해 주세요.")
            else:
                user_data = {
                    "name": new_name, # 이름 데이터 다시 저장
                    "password_hash": hash_pattern(st.session_state['signup_code'])
                }
                save_user(new_id, user_data)
                st.success(f"🎉 {new_name}님, 가입이 완료되었습니다! 로그인 페이지로 이동하세요.")
                st.session_state['signup_code'] = []