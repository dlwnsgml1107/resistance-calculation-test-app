import streamlit as st

st.set_page_config(page_title="저항 색상띠 계산기", page_icon="🔌", layout="wide")

# 색상 코드 데이터
COLOR_DATA = {
    "검정": {"digit": 0, "multiplier": 1, "tolerance": None, "tempco": 250, "hex": "#000000"},
    "갈색": {"digit": 1, "multiplier": 10, "tolerance": 1, "tempco": 100, "hex": "#8B4513"},
    "빨강": {"digit": 2, "multiplier": 100, "tolerance": 2, "tempco": 50, "hex": "#E53935"},
    "주황": {"digit": 3, "multiplier": 1_000, "tolerance": None, "tempco": 15, "hex": "#F57C00"},
    "노랑": {"digit": 4, "multiplier": 10_000, "tolerance": None, "tempco": 25, "hex": "#FDD835"},
    "초록": {"digit": 5, "multiplier": 100_000, "tolerance": 0.5, "tempco": 20, "hex": "#43A047"},
    "파랑": {"digit": 6, "multiplier": 1_000_000, "tolerance": 0.25, "tempco": 10, "hex": "#1E88E5"},
    "보라": {"digit": 7, "multiplier": 10_000_000, "tolerance": 0.1, "tempco": 5, "hex": "#8E24AA"},
    "회색": {"digit": 8, "multiplier": 100_000_000, "tolerance": 0.05, "tempco": 1, "hex": "#9E9E9E"},
    "흰색": {"digit": 9, "multiplier": 1_000_000_000, "tolerance": None, "tempco": None, "hex": "#F5F5F5"},
    "금색": {"digit": None, "multiplier": 0.1, "tolerance": 5, "tempco": None, "hex": "#D4AF37"},
    "은색": {"digit": None, "multiplier": 0.01, "tolerance": 10, "tempco": None, "hex": "#C0C0C0"},
}

DIGIT_COLORS = [name for name, data in COLOR_DATA.items() if data["digit"] is not None]
MULTIPLIER_COLORS = list(COLOR_DATA)
TOLERANCE_COLORS = [name for name, data in COLOR_DATA.items() if data["tolerance"] is not None]
TEMPCO_COLORS = [name for name, data in COLOR_DATA.items() if data["tempco"] is not None]


def convert_resistance(value):
    """저항값 크기에 따라 적절한 단위로 변환해 반환한다."""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:g} GΩ"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:g} MΩ"
    elif value >= 1_000:
        return f"{value / 1_000:g} kΩ"
    else:
        return f"{value:g} Ω"


st.title("🔌 저항 색상띠 계산기")
st.caption("데스크톱 화면 기준 · 입력, 계산 결과, 색상 코드표를 한 화면에 가로로 배치")

# 표의 데이터도 for 반복문으로 구성
table_rows = []
for color_name, info in COLOR_DATA.items():
    table_rows.append({
        "색상": color_name,
        "숫자": "-" if info["digit"] is None else str(info["digit"]),
        "배율": f"×{info['multiplier']:g}",
        "허용오차": "-" if info["tolerance"] is None else f"±{info['tolerance']:g}%",
        "온도계수": "-" if info["tempco"] is None else f"{info['tempco']}",
    })

# 데스크톱에서 세 영역을 동일한 화면의 한 행에 배치
input_col, result_col, table_col = st.columns([1.15, 1.0, 1.45], gap="medium")

with input_col:
    st.subheader("① 색상띠 입력")
    band_count = st.radio(
        "색상띠 개수",
        [4, 5, 6],
        horizontal=True,
        format_func=lambda n: f"{n}색띠",
    )

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

    # 선택한 띠 색상을 자리 순서대로 리스트에 저장
    selected_colors = []
    for position, color_name in enumerate(color_bands, start=1):
        selected_colors.append({"자리": position, "색상": color_name})

    st.markdown("**선택한 색상띠**")
    swatches = st.columns(len(selected_colors))
    for col, item in zip(swatches, selected_colors):
        with col:
            st.markdown(
                f"""
                <div style="height:42px;background:{COLOR_DATA[item['색상']]['hex']};
                border:1px solid #999;border-radius:5px;"></div>
                <div style="text-align:center;font-size:0.72rem;margin-top:3px;">
                {item['자리']}번<br>{item['색상']}
                </div>
                """,
                unsafe_allow_html=True,
            )

# 계산값은 입력값을 바탕으로 공통 계산
resistance = significant * multiplier
minimum = resistance * (1 - tolerance / 100)
maximum = resistance * (1 + tolerance / 100)

with result_col:
    st.subheader("② 계산 결과")
    st.markdown(
        f"""
        <div style="padding:15px 12px;background:#E8F5E9;border:1px solid #81C784;
        border-radius:10px;margin:4px 0 12px 0;">
            <div style="color:#2E7D32;font-size:0.9rem;font-weight:600;">최종 저항값</div>
            <div style="color:#16803C;font-size:2rem;font-weight:800;line-height:1.35;">
                {convert_resistance(resistance)}
            </div>
            <div style="color:#2E7D32;font-size:0.88rem;">허용오차 ±{tolerance:g}%</div>
        </div>
        """,
        unsafe_allow_html=True,
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
            f"{COLOR_DATA[band2]['digit']} × 10 + {COLOR_DATA[band3]['digit']} "
            f"= **{significant}**"
        )
        multiplier_band = band4

    st.write(f"② 배율: {multiplier_band} = **×{multiplier:g}**")
    st.write(f"③ 저항값: {significant} × {multiplier:g} = **{convert_resistance(resistance)}**")
    st.write(f"④ 허용 범위: **{convert_resistance(minimum)} ~ {convert_resistance(maximum)}**")
    if band_count == 6:
        st.write(f"⑤ 온도계수: **{tempco} ppm/°C**")

    st.markdown("**저항값 범위**")
    st.caption(f"최솟값: {convert_resistance(minimum)}")
    st.caption(f"최댓값: {convert_resistance(maximum)}")

with table_col:
    st.subheader("③ 저항 색상 코드표")
    st.caption("색상별 숫자 · 배율 · 허용오차 · 온도계수")

    # for 반복문을 사용해 표의 각 행과 셀을 생성
    html_table = """
    <table style="width:100%;border-collapse:collapse;text-align:center;font-size:0.78rem;">
    <thead><tr style="background:#E8F5E9;">
    <th style="padding:7px 4px;border:1px solid #ccc;">색상</th>
    <th style="padding:7px 4px;border:1px solid #ccc;">숫자</th>
    <th style="padding:7px 4px;border:1px solid #ccc;">배율</th>
    <th style="padding:7px 4px;border:1px solid #ccc;">허용오차</th>
    <th style="padding:7px 4px;border:1px solid #ccc;">온도계수<br>(ppm/°C)</th>
    </tr></thead><tbody>
    """
    for row in table_rows:
        html_table += "<tr>"
        for key in ["색상", "숫자", "배율", "허용오차", "온도계수"]:
            html_table += f"<td style='padding:6px 3px;border:1px solid #ccc;'>{row[key]}</td>"
        html_table += "</tr>"
    html_table += "</tbody></table>"

    st.markdown(html_table, unsafe_allow_html=True)

st.markdown(
    "<div style='color:gray;font-size:0.75rem;margin-top:10px;'>"
    "※ 6색띠의 여섯째 띠는 온도계수입니다. 색상 코드와 온도계수는 일반적인 규격 기준이며 "
    "제조사 및 부품 규격에 따라 차이가 있을 수 있습니다.</div>",
    unsafe_allow_html=True,
)
