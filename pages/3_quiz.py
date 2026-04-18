import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import random
import time
from utils.data_manager import get_rankings, save_ranking

st.set_page_config(page_title="포켓몬 퀴즈", page_icon="⚡")

# 1. 로그인 여부 확인 (비로그인 접근 차단)
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

# 2. 이미지 폴더 경로 설정 (실제 폴더 경로에 맞게 수정하세요)
IMAGE_DIR = "pokemon_data" 

# --- 💡 과제 필수 요건: 캐싱 적용 부분 ---
@st.cache_data
def load_pokemon_images():
    """
    이미지 폴더를 읽어 파일 목록을 반환합니다.
    @st.cache_data를 적용하여, 버튼을 누를 때마다 폴더를 다시 읽는 성능 낭비를 막습니다.
    """
    if not os.path.exists(IMAGE_DIR):
        return []
    # .png 또는 .jpg 로 끝나는 파일만 가져옵니다.
    return [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg'))]

pokemon_files = load_pokemon_images()

def next_question():
    """다음 문제를 랜덤으로 뽑아 세션에 저장하는 함수"""
    st.session_state['current_pokemon'] = random.choice(pokemon_files)

# 최초 1회 문제 세팅
if st.session_state['current_pokemon'] is None and not st.session_state['game_over']:
    next_question()
    
# ==========================================
# 🚨 1. 게임 종료(틀림) 화면
# ==========================================
if st.session_state['game_over']:
    current_file = st.session_state['current_pokemon']
    correct_name = current_file.split('.')[0].split('_')[1]
    
    # ❌ 틀렸을 때 결과 출력
    st.error(f"## ❌ 아쉽습니다! \n정답은 **[{correct_name}]** 였습니다.")
    st.warning(f"🏆 최종 기록: **{st.session_state['correct_count']}마리** 연속 정답")
    
    # 📝 랭킹 등록 영역
    if not st.session_state['ranking_saved']:
        st.write("---")
        st.subheader("📝 명예의 전당 등록")
        user_id = st.text_input("랭킹에 기록될 이름을 입력하세요", value=st.session_state.get('current_user', ''))
        
        if st.button("내 기록 저장하기", type="primary"):
            save_ranking(user_id, st.session_state['correct_count'])
            st.session_state['ranking_saved'] = True
            st.success("랭킹 등록이 완료되었습니다!")
            st.rerun()
    
    # 📊 랭킹판 표시
    st.write("---")
    st.subheader("📊 Top 10 랭킹")
    rankings = get_rankings()[:10]
    for i, r in enumerate(rankings):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"**{i+1}위**"
        st.write(f"{medal} &nbsp;&nbsp; {r['id']} &nbsp;({r['count']}마리)")
    
    st.write("---")
    if st.button("🔄 다시 도전하기"):
        st.session_state.update({'game_over': False, 'correct_count': 0, 'current_pokemon': None, 'ranking_saved': False})
        next_question()
        st.rerun()
        
    st.stop() # 게임 오버 시 여기서 멈춤 (아래 퀴즈 화면 안 보임)

# ==========================================
# 🟢 2. 퀴즈 진행 화면
# ==========================================
current_file = st.session_state['current_pokemon']
correct_name = current_file.split('.')[0].split('_')[1]

col1, col2 = st.columns([2, 1])
with col1:
    st.title("⚡ 포켓몬 서바이벌!")
    st.write("틀리면 바로 탈락입니다. 신중하게 입력하세요!")
with col2:
    st.metric("현재 맞춘 갯수", f"{st.session_state['correct_count']} 마리")

image_path = os.path.join(IMAGE_DIR, current_file)

# 2. 파일 경로(image_path)를 넣어서 이미지를 출력합니다.
st.image(image_path, width=300)

# 정답 입력 (폼을 사용해 엔터키 지원)
with st.form("answer_form", clear_on_submit=True):
    user_answer = st.text_input("이 포켓몬의 이름은 무엇일까요?")
    submitted = st.form_submit_button("정답 확인")

if submitted:
    if not user_answer:
        st.warning("이름을 입력해 주세요!")
    elif user_answer.strip() == correct_name:
        # ✅ 정답 처리 로직
        st.success("## ⭕ 정답입니다!")
        time.sleep(0.8) # 0.8초 동안 O 표시를 보여주고 잠시 멈춤
        
        st.session_state['correct_count'] += 1
        next_question()
        st.rerun()
    else:
        # ❌ 오답 처리 로직
        st.session_state['game_over'] = True
        st.rerun()