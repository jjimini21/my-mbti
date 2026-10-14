
import streamlit as st

POKEMON = {
    "INTJ": ("뮤츠", "Mewtwo", 150, "에스퍼", "분석적 · 독립적 · 전략적",
             "깊이 생각하고 큰 그림을 설계하는 INTJ와 뛰어난 지능을 지닌 뮤츠는 잘 어울려요.\n혼자서도 목표를 향해 나아가는 모습이 닮았어요."),
    "INTP": ("메타몽", "Ditto", 132, "노말", "호기심 · 창의적 · 유연함",
             "새로운 가능성을 탐구하는 INTP처럼 메타몽은 다양한 모습으로 변신해요.\n정해진 틀에 갇히지 않는 상상력이 공통점이에요."),
    "ENTJ": ("루카리오", "Lucario", 448, "격투 · 강철", "리더십 · 결단력 · 추진력",
             "목표를 향해 적극적으로 이끄는 ENTJ와 강한 의지의 루카리오는 환상의 팀이에요.\n서로를 믿고 어려운 도전도 함께 해낼 것 같아요."),
    "ENTP": ("개굴닌자", "Greninja", 658, "물 · 악", "재치 · 도전 정신 · 순발력",
             "아이디어가 넘치고 새로운 시도를 즐기는 ENTP처럼 개굴닌자는 빠르고 기민해요.\n예상 밖의 상황도 재치 있게 해결하는 단짝이에요."),
    "INFJ": ("가디안", "Gardevoir", 282, "에스퍼 · 페어리", "공감 · 통찰력 · 다정함",
             "다른 사람의 마음을 깊이 헤아리는 INFJ와 소중한 이를 지키는 가디안은 잘 어울려요.\n말하지 않아도 마음을 이해해 주는 친구가 될 거예요."),
    "INFP": ("이브이", "Eevee", 133, "노말", "상상력 · 따뜻함 · 개성",
             "자신만의 가치와 가능성을 소중히 여기는 INFP에게 이브이는 꼭 맞는 친구예요.\n여러 모습으로 성장할 수 있다는 점도 닮았어요."),
    "ENFJ": ("피카츄", "Pikachu", 25, "전기", "친화력 · 열정 · 팀워크",
             "주변에 활기를 전하고 친구들을 챙기는 ENFJ와 밝고 용감한 피카츄는 찰떡궁합이에요.\n함께라면 팀의 분위기를 따뜻하게 만들어 줄 거예요."),
    "ENFP": ("푸린", "Jigglypuff", 39, "노말 · 페어리", "활발함 · 표현력 · 낙천적",
             "즐거운 에너지를 나누는 ENFP와 노래하는 푸린은 잘 맞아요.\n평범한 하루도 신나는 추억으로 바꿔 줄 단짝이에요."),
    "ISTJ": ("꼬부기", "Squirtle", 7, "물", "책임감 · 성실함 · 차분함",
             "맡은 일을 꾸준히 해내는 ISTJ처럼 꼬부기는 믿음직하고 침착해요.\n서두르지 않고 차근차근 성장하는 여정을 함께할 수 있어요."),
    "ISFJ": ("해피너스", "Blissey", 242, "노말", "배려심 · 헌신 · 안정감",
             "주변을 세심하게 살피는 ISFJ와 다른 이를 보살피는 해피너스는 닮았어요.\n곁에 있는 것만으로도 안심이 되는 포근한 친구예요."),
    "ESTJ": ("윈디", "Arcanine", 59, "불꽃", "책임감 · 추진력 · 든든함",
             "책임 있게 앞장서는 ESTJ와 용맹하고 충직한 윈디는 믿음직한 조합이에요.\n서로를 지키며 목표를 향해 나아갈 수 있어요."),
    "ESFJ": ("치라미", "Minccino", 572, "노말", "친절함 · 사교적 · 꼼꼼함",
             "주변을 살뜰히 챙기는 ESFJ와 치라미는 잘 어울려요.\n작은 부분까지 신경 쓰는 모습이 모두를 기분 좋게 해 줄 거예요."),
    "ISTP": ("메타그로스", "Metagross", 376, "강철 · 에스퍼", "실용적 · 침착함 · 분석적",
             "상황을 냉정하게 파악하고 직접 해결하는 ISTP와 메타그로스는 잘 맞아요.\n복잡한 문제도 차분하게 분석하는 파트너가 될 거예요."),
    "ISFP": ("나룸퍼프", "Swirlix", 684, "페어리", "감각적 · 온화함 · 자유로움",
             "자기만의 감성과 평화로운 분위기를 아끼는 ISFP에게 나룸퍼프가 어울려요.\n부담 없이 곁을 지키며 소소한 행복을 함께 누릴 수 있어요."),
    "ESTP": ("리자몽", "Charizard", 6, "불꽃 · 비행", "대담함 · 행동력 · 모험심",
             "직접 부딪치며 경험하는 ESTP와 대담한 리자몽은 멋진 콤비예요.\n새로운 모험 앞에서도 함께 도전할 수 있어요."),
    "ESFP": ("파치리스", "Pachirisu", 417, "전기", "밝음 · 사교적 · 활기",
             "사람들과 어울리며 즐거움을 나누는 ESFP와 활기찬 파치리스는 금세 친해질 거예요.\n함께 있으면 주변까지 웃음으로 채우는 단짝이에요."),
}

