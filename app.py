import streamlit as st

st.set_page_config(page_title="저항 색상띠 계산기", page_icon="🔌", layout="centered")

# 저항 색상띠 표: 유효숫자, 승수, 허용오차
COLOR_DATA = {
    "검정": {"digit": 0, "multiplier": 1, "tolerance": None, "hex": "#000000"},
    "갈색": {"digit": 1, "multiplier": 10, "tolerance": 1, "hex": "#8B4513"},
    "빨강": {"digit": 2, "multiplier": 100, "tolerance": 2, "hex": "#E53935"},
    "주황": {"digit": 3, "multiplier": 1_000, "tolerance": None, "hex": "#F57C00"},
    "노랑": {"digit": 4, "multiplier": 10_000, "tolerance": None, "hex": "#FDD835"},
    "초록": {"digit": 5, "multiplier": 100_000, "tolerance": 0.5, "hex": "#43A047"},
    "파랑": {"digit": 6, "multiplier": 1_000_000, "tolerance": 0.25, "hex": "#1E88E5"},
    "보라": {"digit": 7, "multiplier": 10_000_000, "tolerance": 0.1, "hex": "#8E24AA"},
    "회색": {"digit": 8, "multiplier": 100_000_000, "tolerance": 0.05, "hex": "#9E9E9E"},
    "흰색": {"digit": 9, "multiplier": 1_000_000_000, "tolerance": None, "hex": "#F5F5F5"},
    "금색": {"digit": None, "multiplier": 0.1, "tolerance": 5, "hex": "#D4AF37"},
    "은색": {"digit": None, "multiplier": 0.01, "tolerance": 10, "hex": "#C0C0C0"},
}

DIGIT_COLORS = [c for c, v in COLOR_DATA.items() if v["digit"] is not None]
MULTIPLIER_COLORS = list(COLOR_DATA.keys())
TOLERANCE_COLORS = [
    c for c, v in COLOR_DATA.items() if v["tolerance"] is not None
]

def format_ohms(value: float) -> str:
    """저항값을 읽기 쉬운 단위로 표시한다."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:g} MΩ"
    if value >= 1_000:
        return f"{value / 1_000:g} kΩ"
    return f"{value:g} Ω"

st.title("🔌 저항 색상띠 계산기")
st.write("저항의 색상띠를 순서대로 선택하면 저항값과 허용오차를 계산합니다.")

band_count = st.radio(
    "색상띠 개수",
    options=[4, 5],
    horizontal=True,
    format_func=lambda x: f"{x}색띠",
)

st.caption(
    "색상띠는 저항의 한쪽 끝에 있는 허용오차 띠를 마지막으로 하여 "
    "왼쪽부터 순서대로 선택하세요."
)

if band_count == 4:
    st.subheader("4색띠 저항")
    st.caption("첫째 띠·둘째 띠: 유효숫자 / 셋째 띠: 승수 / 넷째 띠: 허용오차")
    col1, col2 = st.columns(2)
    with col1:
        band1 = st.selectbox("첫째 띠", DIGIT_COLORS, index=1)
    with col2:
        band2 = st.selectbox("둘째 띠", DIGIT_COLORS, index=0)
    col3, col4 = st.columns(2)
    with col3:
        band3 = st.selectbox("셋째 띠 (승수)", MULTIPLIER_COLORS, index=2)
    with col4:
        band4 = st.selectbox("넷째 띠 (허용오차)", TOLERANCE_COLORS, index=0)

    significant = COLOR_DATA[band1]["digit"] * 10 + COLOR_DATA[band2]["digit"]
    multiplier = COLOR_DATA[band3]["multiplier"]
    tolerance = COLOR_DATA[band4]["tolerance"]

else:
    st.subheader("5색띠 저항")
    st.caption("첫째~셋째 띠: 유효숫자 / 넷째 띠: 승수 / 다섯째 띠: 허용오차")
    col1, col2, col3 = st.columns(3)
    with col1:
        band1 = st.selectbox("첫째 띠", DIGIT_COLORS, index=1)
    with col2:
        band2 = st.selectbox("둘째 띠", DIGIT_COLORS, index=0)
    with col3:
        band3 = st.selectbox("셋째 띠", DIGIT_COLORS, index=0)
    col4, col5 = st.columns(2)
    with col4:
        band4 = st.selectbox("넷째 띠 (승수)", MULTIPLIER_COLORS, index=2)
    with col5:
        band5 = st.selectbox("다섯째 띠 (허용오차)", TOLERANCE_COLORS, index=0)

    significant = (
        COLOR_DATA[band1]["digit"] * 100
        + COLOR_DATA[band2]["digit"] * 10
        + COLOR_DATA[band3]["digit"]
    )
    multiplier = COLOR_DATA[band4]["multiplier"]
    tolerance = COLOR_DATA[band5]["tolerance"]

resistance = significant * multiplier
minimum = resistance * (1 - tolerance / 100)
maximum = resistance * (1 + tolerance / 100)

st.divider()
st.subheader("계산 결과")

st.metric("저항값", format_ohms(resistance))
st.write(f"**허용오차:** ±{tolerance:g}%")
st.write(f"**가능한 저항값 범위:** {format_ohms(minimum)} ~ {format_ohms(maximum)}")

bands = [band1, band2, band3, band4] if band_count == 4 else [
    band1, band2, band3, band4, band5
]
st.write("**선택한 색상띠:** " + " → ".join(bands))

# 선택한 띠를 간단한 그림으로 표시
st.markdown("**색상띠 미리보기**")
swatch_cols = st.columns(len(bands))
for col, color_name in zip(swatch_cols, bands):
    with col:
        st.markdown(
            f"""
            <div style="
                height: 75px;
                border-radius: 8px;
                background: {COLOR_DATA[color_name]['hex']};
                border: 1px solid #888;
            "></div>
            <div style="text-align:center; margin-top:6px;">{color_name}</div>
            """,
            unsafe_allow_html=True,
        )

with st.expander("색상띠 읽는 방법"):
    st.markdown(
        """
        | 색상 | 숫자 | 승수 | 허용오차 |
        |---|---:|---:|---:|
        | 검정 | 0 | ×1 | - |
        | 갈색 | 1 | ×10 | ±1% |
        | 빨강 | 2 | ×100 | ±2% |
        | 주황 | 3 | ×1,000 | - |
        | 노랑 | 4 | ×10,000 | - |
        | 초록 | 5 | ×100,000 | ±0.5% |
        | 파랑 | 6 | ×1,000,000 | ±0.25% |
        | 보라 | 7 | ×10,000,000 | ±0.1% |
        | 회색 | 8 | ×100,000,000 | ±0.05% |
        | 흰색 | 9 | ×1,000,000,000 | - |
        | 금색 | - | ×0.1 | ±5% |
        | 은색 | - | ×0.01 | ±10% |
        """
    )

st.info(
    "참고: 이 프로그램은 일반적인 4색띠·5색띠 저항을 기준으로 합니다. "
    "제조사나 부품 규격에 따라 예외가 있을 수 있습니다."
)
