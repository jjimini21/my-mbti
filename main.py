import json
import re

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="전국 고령화 단계구분도",
    page_icon="🗺️",
    layout="wide",
)

POPULATION_URL = (
    "https://raw.githubusercontent.com/first2022-cyber/"
    "contents//main/population_ts_yearly_gender.zip"
)

GEOJSON_URL = (
    "https://raw.githubusercontent.com/first2022-cyber/"
    "contents//main/sigungu_kr.geojson"
)

TARGET_YEAR = 2026


# --------------------------------------------------
# 데이터 다운로드
# --------------------------------------------------
@st.cache_data(show_spinner="인구 데이터를 불러오는 중...")
def load_population():
    # 압축 CSV는 pandas가 직접 읽음
    df = pd.read_csv(POPULATION_URL, dtype={"코드": str})

    # 2026년 데이터만 사용
    df = df.loc[
        pd.to_numeric(df["연도"], errors="coerce") == TARGET_YEAR
    ].copy()

    # 지역 코드는 문자열로 통일하고 앞 5자리로 시군구 코드 생성
    df["코드"] = df["코드"].astype("string").str.strip()
    df["시군구코드"] = df["코드"].str[:5]

    # 계_로 시작하는 연령별 인구 열만 선택
    total_cols = [
        col for col in df.columns
        if col.startswith("계_")
    ]

    # 65세부터 100세 이상까지
    elderly_cols = [
        col for col in total_cols
        if re.fullmatch(r"계_(?:[6-9]\d|100)세(?: 이상)?", col)
        and int(re.search(r"\d+", col).group()) >= 65
    ]

    # 실제 데이터에 존재하는 65세 이상 연령 열 확인
    elderly_cols = [
        col for col in total_cols
        if (
            re.fullmatch(r"계_(?:[6-9]\d|100)세(?: 이상)?", col)
            and int(re.search(r"\d+", col).group()) >= 65
        )
    ]

    if not total_cols:
        raise ValueError("'계_'로 시작하는 인구 열을 찾을 수 없습니다.")

    if not elderly_cols:
        raise ValueError("65세 이상 인구 열을 찾을 수 없습니다.")

    # 쉼표 등으로 문자열 저장된 숫자도 처리
    for col in total_cols:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False),
            errors="coerce",
        ).fillna(0)

    # 읍면동별 인구를 시군구 코드로 집계
    df["전체인구"] = df[total_cols].sum(axis=1)
    df["65세이상인구"] = df[elderly_cols].sum(axis=1)

    result = (
        df.groupby("시군구코드", as_index=False)
        .agg(
            전체인구=("전체인구", "sum"),
            65세이상인구=("65세이상인구", "sum"),
        )
    )

    result["고령화율"] = (
        result["65세이상인구"]
        .div(result["전체인구"].where(result["전체인구"] > 0))
        .mul(100)
    )

    result = result.dropna(subset=["고령화율"])
    return result


@st.cache_data(show_spinner="시군구 경계 지도를 불러오는 중...")
def load_geojson():
    response = requests.get(GEOJSON_URL, timeout=60)
    response.raise_for_status()
    geojson = response.json()

    # 코드와 시군구 이름을 문자열로 정규화
    for feature in geojson["features"]:
        props = feature["properties"]
        props["코드"] = str(props["코드"]).strip().zfill(5)
        props["시군구"] = str(props["시군구"]).strip()
        props["시도"] = str(props["시도"]).strip()

    return geojson


# --------------------------------------------------
# 앱 화면
# --------------------------------------------------
st.title("🗺️ 전국 고령화 단계구분도")
st.caption("2026년 6월 기준 · 시군구별 65세 이상 인구 비율")

