import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="저항 색상띠 계산기",
    page_icon="🔌",
    layout="wide",
)

# 색상별 숫자, 배율, 허용오차, 온도계수
COLOR_DATA = {
    "검정": {"digit": 0, "multiplier": 1, "tolerance": None, "tempco": 250},
    "갈색": {"digit": 1, "multiplier": 10, "tolerance": 1, "tempco": 100},
    "빨강": {"digit": 2, "multiplier": 100, "tolerance": 2, "tempco": 50},
    "주황": {"digit": 3, "multiplier": 1_000, "tolerance": None, "tempco": 15},
    "노랑": {"digit": 4, "multiplier": 10_000, "tolerance": None, "tempco": 25},
    "초록": {"digit": 5, "multiplier": 100_000, "tolerance": 0.5, "tempco": 20},
    "파랑": {"digit": 6, "multiplier": 1_000_000, "tolerance": 0.25, "tempco": 10},
    "보라": {"digit": 7, "multiplier": 10_000_000, "tolerance": 0.1, "tempco": 5},
    "회색": {"digit": 8, "multiplier": 100_000_000, "tolerance": 0.05, "tempco": 1},
    "흰색": {"digit": 9, "multiplier": 1_000_000_000, "tolerance": None, "tempco": None},
    "금색": {"digit": None, "multiplier": 0.1, "tolerance": 5, "tempco": None},
    "은색": {"digit": None, "multiplier": 0.01, "tolerance": 10, "tempco": None},
}

DIGIT_COLORS = [
    color for color, data in COLOR_DATA.items()
    if data["digit"] is not None
]
MULTIPLIER_COLORS = list(COLOR_DATA.keys())
TOLERANCE_COLORS = [
    color for color, data in COLOR_DATA.items()
    if data["tolerance"] is not None
]
TEMPCO_COLORS = [
    color for color, data in COLOR_DATA.items()
    if data["tempco"] is not None
]


def convert_resistance(value):
    """저항값 크기에 따라 적절한 단위로 변환해 문자열로 반환한다."""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:g} GΩ"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:g} MΩ"
    elif value >= 1_000:
        return f"{value / 1_000:g} kΩ"
    else:
        return f"{value:g} Ω"


st.title("🔌 저항 색상띠 계산기")
st.caption("데스크톱 화면 기준으로 입력, 계산 결과, 색상 코드표를 가로로 배치했습니다.")

# 세 영역을 한 행에 배치
input_col, result_col, table_col = st.columns([1.1, 1.0, 1.45], gap="medium")

with input_col:
    st.subheader("① 색상띠 입력")
    band_count = st.radio(
        "색상띠 개수",
        [4, 5, 6],
        horizontal=True,
        format_func=lambda number: f"{number}색띠",
    )

    # 색상띠 개수에 따라 입력 항목과 계산 규칙을 분기
    if band_count == 4:
        st.caption("유효숫자 2자리 · 배율 · 허용오차")
        band1 = st.selectbox("첫째 띠", DIGIT_COLORS, index=1)
        band2 = st.selectbox("둘째 띠", DIGIT_COLORS, index=0)
        band3 = st.selectbox("셋째 띠 · 배율", MULTIPLIER_COLORS, index=2)
        band4 = st.selectbox("넷째 띠 · 허용오차", TOLERANCE_COLORS, index=0)

        color_bands = [band1, band2, band3, band4]
        significant = COLOR_DATA[band1]["digit"] * 10 + COLOR_DATA[band2]["digit"]
        multiplier = COLOR_DATA[band3]["multiplier"]
        tolerance = COLOR_DATA[band4]["tolerance"]
        tempco = None

    elif band_count == 5:
        st.caption("유효숫자 3자리 · 배율 · 허용오차")
        band1 = st.selectbox("첫째 띠", DIGIT_COLORS, index=1)
        band2 = st.selectbox("둘째 띠", DIGIT_COLORS, index=0)
        band3 = st.selectbox("셋째 띠", DIGIT_COLORS, index=0)
        band4 = st.selectbox("넷째 띠 · 배율", MULTIPLIER_COLORS, index=2)
        band5 = st.selectbox("다섯째 띠 · 허용오차", TOLERANCE_COLORS, index=0)

        color_bands = [band1, band2, band3, band4, band5]
        significant = (
            COLOR_DATA[band1]["digit"] * 100
            + COLOR_DATA[band2]["digit"] * 10
            + COLOR_DATA[band3]["digit"]
        )
        multiplier = COLOR_DATA[band4]["multiplier"]
        tolerance = COLOR_DATA[band5]["tolerance"]
        tempco = None

    else:
        st.caption("유효숫자 3자리 · 배율 · 허용오차 · 온도계수")
        band1 = st.selectbox("첫째 띠", DIGIT_COLORS, index=1)
        band2 = st.selectbox("둘째 띠", DIGIT_COLORS, index=0)
        band3 = st.selectbox("셋째 띠", DIGIT_COLORS, index=0)
        band4 = st.selectbox("넷째 띠 · 배율", MULTIPLIER_COLORS, index=2)
        band5 = st.selectbox("다섯째 띠 · 허용오차", TOLERANCE_COLORS, index=0)
        band6 = st.selectbox("여섯째 띠 · 온도계수", TEMPCO_COLORS, index=1)

        color_bands = [band1, band2, band3, band4, band5, band6]
        significant = (
            COLOR_DATA[band1]["digit"] * 100
            + COLOR_DATA[band2]["digit"] * 10
            + COLOR_DATA[band3]["digit"]
        )
        multiplier = COLOR_DATA[band4]["multiplier"]
        tolerance = COLOR_DATA[band5]["tolerance"]
        tempco = COLOR_DATA[band6]["tempco"]

    # 선택한 색상띠를 자리 순서대로 리스트에 저장
    selected_colors = []
    for position, color_name in enumerate(color_bands, start=1):
        selected_colors.append({
            "자리": position,
            "색상": color_name,
        })

    st.markdown("**선택한 색상띠 순서**")
    st.dataframe(
        pd.DataFrame(selected_colors),
        hide_index=True,
        use_container_width=True,
    )

