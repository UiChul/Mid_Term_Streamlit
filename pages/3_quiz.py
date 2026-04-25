import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils.audio_manager import play_bgm_from_folder

import random
import time
from utils.data_manager import get_rankings, save_ranking
play_bgm_from_folder("quiz_bgm")

st.set_page_config(page_title="포켓몬 퀴즈", page_icon="⚡")

# # 1. 로그인 확인
# if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#     st.warning("로그인이 필요한 서비스입니다. 왼쪽 메뉴에서 먼저 로그인해 주세요.")
#     st.stop()

st.title("⚡ 실시간 포켓몬 도감 퀴즈!")
st.write(f"환영합니다, **{st.session_state.get('current_user', '트레이너')}**님! 당신의 포켓몬 지식을 테스트해 보세요.")

if 'game_over' not in st.session_state:
    st.session_state.update({
        'game_over': False,
        'correct_count': 0,
        'current_pokemon': None,
        'ranking_saved': False
    })

# 이미지 폴더 경로
IMAGE_DIR = "pokemon_data" 

# 캐싱 적용-
@st.cache_data
def load_pokemon_images():
    
    if not os.path.exists(IMAGE_DIR):
        return []
    return [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg'))]

pokemon_files = load_pokemon_images()

def next_question():

    st.session_state['current_pokemon'] = random.choice(pokemon_files)

if st.session_state['current_pokemon'] is None and not st.session_state['game_over']:
    next_question()
    
# 게임 종료

if st.session_state['game_over']:
    current_file = st.session_state['current_pokemon']
    correct_name = current_file.split('.')[0].split('_')[1]
    
    # 틀렸을 때
    st.error(f"## ❌ 아쉽습니다! \n ##   정답은 **[{correct_name}]** 입니다.")
    st.warning(f"🏆 최종 기록: **{st.session_state['correct_count']}마리** 연속 정답")
    
    # 전당 등록 영역
    if not st.session_state['ranking_saved']:
        st.write("---")
        st.subheader("전당 등록")
        user_id = st.text_input("전당에 기록될 이름을 입력하세요", value=st.session_state.get('current_user', ''))
        
        if st.button("내 기록 저장하기", type="primary"):
            save_ranking(user_id, st.session_state['correct_count'])
            st.session_state['ranking_saved'] = True
            st.success("전당 등록이 완료되었습니다!")
            st.rerun()
    
    # 📊 랭킹판 표시
    st.write("---")
    st.subheader("📊 Top 10 전당")
    rankings = get_rankings()[:10]
    for i, r in enumerate(rankings):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"**{i+1}위**"
        st.write(f"{medal} &nbsp;&nbsp; {r['id']} &nbsp;({r['count']}마리)")
    
    st.write("---")
    if st.button("🔄 다시 도전하기"):
        st.session_state.update({'game_over': False, 'correct_count': 0, 'current_pokemon': None, 'ranking_saved': False})
        next_question()
        st.rerun()
        
    st.stop()

# 퀴즈 진행 

current_file = st.session_state['current_pokemon']
correct_name = current_file.split('.')[0].split('_')[1]

col1, col2 = st.columns([3, 1])
with col1:
    st.write("틀리면 바로 탈락입니다. 신중하게 입력하세요!")
with col2:
    st.metric("현재 맞춘 갯수", f"{st.session_state['correct_count']} 마리")

image_path = os.path.join(IMAGE_DIR, current_file)

st.image(image_path, width=300)

# 정답 입력 
with st.form("answer_form", clear_on_submit=True):
    user_answer = st.text_input("이 포켓몬의 이름은 무엇일까요?")
    submitted = st.form_submit_button("정답 확인")

if submitted:
    if not user_answer:
        st.warning("이름을 입력해 주세요!")
    elif user_answer.strip() == correct_name:
        # 정답
        st.success("## ⭕ 정답입니다!")
        time.sleep(0.8)
        
        st.session_state['correct_count'] += 1
        next_question()
        st.rerun()
    else:
        # 오답 
        st.session_state['game_over'] = True
        st.rerun()