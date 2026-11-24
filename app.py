import streamlit as st

st.set_page_config(
    page_title="저항 색상띠 계산기",
    page_icon="🔌",
    layout="wide",
)

# 색상별 숫자, 배율, 허용오차, 온도계수(ppm/°C)
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

DIGIT_COLORS = [name for name, info in COLOR_DATA.items() if info["digit"] is not None]
MULTIPLIER_COLORS = list(COLOR_DATA.keys())
TOLERANCE_COLORS = [
    name for name, info in COLOR_DATA.items() if info["tolerance"] is not None
]
TEMPCO_COLORS = [
    name for name, info in COLOR_DATA.items() if info["tempco"] is not None
]


def convert_resistance(value):
    """저항값 크기에 따라 Ω, kΩ, MΩ, GΩ 단위로 변환해 문자열로 반환한다."""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:g} GΩ"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:g} MΩ"
    elif value >= 1_000:
        return f"{value / 1_000:g} kΩ"
    else:
        return f"{value:g} Ω"


st.title("🔌 저항 색상띠 계산기")
st.write("4색띠·5색띠·6색띠 저항의 색상을 선택하고 저항값과 계산 과정을 확인하세요.")

# 화면을 좌우로 나누어 입력 영역과 결과 영역을 가로 배치
left, right = st.columns([1, 1.35], gap="large")

with left:
    st.subheader("① 색상띠 입력")
    band_count = st.radio(
        "저항 색상띠 개수",
        [4, 5, 6],
        horizontal=True,
        format_func=lambda n: f"{n}색띠",
    )

    st.caption("왼쪽부터 첫 번째 띠 순서대로 선택하세요. 마지막 띠는 허용오차(6색띠는 온도계수 포함)입니다.")

    # 색상띠 개수에 따라 입력 항목을 if-else로 구분
    if band_count == 4:
        st.markdown("**4색띠: 유효숫자 2자리 · 배율 · 허용오차**")
        c1, c2 = st.columns(2)
        with c1:
            band1 = st.selectbox("첫째 띠", DIGIT_COLORS, index=1)
            band3 = st.selectbox("셋째 띠 (배율)", MULTIPLIER_COLORS, index=2)
        with c2:
            band2 = st.selectbox("둘째 띠", DIGIT_COLORS, index=0)
            band4 = st.selectbox("넷째 띠 (허용오차)", TOLERANCE_COLORS, index=0)

        color_bands = [band1, band2, band3, band4]
        significant = COLOR_DATA[band1]["digit"] * 10 + COLOR_DATA[band2]["digit"]
        multiplier = COLOR_DATA[band3]["multiplier"]
        tolerance = COLOR_DATA[band4]["tolerance"]
        tempco = None

    elif band_count == 5:
        st.markdown("**5색띠: 유효숫자 3자리 · 배율 · 허용오차**")
        c1, c2, c3 = st.columns(3)
        with c1:
            band1 = st.selectbox("첫째 띠", DIGIT_COLORS, index=1)
        with c2:
            band2 = st.selectbox("둘째 띠", DIGIT_COLORS, index=0)
        with c3:
            band3 = st.selectbox("셋째 띠", DIGIT_COLORS, index=0)
        c4, c5 = st.columns(2)
        with c4:
            band4 = st.selectbox("넷째 띠 (배율)", MULTIPLIER_COLORS, index=2)
        with c5:
            band5 = st.selectbox("다섯째 띠 (허용오차)", TOLERANCE_COLORS, index=0)

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
        st.markdown("**6색띠: 유효숫자 3자리 · 배율 · 허용오차 · 온도계수**")
        c1, c2, c3 = st.columns(3)
        with c1:
            band1 = st.selectbox("첫째 띠", DIGIT_COLORS, index=1)
        with c2:
            band2 = st.selectbox("둘째 띠", DIGIT_COLORS, index=0)
        with c3:
            band3 = st.selectbox("셋째 띠", DIGIT_COLORS, index=0)
        c4, c5, c6 = st.columns(3)
        with c4:
            band4 = st.selectbox("넷째 띠 (배율)", MULTIPLIER_COLORS, index=2)
        with c5:
            band5 = st.selectbox("다섯째 띠 (허용오차)", TOLERANCE_COLORS, index=0)
        with c6:
            band6 = st.selectbox("여섯째 띠 (온도계수)", TEMPCO_COLORS, index=1)

        color_bands = [band1, band2, band3, band4, band5, band6]
        significant = (
            COLOR_DATA[band1]["digit"] * 100
            + COLOR_DATA[band2]["digit"] * 10
            + COLOR_DATA[band3]["digit"]
        )
        multiplier = COLOR_DATA[band4]["multiplier"]
        tolerance = COLOR_DATA[band5]["tolerance"]
        tempco = COLOR_DATA[band6]["tempco"]

    st.markdown("**선택한 색상띠 순서**")
    # 사용자가 선택한 각 자리의 색상을 순서대로 리스트에 저장
    selected_colors = []
    for position, color_name in enumerate(color_bands, start=1):
        selected_colors.append({"자리": position, "색상": color_name})

    swatch_columns = st.columns(len(selected_colors))
    for column, item in zip(swatch_columns, selected_colors):
        with column:
            st.markdown(
                f"""
                <div style="height:55px; background:{COLOR_DATA[item['색상']]['hex']};
                border:1px solid #888; border-radius:6px;"></div>
                <div style="text-align:center; font-size:0.85rem; margin-top:4px;">
                {item['자리']}번 · {item['색상']}
                </div>
                """,
                unsafe_allow_html=True,
            )