# 입력값을 이용해 공통 계산
resistance = significant * multiplier
minimum = resistance * (1 - tolerance / 100)
maximum = resistance * (1 + tolerance / 100)

with result_col:
    st.subheader("② 계산 결과")

    # HTML 대신 Streamlit의 기본 성공 메시지로 저항값 강조
    st.success(
        f"### {convert_resistance(resistance)}\n\n"
        f"허용오차: ±{tolerance:g}%"
    )

    st.markdown("**계산 과정**")
    if band_count == 4:
        st.write(
            f"① 유효숫자: {COLOR_DATA[band1]['digit']} × 10 + "
            f"{COLOR_DATA[band2]['digit']} = **{significant}**"
        )
        multiplier_band = band3
    else:
        st.write(
            f"① 유효숫자: {COLOR_DATA[band1]['digit']} × 100 + "
            f"{COLOR_DATA[band2]['digit']} × 10 + "
            f"{COLOR_DATA[band3]['digit']} = **{significant}**"
        )
        multiplier_band = band4

    st.write(f"② 배율: {multiplier_band} = **×{multiplier:g}**")
    st.write(
        f"③ 저항값: {significant} × {multiplier:g} "
        f"= **{convert_resistance(resistance)}**"
    )
    st.write(
        f"④ 허용 범위: **{convert_resistance(minimum)} ~ "
        f"{convert_resistance(maximum)}**"
    )

    if band_count == 6:
        st.write(f"⑤ 온도계수: **{tempco} ppm/°C**")

    st.markdown("**저항값 범위**")
    st.metric("최솟값", convert_resistance(minimum))
    st.metric("최댓값", convert_resistance(maximum))

with table_col:
    st.subheader("③ 저항 색상 코드표")
    st.caption("숫자 · 배율 · 허용오차 · 온도계수")

    # for 반복문으로 색상 코드표의 행 생성
    table_rows = []
    for color_name, info in COLOR_DATA.items():
        table_rows.append({
            "색상": color_name,
            "숫자": "-" if info["digit"] is None else info["digit"],
            "배율": f"×{info['multiplier']:g}",
            "허용오차": "-" if info["tolerance"] is None else f"±{info['tolerance']:g}%",
            "온도계수": "-" if info["tempco"] is None else info["tempco"],
        })

    st.dataframe(
        pd.DataFrame(table_rows),
        hide_index=True,
        use_container_width=True,
        height=520,
    )

st.caption(
    "※ 6색띠의 여섯째 띠는 온도계수(ppm/°C)입니다. "
    "실제 부품의 색상 코드 및 규격은 제조사에 따라 차이가 있을 수 있습니다."
)
