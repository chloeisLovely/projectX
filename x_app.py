import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import streamlit.components.v1 as components
from streamlit_drawable_canvas import st_canvas
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="우리 팀의 우주정거장 프로젝트",
    page_icon="🛰️",
    layout="wide"
)

# --- 제목 ---
st.title("🛰️ 팀 프로젝트 활동: 우리 팀의 우주정거장")
st.markdown("---")


# --- [1단계] 아이디어 모으기 ---
st.header("[1단계] 아이디어 모으기")
st.subheader("우리 정거장이 달 탐사에 도움을 주려면 어떤 기능이 필요할까요?")

col1, col2 = st.columns(2)
with col1:
    st.checkbox("⚡ 에너지 공급 방법 구상")
    st.checkbox("🏠 생활 공간 설계")
    st.checkbox("🔬 과학 실험실 기능 구상")
with col2:
    st.checkbox("🚀 우주선 도킹 시스템 설계")
    st.checkbox("🚨 위기 상황 대비 계획")

st.markdown("---")


# --- [2단계] 설계도 그리기 (업그레이드) ---
st.header("[2단계] 설계도 그리기")
st.subheader("팀원들과 함께 우주정거장 설계도를 직접 그려보세요!")
st.info("왼쪽 사이드바에서 그리기 도구, 굵기, 색상을 선택할 수 있습니다.")

# 그리기 도구 설정 (사이드바)
drawing_mode = st.sidebar.selectbox(
    "그리기 도구:",
    ("freedraw", "line", "rect", "circle", "transform"),
    help="freedraw: 자유롭게 그리기, line: 선, rect: 사각형, circle: 원, transform: 선택 및 수정"
)
stroke_width = st.sidebar.slider("선 굵기: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("선 색상: ")
bg_color = st.sidebar.color_picker("배경 색상: ", "#eee")

# 그림판 (Canvas) 생성
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=450,
    drawing_mode=drawing_mode,
    key="canvas",
)

# 그려진 이미지를 PIL Image 객체로 변환
drawn_image = None
if canvas_result.image_data is not None:
    drawn_image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')

st.markdown("---")


# --- 발표 준비 ---
st.header("📢 발표 준비")
st.subheader("프로젝트 발표를 위해 아래 내용을 입력해주세요.")

station_name = st.text_input("1. 우리 팀 정거장의 이름은?")
special_feature = st.text_area("2. 우리 정거장만의 특별한 기능이 있다면? (자유롭게 작성)")
presenter = st.text_input("3. 발표 담당자는 누구인가요?")

st.markdown("---")


# --- 오늘의 다짐 ---
st.header("## 6. 오늘의 다짐") # 원본 양식의 번호를 따름
quote = "“달 탐사 다누리호에서 시작된 우리의 발걸음은, 우주정거장을 거쳐 더 멀리 화성까지 이어질 것이다.”"
st.info(f"**{quote}** 🌠")

st.markdown("---")


# --- 제출 및 결과 확인 ---
# session_state를 사용하여 제출 상태와 데이터를 관리
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if st.button("🚀 프로젝트 제출하기"):
    st.session_state.submitted = True
    st.session_state.station_name = station_name
    st.session_state.special_feature = special_feature
    st.session_state.presenter = presenter
    st.session_state.drawn_image = drawn_image

# 제출 버튼을 누르면 요약 정보와 다운로드 버튼 표시
if st.session_state.submitted:
    st.success("프로젝트 내용이 성공적으로 정리되었습니다!")
    st.markdown("<hr>", unsafe_allow_html=True)

    # HTML에 포함시키기 위해 이미지를 base64로 인코딩
    img_html = ""
    if st.session_state.get('drawn_image') is not None:
        buffered = BytesIO()
        st.session_state.drawn_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        img_html = f'''
            <h4 style="margin-top: 20px;">📐 우리가 그린 설계도:</h4>
            <img src="data:image/png;base64,{img_str}" style="width: 100%; max-width: 600px; border: 1px solid #ddd; border-radius: 5px; margin-top: 10px;">
        '''
    else:
        img_html = "<h4 style='color: red;'>※ 설계도가 그려지지 않았습니다.</h4>"

    # 이미지로 저장될 영역의 HTML 코드 생성
    summary_html = f"""
    <div id="capture" style="padding: 25px; border: 2px solid #007bff; border-radius: 15px; background-color: white; font-family: sans-serif; color: black;">
        <h2 style="color: #007bff; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px;">📝 우리 팀 프로젝트 최종 요약</h2>
        <br>
        <p style="font-size: 1.1em;"><strong>🛰️ 정거장 이름:</strong> {st.session_state.get('station_name', '입력되지 않음')}</p>
        <p style="font-size: 1.1em;"><strong>🧑‍🚀 발표 담당자:</strong> {st.session_state.get('presenter', '입력되지 않음')}</p>
        <h4 style="color: #333; margin-top: 20px;"><strong>✨ 특별한 기능:</strong></h4>
        <div style="white-space: pre-wrap; background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #dee2e6; min-height: 80px;">{st.session_state.get('special_feature', '입력되지 않음')}</div>
        {img_html}
    </div>
    """
    
    st.subheader("✅ 최종 결과 미리보기")
    st.markdown(summary_html, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # 이미지 다운로드 버튼과 자바스크립트 코드
    st.subheader("🖼️ 결과 이미지로 저장 및 다운로드")
    st.info("아래 버튼을 누르면 위 요약 내용이 이미지 파일(PNG)로 다운로드됩니다.")

    js_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
    const saveImage = () => {{
        const captureDiv = document.getElementById('capture');
        if (captureDiv) {{
            html2canvas(captureDiv, {{
                scale: 2, // 2배율로 고해상도 이미지 생성
                useCORS: true,
                backgroundColor: 'white'
            }}).then(canvas => {{
                const imageURL = canvas.toDataURL('image/png');
                const downloadLink = document.createElement('a');
                downloadLink.href = imageURL;
                downloadLink.download = '{st.session_state.get('station_name', '우주정거장')}_프로젝트_결과.png';
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            }});
        }}
    }}
    </script>
    <button onclick="saveImage()" style="display: inline-block; padding: 12px 24px; font-size: 16px; font-weight: bold; color: white; background: linear-gradient(45deg, #0d6efd, #0dcaf0); border: none; border-radius: 8px; cursor: pointer; text-align: center; text-decoration: none; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        결과 이미지 다운로드 ↓
    </button>
    """
    components.html(js_code, height=60)