with right:
    st.subheader("② 계산 결과")
    resistance = significant * multiplier
    minimum = resistance * (1 - tolerance / 100)
    maximum = resistance * (1 + tolerance / 100)

    # 저항값을 초록색으로 강조하여 표시
    st.markdown(
        f"""
        <div style="padding:20px; border-radius:12px; background:#E8F5E9;
        border:1px solid #81C784; margin-bottom:14px;">
            <div style="font-size:0.95rem; color:#2E7D32; font-weight:600;">계산된 저항값</div>
            <div style="font-size:2.2rem; color:#16803C; font-weight:800;">
                {convert_resistance(resistance)}
            </div>
            <div style="font-size:0.95rem; color:#2E7D32;">
                허용오차 ±{tolerance:g}%
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**계산 과정**")
    if band_count == 4:
        st.write(f"1. 유효숫자: {COLOR_DATA[band1]['digit']} × 10 + {COLOR_DATA[band2]['digit']} = **{significant}**")
    else:
        st.write(
            f"1. 유효숫자: {COLOR_DATA[band1]['digit']} × 100 + "
            f"{COLOR_DATA[band2]['digit']} × 10 + {COLOR_DATA[band3]['digit']} "
            f"= **{significant}**"
        )
    multiplier_band = band3 if band_count == 4 else band4
    st.write(
        f"2. 배율: {multiplier_band} = **×{multiplier:g}**"
    )
    st.write(
        f"3. 저항값: {significant} × {multiplier:g} = "
        f"**{convert_resistance(resistance)}**"
    )
    st.write(
        f"4. 허용오차 범위: {convert_resistance(minimum)} ~ "
        f"{convert_resistance(maximum)}"
    )
    if band_count == 6:
        st.write(f"5. 온도계수: **{tempco} ppm/°C**")

    st.markdown("**저항값 범위**")
    low_col, high_col = st.columns(2)
    low_col.metric("최솟값", convert_resistance(minimum))
    high_col.metric("최댓값", convert_resistance(maximum))

st.divider()

# 색상표를 반복문(for)으로 생성하고, 계산 결과 아래가 아닌 오른쪽 열에 배치
result_column, table_column = st.columns([1, 1.25], gap="large")

# 표에 들어갈 자료를 for문으로 정리
table_rows = []
for color_name, info in COLOR_DATA.items():
    digit_text = "-" if info["digit"] is None else str(info["digit"])
    multiplier_text = f"×{info['multiplier']:g}"
    tolerance_text = "-" if info["tolerance"] is None else f"±{info['tolerance']:g}%"
    tempco_text = "-" if info["tempco"] is None else f"{info['tempco']} ppm/°C"
    table_rows.append(
        {
            "색상": color_name,
            "숫자": digit_text,
            "배율": multiplier_text,
            "허용오차": tolerance_text,
            "온도계수": tempco_text,
        }
    )

with result_column:
    st.subheader("③ 계산 요약")
    st.write("선택한 색상띠:", " → ".join(color_bands))
    st.write(f"유효숫자: **{significant}**")
    st.write(f"배율: **×{multiplier:g}**")
    st.write(f"최종 저항값: **{convert_resistance(resistance)}**")
    st.write(f"허용오차: **±{tolerance:g}%**")
    if band_count == 6:
        st.write(f"온도계수: **{tempco} ppm/°C**")

with table_column:
    st.subheader("④ 저항 색상 코드표")
    st.caption("색상별 숫자, 배율, 허용오차 및 온도계수")

    # 행과 셀을 for문으로 순회해 HTML 표를 구성
    html_table = """
    <div style="overflow-x:auto;">
    <table style="width:100%; border-collapse:collapse; text-align:center; font-size:0.9rem;">
    <thead>
    <tr style="background:#E8F5E9;">
    <th style="padding:8px; border:1px solid #ccc;">색상</th>
    <th style="padding:8px; border:1px solid #ccc;">숫자</th>
    <th style="padding:8px; border:1px solid #ccc;">배율</th>
    <th style="padding:8px; border:1px solid #ccc;">허용오차</th>
    <th style="padding:8px; border:1px solid #ccc;">온도계수</th>
    </tr>
    </thead><tbody>
    """
    for row in table_rows:
        html_table += "<tr>"
        for key in ["색상", "숫자", "배율", "허용오차", "온도계수"]:
            html_table += f"<td style='padding:7px; border:1px solid #ccc;'>{row[key]}</td>"
        html_table += "</tr>"
    html_table += "</tbody></table></div>"

    st.markdown(html_table, unsafe_allow_html=True)

st.info(
    "참고: 6색띠의 여섯째 띠는 온도 변화에 따른 저항값 변화를 나타내는 "
    "온도계수(ppm/°C)입니다. 온도계수 값은 일반적으로 사용되는 색상 코드 기준이며, "
    "부품 제조사와 규격에 따라 차이가 있을 수 있습니다."
)