st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;700;900&display=swap');

.stApp {
    background: linear-gradient(180deg, #fff9e9, #fff0c2);
    color: #493923;
}
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.block-container {
    max-width: 850px;
    padding-top: 2rem;
}
.hero {
    text-align: center;
    background: #fffdf6;
    border: 2px solid #ffe49a;
    border-radius: 26px;
    padding: 28px 15px;
    box-shadow: 0 7px 0 #f6d783;
}
.hero h1 {
    font-family: 'Jua', sans-serif;
    font-size: clamp(2rem, 6vw, 3.2rem);
    color: #8b5c13;
}
.hero p {
    font-size: 1.1rem;
}
.section-title {
    font-family: 'Jua', sans-serif;
    color: #7a5013;
    font-size: 1.6rem;
    margin-top: 1.5rem;
}
div.stButton > button {
    background: #fffdf6;
    color: #5a431d;
    border: 2px solid #f2d47b;
    border-radius: 14px;
    min-height: 3.2rem;
    font-size: 1.05rem;
    font-weight: 900;
}
div.stButton > button:hover {
    background: #ffe68b;
    border-color: #eab83f;
    color: #53380b;
}
.result {
    background: #fffdf6;
    border: 2px solid #f7d77f;
    border-radius: 24px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 7px 0 #f4d27a;
}
.poke-name {
    font-family: 'Jua', sans-serif;
    color: #7a5013;
    font-size: 2rem;
}
.pill {
    display: inline-block;
    background: #fff0b7;
    border-radius: 30px;
    padding: 8px 12px;
    margin: 4px;
    font-weight: 700;
}
.reason {
    white-space: pre-line;
    text-align: left;
    line-height: 1.9;
    background: #fff7df;
    border-radius: 15px;
    padding: 16px;
    margin-top: 16px;
}
.footer {
    text-align: center;
    color: #8c774e;
    margin-top: 30px;
    font-size: .9rem;
}
</style>

<div class="hero">
    <div>✨ 나와 찰떡궁합인 포켓몬은?</div>
    <h1>MBTI 단짝 포켓몬 찾기</h1>
    <p>나의 성격 유형을 고르고 운명의 파트너를 만나 봐!</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">🌼 1. 내 MBTI를 선택해 줘!</div>',
    unsafe_allow_html=True
)
st.caption("아래 16가지 유형 중 하나를 눌러 주세요.")

types = list(POKEMON.keys())

for start in range(0, 16, 4):
    cols = st.columns(4)
    for col, mbti in zip(cols, types[start:start + 4]):
        with col:
            if st.button(mbti, key=mbti, use_container_width=True):
                st.session_state["selected_mbti"] = mbti

selected = st.session_state.get("selected_mbti")

if selected:
    ko, en, number, poke_type, traits, reason = POKEMON[selected]

    st.balloons()

    st.markdown(
        '<div class="section-title">🎉 2. 너의 단짝 포켓몬을 찾았어!</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="result">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="pill">💛 {selected}의 BEST FRIEND</div>',
        unsafe_allow_html=True
    )

    image_url = (
        "https://raw.githubusercontent.com/PokeAPI/sprites/"
        f"master/sprites/pokemon/other/official-artwork/{number}.png"
    )

    st.image(image_url, width=280)

    st.markdown(
        f'<div class="poke-name">{ko} ({en})</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<span class="pill">타입: {poke_type}</span>'
        f'<span class="pill">특징: {traits}</span>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="reason"><b>💌 우리가 잘 어울리는 이유</b><br>'
        + reason.replace("\n", "<br>")
        + '</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    if st.button("🔄 다른 MBTI도 찾아보기", use_container_width=True):
        del st.session_state["selected_mbti"]
        st.rerun()

else:
    st.info("💡 MBTI 버튼을 누르면 단짝 포켓몬이 나타나요!")

st.markdown("""
<div class="footer">
    이 결과는 재미를 위한 성격 궁합 콘텐츠예요. 💛<br>
    포켓몬 이미지를 표시하려면 인터넷 연결이 필요해요.
</div>
""", unsafe_allow_html=True)
