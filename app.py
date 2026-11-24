import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="저항 색상띠 계산기",
    page_icon="🔌",
    layout="wide",
)

# 색상별 숫자, 배율, 허용오차, 온도계수
COLOR_DATA = {
    "검정": {"digit": 0, "multiplier": 1, "tolerance": None, "tempco": 250, "hex": "#222222"},
    "갈색": {"digit": 1, "multiplier": 10, "tolerance": 1, "tempco": 100, "hex": "#8B4513"},
    "빨강": {"digit": 2, "multiplier": 100, "tolerance": 2, "tempco": 50, "hex": "#E53935"},
    "주황": {"digit": 3, "multiplier": 1_000, "tolerance": None, "tempco": 15, "hex": "#F57C00"},
    "노랑": {"digit": 4, "multiplier": 10_000, "tolerance": None, "tempco": 25, "hex": "#FDD835"},
    "초록": {"digit": 5, "multiplier": 100_000, "tolerance": 0.5, "tempco": 20, "hex": "#43A047"},
    "파랑": {"digit": 6, "multiplier": 1_000_000, "tolerance": 0.25, "tempco": 10, "hex": "#1E88E5"},
    "보라": {"digit": 7, "multiplier": 10_000_000, "tolerance": 0.1, "tempco": 5, "hex": "#8E24AA"},
    "회색": {"digit": 8, "multiplier": 100_000_000, "tolerance": 0.05, "tempco": 1, "hex": "#9E9E9E"},
    "흰색": {"digit": 9, "multiplier": 1_000_000_000, "tolerance": None, "tempco": None, "hex": "#FFFFFF"},
    "금색": {"digit": None, "multiplier": 0.1, "tolerance": 5, "tempco": None, "hex": "#D4AF37"},
    "은색": {"digit": None, "multiplier": 0.01, "tolerance": 10, "tempco": None, "hex": "#C0C0C0"},
}

DIGIT_COLORS = [name for name, data in COLOR_DATA.items() if data["digit"] is not None]
MULTIPLIER_COLORS = list(COLOR_DATA.keys())
TOLERANCE_COLORS = [name for name, data in COLOR_DATA.items() if data["tolerance"] is not None]
TEMPCO_COLORS = [name for name, data in COLOR_DATA.items() if data["tempco"] is not None]


def convert_resistance(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:g} GΩ"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:g} MΩ"
    elif value >= 1_000:
        return f"{value / 1_000:g} kΩ"
    return f"{value:g} Ω"


def text_color(color_name):
    return "#FFFFFF" if color_name in ["검정", "갈색", "빨강", "파랑", "보라"] else "#222222"


