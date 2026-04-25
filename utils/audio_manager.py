import streamlit as st
import streamlit.components.v1 as components
import base64
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BGM_DIR = os.path.join(BASE_DIR, "bgm")

@st.cache_data
def get_base64_audio(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def play_bgm_from_folder(folder_name):
    target_dir = os.path.join(BGM_DIR, folder_name)
    if not os.path.exists(target_dir):
        return

    audio_files = [f for f in os.listdir(target_dir) if f.lower().endswith(('.mp3', '.flac'))]
    if not audio_files:
        return

    target_file = audio_files[0]
    file_path = os.path.join(target_dir, target_file)
    b64 = get_base64_audio(file_path)

    html_code = f"""
    <style>
        #mini-player {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 220px;
            background: rgba(30,30,30,0.85);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 10px;
            color: white;
            font-size: 12px;
            z-index: 9999;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}

        #mini-player audio {{
            width: 100%;
            height: 28px;
        }}

        #title {{
            font-size: 11px;
            margin-bottom: 4px;
            opacity: 0.8;
        }}
    </style>

    <div id="mini-player">
        <div id="title">🎵 {target_file}</div>
        <audio id="player" src="data:audio/mpeg;base64,{b64}" controls loop></audio>
    </div>

    <script>
        const audio = document.getElementById("player");
        const folder = "{folder_name}";

        // 저장값
        const savedFolder = localStorage.getItem("bgm_folder");
        const savedTime = localStorage.getItem("bgm_time");
        const savedPlaying = localStorage.getItem("bgm_playing");

        // 초기화
        audio.onloadedmetadata = () => {{
            if (savedFolder === folder && savedTime) {{
                audio.currentTime = parseFloat(savedTime);
            }}

            if (savedPlaying === "true") {{
                audio.play().catch(() => {{}});
            }}
        }};

        // 상태 저장
        audio.ontimeupdate = () => {{
            localStorage.setItem("bgm_time", audio.currentTime);
        }};

        audio.onplay = () => {{
            localStorage.setItem("bgm_playing", "true");
            localStorage.setItem("bgm_folder", folder);
        }};

        audio.onpause = () => {{
            localStorage.setItem("bgm_playing", "false");
        }};

        // autoplay 우회 (1회 클릭)
        window.addEventListener("click", () => {{
            if (localStorage.getItem("bgm_playing") === "true" && audio.paused) {{
                audio.play().catch(() => {{}});
            }}
        }}, {{ once: true }});
    </script>
    """

    components.html(html_code, height=120)