try:
    population = load_population()
    geojson = load_geojson()

    # GeoJSON의 시군구 코드를 기준으로 정확하게 결합
    geo_codes = {
        feature["properties"]["코드"]
        for feature in geojson["features"]
    }

    population["시군구코드"] = (
        population["시군구코드"].astype("string").str.zfill(5)
    )

    matched = population[
        population["시군구코드"].isin(geo_codes)
    ].copy()

    if matched.empty:
        st.error(
            "인구 데이터와 GeoJSON의 코드가 일치하지 않습니다. "
            "두 데이터의 코드 형식과 2026년 데이터 존재 여부를 확인하세요."
        )
        st.stop()

    # 데이터가 없는 시군구는 지도에서 제외
    matched_codes = set(matched["시군구코드"])

    map_geojson = {
        "type": "FeatureCollection",
        "features": [
            feature for feature in geojson["features"]
            if feature["properties"]["코드"] in matched_codes
        ],
    }

    # Plotly 지도 데이터
    fig = px.choropleth(
        matched,
        geojson=map_geojson,
        locations="시군구코드",
        featureidkey="properties.코드",
        color="고령화율",
        color_continuous_scale=[
            [0.0, "#fff7bc"],
            [0.25, "#fec44f"],
            [0.5, "#fe9929"],
            [0.75, "#ec7014"],
            [1.0, "#993404"],
        ],
        range_color=(0, 40),
        hover_name=None,
        hover_data={
            "시군구코드": False,
            "고령화율": ":.2f",
            "전체인구": ":,.0f",
            "65세이상인구": ":,.0f",
        },
        labels={
            "고령화율": "고령화율(%)",
            "전체인구": "전체 인구",
            "65세이상인구": "65세 이상 인구",
        },
    )

    # 시군구 이름은 지도 경계의 속성에서 직접 표시
    for trace in fig.data:
        trace.customdata = [
            [
                feature["properties"]["시군구"],
                feature["properties"]["시도"],
            ]
            for feature in map_geojson["features"]
        ]
        trace.hovertemplate = (
            "<b>%{customdata[1]} %{customdata[0]}</b><br>"
            "고령화율: %{z:.2f}%<br>"
            "<extra></extra>"
        )

    fig.update_geos(
        visible=False,
        fitbounds="locations",
        showcountries=False,
        showcoastlines=False,
        showland=False,
        showframe=False,
    )

    fig.update_traces(
        marker_line_color="white",
        marker_line_width=0.45,
    )

    fig.update_layout(
        height=800,
        margin=dict(l=0, r=0, t=35, b=0),
        coloraxis_colorbar=dict(
            title="고령화율(%)",
            ticksuffix="%",
        ),
        paper_bgcolor="white",
        geo=dict(
            bgcolor="white",
        ),
    )

    # 핵심 지표
    c1, c2, c3 = st.columns(3)
    c1.metric("분석 연도", f"{TARGET_YEAR}년")
    c2.metric("분석 시군구", f"{len(matched):,}개")
    c3.metric(
        "전국 평균 고령화율",
        f"{matched['65세이상인구'].sum() / matched['전체인구'].sum() * 100:.2f}%"
        if matched["전체인구"].sum() > 0
        else "계산 불가",
    )

    st.plotly_chart(fig, use_container_width=True)

    # 데이터 표
    st.subheader("시군구별 고령화율")

    table = matched.merge(
        pd.DataFrame([
            {
                "시군구코드": feature["properties"]["코드"],
                "시도": feature["properties"]["시도"],
                "시군구": feature["properties"]["시군구"],
            }
            for feature in map_geojson["features"]
        ]).drop_duplicates("시군구코드"),
        on="시군구코드",
        how="left",
    )

    table = table[
        ["시군구코드", "시도", "시군구",
         "전체인구", "65세이상인구", "고령화율"]
    ].sort_values("고령화율", ascending=False)

    st.dataframe(
        table,
        hide_index=True,
        use_container_width=True,
        column_config={
            "시군구코드": st.column_config.TextColumn("코드"),
            "전체인구": st.column_config.NumberColumn(
                "전체 인구", format="%d"
            ),
            "65세이상인구": st.column_config.NumberColumn(
                "65세 이상 인구", format="%d"
            ),
            "고령화율": st.column_config.NumberColumn(
                "고령화율(%)", format="%.2f%%"
            ),
        },
    )

    csv = table.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "CSV 다운로드",
        data=csv,
        file_name="전국_시군구별_고령화율_2026.csv",
        mime="text/csv",
    )

except requests.RequestException as e:
    st.error(f"데이터 다운로드에 실패했습니다: {e}")
except (KeyError, ValueError, TypeError) as e:
    st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")