def render_resistor(color_bands):
    band_html = ""
    for index, color_name in enumerate(color_bands, start=1):
        band_html += f"""
        <div class="resistor-band-wrap">
            <div class="resistor-band" style="background:{COLOR_DATA[color_name]['hex']};
                 {'border:1px solid #777;' if color_name == '흰색' else ''}"></div>
            <span class="band-caption">{index}번째 · {color_name}</span>
        </div>
        """

    st.markdown(
        f"""
        <style>
        .resistor-card {{
            background: linear-gradient(135deg, #f8fafc, #eef2f7);
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 22px 18px 16px;
            margin: 8px 0 18px;
            overflow: hidden;
        }}
        .resistor-stage {{
            display:flex; align-items:center; justify-content:center;
            min-height:105px; padding:8px 0 14px;
        }}
        .resistor-wire {{
            height:7px; width:12%; background:linear-gradient(#b7b7b7,#777,#c9c9c9);
            border-radius:4px;
        }}
        .resistor-body {{
            display:flex; align-items:stretch; justify-content:space-evenly;
            width:70%; height:62px; padding:0 15px;
            background:linear-gradient(180deg,#f4d9a6 0%,#e9c58b 22%,#d9ad6e 52%,#c99758 100%);
            border:1px solid #bd925e; border-radius:18px;
            box-shadow: inset 0 5px 8px rgba(255,255,255,.45),
                        inset 0 -6px 8px rgba(105,65,25,.16),
                        0 5px 10px rgba(0,0,0,.12);
            gap:9px;
        }}
        .resistor-band-wrap {{
            display:flex; flex-direction:column; align-items:center;
            justify-content:center; min-width:0; flex:1;
        }}
        .resistor-band {{
            width:100%; max-width:25px; height:62px;
            box-shadow: inset 2px 0 3px rgba(255,255,255,.25),
                        inset -2px 0 3px rgba(0,0,0,.2);
        }}
        .band-caption {{
            font-size:12px; font-weight:650; color:#334155;
            margin-top:9px; white-space:nowrap;
        }}
        .resistor-caption {{
            text-align:center; color:#64748b; font-size:12px; margin-top:3px;
        }}
        @media (max-width: 650px) {{
            .resistor-body {{ width:76%; gap:5px; padding:0 8px; }}
            .resistor-band {{ max-width:18px; }}
            .band-caption {{ font-size:10px; }}
        }}
        </style>
        <div class="resistor-card">
            <div class="resistor-stage">
                <div class="resistor-wire"></div>
                <div class="resistor-body">{band_html}</div>
                <div class="resistor-wire"></div>
            </div>
            <div class="resistor-caption">선택한 색상띠를 실제 저항처럼 표시한 모습</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_color_table():
    rows = ""
    for color_name, info in COLOR_DATA.items():
        swatch_border = "border:1px solid #999;" if color_name == "흰색" else ""
        rows += f"""
        <tr>
            <td><span class="color-chip" style="background:{info['hex']};{swatch_border}"></span>
                <b>{color_name}</b></td>
            <td>{'-' if info['digit'] is None else info['digit']}</td>
            <td>×{info['multiplier']:g}</td>
            <td>{'-' if info['tolerance'] is None else f"±{info['tolerance']:g}%"}</td>
            <td>{'-' if info['tempco'] is None else info['tempco']}</td>
        </tr>
        """

    st.markdown(
        f"""
        <style>
        .code-table {{width:100%; border-collapse:collapse; font-size:13px;}}
        .code-table th {{background:#edf2f7; color:#334155; font-weight:700;}}
        .code-table th,.code-table td {{
            padding:8px 6px; border-bottom:1px solid #e5e7eb; text-align:center;
        }}
        .code-table tr:nth-child(even) {{background:#f8fafc;}}
        .code-table td:first-child {{text-align:left; white-space:nowrap;}}
        .color-chip {{
            display:inline-block; width:17px; height:17px; border-radius:4px;
            vertical-align:middle; margin-right:7px; box-shadow:0 1px 3px #0002;
        }}
        </style>
        <table class="code-table">
            <thead><tr><th>색상</th><th>숫자</th><th>배율</th><th>허용오차</th><th>온도계수</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


st.title("🔌 저항 색상띠 계산기")
st.caption("색상띠를 선택하면 실제 저항 모양과 저항값을 함께 확인할 수 있습니다.")

input_col, result_col, table_col = st.columns([1.08, 1.0, 1.35], gap="large")

with input_col:
    st.subheader("① 색상띠 입력")
    band_count = st.radio(
        "색상띠 개수", [4, 5, 6], horizontal=True,
        format_func=lambda number: f"{number}색띠",
    )

    if band_count == 4:
        st.caption("유효숫자 2자리 · 배율 · 허용오차")
        band1 = st.selectbox("첫째 띠 · 첫 번째 숫자", DIGIT_COLORS, index=1)
        band2 = st.selectbox("둘째 띠 · 두 번째 숫자", DIGIT_COLORS, index=0)
        band3 = st.selectbox("셋째 띠 · 배율", MULTIPLIER_COLORS, index=2)
        band4 = st.selectbox("넷째 띠 · 허용오차", TOLERANCE_COLORS, index=0)
        color_bands = [band1, band2, band3, band4]
        significant = COLOR_DATA[band1]["digit"] * 10 + COLOR_DATA[band2]["digit"]
        multiplier = COLOR_DATA[band3]["multiplier"]
        tolerance = COLOR_DATA[band4]["tolerance"]
        tempco = None

    elif band_count == 5:
        st.caption("유효숫자 3자리 · 배율 · 허용오차")
        band1 = st.selectbox("첫째 띠 · 첫 번째 숫자", DIGIT_COLORS, index=1)
        band2 = st.selectbox("둘째 띠 · 두 번째 숫자", DIGIT_COLORS, index=0)
        band3 = st.selectbox("셋째 띠 · 세 번째 숫자", DIGIT_COLORS, index=0)
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
        band1 = st.selectbox("첫째 띠 · 첫 번째 숫자", DIGIT_COLORS, index=1)
        band2 = st.selectbox("둘째 띠 · 두 번째 숫자", DIGIT_COLORS, index=0)
        band3 = st.selectbox("셋째 띠 · 세 번째 숫자", DIGIT_COLORS, index=0)
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

    st.markdown("**선택한 색상띠 미리보기**")
    render_resistor(color_bands)

resistance = significant * multiplier
minimum = resistance * (1 - tolerance / 100)
maximum = resistance * (1 + tolerance / 100)

with result_col:
    st.subheader("② 계산 결과")
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#e8f8ee,#d5f2df);
                    border:1px solid #a8dfba;border-radius:16px;padding:18px 20px;
                    margin:8px 0 18px;">
            <div style="font-size:13px;color:#287344;font-weight:700;">최종 저항값</div>
            <div style="font-size:30px;font-weight:800;color:#176b39;margin:5px 0;">
                {convert_resistance(resistance)}
            </div>
            <div style="font-size:14px;color:#287344;">허용오차 ±{tolerance:g}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background:#f8fafc;border:1px solid #dbe3ec;
                    border-radius:14px;padding:15px 17px;margin:10px 0 14px;">
            <div style="font-size:16px;font-weight:750;color:#263548;margin-bottom:10px;">
                계산 과정
            </div>
        """,
        unsafe_allow_html=True,
    )

    if band_count == 4:
        calculation_lines = [
            f"유효숫자: {COLOR_DATA[band1]['digit']} × 10 + "
            f"{COLOR_DATA[band2]['digit']} = {significant}",
        ]
        multiplier_band = band3
    else:
        calculation_lines = [
            f"유효숫자: {COLOR_DATA[band1]['digit']} × 100 + "
            f"{COLOR_DATA[band2]['digit']} × 10 + "
            f"{COLOR_DATA[band3]['digit']} = {significant}",
        ]
        multiplier_band = band4

    calculation_lines.extend([
        f"배율: {multiplier_band} = ×{multiplier:g}",
        f"저항값: {significant} × {multiplier:g} = {convert_resistance(resistance)}",
    ])

    for step_number, line in enumerate(calculation_lines, start=1):
        st.markdown(
            f"""
            <div style="background:#ffffff;border:1px solid #e2e8f0;
                        border-radius:9px;padding:9px 12px;margin:6px 0;
                        color:#334155;font-size:14px;">
                <span style="color:#64748b;font-weight:700;margin-right:8px;">
                    {step_number:02d}
                </span>{line}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg,#fff8e8,#fff1d6);
                    border:1px solid #f1d49a;border-radius:14px;
                    padding:15px 17px;margin:10px 0 14px;">
            <div style="font-size:16px;font-weight:750;color:#805b16;margin-bottom:10px;">
                허용오차 범위
            </div>
            <div style="font-size:13px;color:#8a6a2b;margin-bottom:5px;">
                기준 저항값 {convert_resistance(resistance)} · 허용오차 ±{tolerance:g}%
            </div>
            <div style="font-size:14px;color:#6b4d12;line-height:1.8;">
                최솟값 <b>{convert_resistance(minimum)}</b><br>
                최댓값 <b>{convert_resistance(maximum)}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    if band_count == 6:
        st.write(f"⑤ 온도계수: **{tempco} ppm/°C**")


with table_col:
    st.subheader("③ 저항 색상 코드표")
    st.caption("색상별 숫자 · 배율 · 허용오차 · 온도계수")
    render_color_table()

