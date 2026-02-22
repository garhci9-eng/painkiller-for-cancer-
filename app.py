"""
app.py — 암성 통증 비마약성 신약 후보 탐색 웹 앱
실행: streamlit run app.py
"""

import io
import base64
import pandas as pd
import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# 내부 모듈
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.chembl    import search_compounds, TARGETS, TARGET_DESCRIPTIONS
from utils.molecules import calculate_descriptors, lipinski_pass, side_effect_score, mol_to_image_b64, smiles_placeholder_svg
from utils.db        import (init_db, save_compounds, log_search,
                              add_favorite, remove_favorite,
                              get_favorites, get_search_history, get_saved_compounds)

# ── 초기화 ────────────────────────────────────────────────────────────────────
init_db()
st.set_page_config(
    page_title="Cancer Pain Drug Discovery",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .metric-card {
    background: #f0f4ff;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 4px 0;
    border-left: 4px solid #4A90D9;
  }
  .score-high  { color: #27ae60; font-weight: bold; }
  .score-mid   { color: #f39c12; font-weight: bold; }
  .score-low   { color: #e74c3c; font-weight: bold; }
  .badge-pass  { background:#d4edda; color:#155724; padding:2px 8px; border-radius:12px; font-size:12px; }
  .badge-fail  { background:#f8d7da; color:#721c24; padding:2px 8px; border-radius:12px; font-size:12px; }
  .notice-box  { background:#fff3cd; border-left:4px solid #ffc107; padding:10px 14px; border-radius:6px; margin:10px 0; font-size:13px; }
  .license-box { background:#e8f4f8; border-left:4px solid #17a2b8; padding:10px 14px; border-radius:6px; margin:10px 0; font-size:12px; }
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.title("🔬 암성 통증 비마약성 신약 후보 탐색")
st.caption("ChEMBL 공개 데이터 · AI 부작용 예측 · 비오피오이드 타겟")

st.markdown("""
<div class="license-box">
⚖️ <b>저작권:</b> 사용자 아이디어 50% + Claude AI (Anthropic) 50% 공동 창작 &nbsp;|&nbsp;
<b>사용 제한:</b> 공익적 목적(학술·연구·교육·공공보건)으로만 사용 가능. 사적 이익·상업적 목적 사용 금지.
</div>
<div class="notice-box">
⚕️ <b>의료 고지:</b> 이 프로그램은 연구 참고용입니다. 실제 임상 적용 시 반드시 전문 의료·약학 전문가의 검토를 받으세요.
</div>
""", unsafe_allow_html=True)

# ── 사이드바 ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🎯 검색 설정")

    target_name = st.selectbox(
        "타겟 수용체",
        options=list(TARGETS.keys()),
        help="비마약성 암성 통증 타겟을 선택하세요.",
    )

    ic50_max = st.slider(
        "IC50 최대값 (nM)",
        min_value=10, max_value=10000, value=1000, step=10,
        help="낮을수록 강한 효능의 화합물만 탐색합니다.",
    )

    result_limit = st.slider(
        "최대 결과 수",
        min_value=10, max_value=500, value=100, step=10,
    )

    drug_score_min = st.slider(
        "최소 약물 점수",
        min_value=0.0, max_value=1.0, value=0.5, step=0.05,
        help="1에 가까울수록 부작용이 적은 후보입니다.",
    )

    lipinski_only = st.checkbox("Lipinski 통과만 표시", value=True)

    search_btn = st.button("🔍 검색 시작", type="primary", use_container_width=True)

    st.divider()
    st.markdown(f"**선택된 타겟 정보**")
    if target_name in TARGET_DESCRIPTIONS:
        st.caption(TARGET_DESCRIPTIONS[target_name])

# ── 탭 ───────────────────────────────────────────────────────────────────────
tab_search, tab_smiles, tab_saved, tab_fav, tab_history = st.tabs([
    "🔍 후보 탐색", "🧪 SMILES 분석", "💾 저장된 화합물", "⭐ 즐겨찾기", "📜 검색 기록"
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — 후보 탐색
# ════════════════════════════════════════════════════════════════════════════
with tab_search:
    if search_btn:
        with st.spinner(f"ChEMBL에서 {target_name} 화합물 검색 중..."):
            df = search_compounds(
                target_name=target_name,
                ic50_max=ic50_max,
                limit=result_limit,
                lipinski_only=lipinski_only,
            )

        if df.empty:
            st.warning("검색 결과가 없습니다. 타겟이나 IC50 범위를 조정해보세요.")
        else:
            # drug_score 필터
            df = df[df["drug_score"] >= drug_score_min]

            # DB 저장
            saved_n = save_compounds(df)
            log_search(target_name, ic50_max, len(df))

            st.session_state["last_df"]     = df
            st.session_state["last_target"] = target_name
            st.success(f"✅ {len(df)}개 후보 발견 · {saved_n}개 DB 저장 완료")

    # 결과 표시
    if "last_df" in st.session_state:
        df = st.session_state["last_df"]

        # ── 요약 지표 ─────────────────────────────────────────────────────
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("총 후보", f"{len(df)}")
        c2.metric("평균 IC50", f"{df['ic50_nM'].mean():.0f} nM")
        c3.metric("평균 약물점수", f"{df['drug_score'].mean():.2f}")
        c4.metric("Lipinski 통과", f"{df['lipinski_pass'].sum()}" if "lipinski_pass" in df else "—")
        c5.metric("평균 MW", f"{df['MW'].mean():.0f}")

        st.divider()

        # ── 상위 후보 카드 ─────────────────────────────────────────────────
        st.subheader("🏆 상위 신약 후보")
        top_n = min(6, len(df))
        cols = st.columns(3)

        for i, (_, row) in enumerate(df.head(top_n).iterrows()):
            with cols[i % 3]:
                score = row.get("drug_score", 0)
                score_class = "score-high" if score >= 0.7 else "score-mid" if score >= 0.5 else "score-low"
                badge = "badge-pass" if row.get("lipinski_pass") else "badge-fail"
                badge_text = "Lipinski ✅" if row.get("lipinski_pass") else "Lipinski ❌"

                with st.container(border=True):
                    st.markdown(f"**{row['chembl_id']}**")

                    # 분자 구조 이미지
                    img_b64 = mol_to_image_b64(row.get("smiles", ""), size=200)
                    if img_b64:
                        st.image(
                            f"data:image/png;base64,{img_b64}",
                            use_container_width=True,
                        )
                    else:
                        st.markdown(smiles_placeholder_svg(200), unsafe_allow_html=True)

                    st.markdown(f"""
                    <span class="{badge}">{badge_text}</span>
                    <span class="{score_class}" style="float:right">점수 {score:.2f}</span>
                    """, unsafe_allow_html=True)

                    st.caption(f"IC50: {row['ic50_nM']:.0f} nM | MW: {row.get('MW',0):.0f} | LogP: {row.get('LogP',0):.2f}")

                    if st.button("⭐ 즐겨찾기", key=f"fav_{row['chembl_id']}_{i}"):
                        add_favorite(row["chembl_id"])
                        st.toast(f"{row['chembl_id']} 즐겨찾기 추가!")

        st.divider()

        # ── 전체 테이블 ────────────────────────────────────────────────────
        st.subheader("📋 전체 결과 테이블")

        display_cols = ["chembl_id", "target", "ic50_nM", "MW", "LogP",
                        "TPSA", "HBD", "HBA", "drug_score", "side_effect_score",
                        "lipinski_pass", "lipinski_violations"]
        show_cols = [c for c in display_cols if c in df.columns]

        st.dataframe(
            df[show_cols].style.background_gradient(
                subset=["drug_score"], cmap="RdYlGn"
            ),
            use_container_width=True,
            height=350,
        )

        # ── CSV 다운로드 ───────────────────────────────────────────────────
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        st.download_button(
            label="📥 CSV 다운로드",
            data=csv_buf.getvalue().encode("utf-8-sig"),
            file_name=f"candidates_{target_name[:10].strip()}.csv",
            mime="text/csv",
            type="primary",
        )

        st.divider()

        # ── 분석 차트 ──────────────────────────────────────────────────────
        st.subheader("📊 분포 분석")
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))
        fig.patch.set_facecolor("#f8f9fa")

        # IC50 분포
        axes[0].hist(np.log10(df["ic50_nM"].clip(lower=0.1)), bins=30,
                     color="#4A90D9", edgecolor="white", alpha=0.85)
        axes[0].axvline(x=3, color="red", linestyle="--", alpha=0.7, label="1000 nM")
        axes[0].set_title("IC50 분포 (log₁₀ nM)", fontsize=12)
        axes[0].set_xlabel("log₁₀(IC50)")
        axes[0].legend()

        # MW vs LogP
        sc = axes[1].scatter(df["MW"], df["LogP"],
                              c=df["drug_score"], cmap="RdYlGn",
                              alpha=0.7, s=25, vmin=0, vmax=1)
        axes[1].axhline(y=5, color="red", linestyle="--", alpha=0.4, label="LogP=5")
        axes[1].axvline(x=500, color="red", linestyle="--", alpha=0.4, label="MW=500")
        axes[1].set_xlabel("분자량 (MW)")
        axes[1].set_ylabel("LogP")
        axes[1].set_title("MW vs LogP (색=약물점수)", fontsize=12)
        axes[1].legend(fontsize=8)
        plt.colorbar(sc, ax=axes[1])

        # 약물 점수 히스토그램
        axes[2].hist(df["drug_score"], bins=20,
                     color="#27ae60", edgecolor="white", alpha=0.85)
        axes[2].axvline(x=0.7, color="orange", linestyle="--", alpha=0.7, label="고품질 기준")
        axes[2].set_title("약물 점수 분포", fontsize=12)
        axes[2].set_xlabel("약물 점수")
        axes[2].legend()

        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    else:
        st.info("왼쪽 사이드바에서 타겟과 조건을 선택한 뒤 **검색 시작**을 눌러주세요.")

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — SMILES 직접 분석
# ════════════════════════════════════════════════════════════════════════════
with tab_smiles:
    st.subheader("🧪 SMILES 직접 입력 분석")
    st.caption("화합물의 SMILES 표기를 입력하면 약물유사성과 부작용 점수를 즉시 계산합니다.")

    EXAMPLES = {
        "직접 입력": "",
        "아세트아미노펜 (타이레놀)": "CC(=O)Nc1ccc(O)cc1",
        "이부프로펜":                "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
        "케토롤락":                  "OC(=O)c1cccc2C(=O)c3ccccc3N12",
        "가바펜틴":                  "NCC1(CC(=O)O)CCCCC1",
        "셀레콕시브":                "Cc1ccc(-c2cc(NS(=O)(=O)c3ccc(N)cc3)no2)cc1",
    }

    col_ex, col_in = st.columns([1, 2])
    with col_ex:
        example = st.selectbox("예시 선택", list(EXAMPLES.keys()))
    with col_in:
        smiles_input = st.text_input(
            "SMILES",
            value=EXAMPLES[example],
            placeholder="예: CC(=O)Nc1ccc(O)cc1",
        )

    if smiles_input:
        desc = calculate_descriptors(smiles_input)
        if desc is None:
            st.error("❌ 유효하지 않은 SMILES입니다.")
        else:
            passed, violations = lipinski_pass(desc)
            se = side_effect_score(desc)
            drug_sc = round(1 - se, 3)

            col_img, col_props = st.columns([1, 2])

            with col_img:
                img_b64 = mol_to_image_b64(smiles_input, size=250)
                if img_b64:
                    st.image(f"data:image/png;base64,{img_b64}", caption="분자 구조")
                else:
                    st.markdown(smiles_placeholder_svg(250), unsafe_allow_html=True)

            with col_props:
                st.markdown("#### 분자 특성")
                props = {
                    "분자량 (MW)":       f"{desc['MW']:.1f}",
                    "LogP":             f"{desc['LogP']:.2f}",
                    "수소결합 공여체(HBD)": str(desc['HBD']),
                    "수소결합 수용체(HBA)": str(desc['HBA']),
                    "극성표면적(TPSA)":  f"{desc['TPSA']:.1f} Å²",
                    "회전가능결합":       str(desc['RotBonds']),
                    "방향족 고리":        str(desc['ArRings']),
                }
                for k, v in props.items():
                    c1, c2 = st.columns([2, 1])
                    c1.caption(k)
                    c2.markdown(f"**{v}**")

            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("약물 점수", f"{drug_sc:.2f}", help="높을수록 좋음")
            c2.metric("부작용 위험", f"{se:.2f}", help="낮을수록 좋음")
            c3.metric("Lipinski", "✅ 통과" if passed else "❌ 위반")

            if violations:
                st.warning("**위반 항목:** " + " | ".join(violations))
            else:
                st.success("✅ 모든 Lipinski Rule of Five 통과")

            # 즐겨찾기 저장 버튼
            note = st.text_input("메모 (선택)", placeholder="예: Nav1.7 타겟 분석용")
            if st.button("⭐ 즐겨찾기에 저장", type="primary"):
                chembl_id = f"CUSTOM_{smiles_input[:10]}"
                add_favorite(chembl_id, note)
                st.success("즐겨찾기에 추가되었습니다.")

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — 저장된 화합물
# ════════════════════════════════════════════════════════════════════════════
with tab_saved:
    st.subheader("💾 저장된 화합물 (SQLite DB)")

    target_filter = st.selectbox(
        "타겟 필터",
        ["전체"] + list(TARGETS.keys()),
        key="saved_filter"
    )

    saved = get_saved_compounds(
        target=target_filter if target_filter != "전체" else None
    )

    if not saved:
        st.info("저장된 화합물이 없습니다. 검색을 먼저 실행하세요.")
    else:
        saved_df = pd.DataFrame(saved)
        st.markdown(f"총 **{len(saved_df)}**개 저장됨")

        st.dataframe(saved_df, use_container_width=True, height=400)

        # CSV 다운로드
        csv_all = saved_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 전체 저장 데이터 CSV 다운로드",
            data=csv_all,
            file_name="saved_compounds.csv",
            mime="text/csv",
        )

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — 즐겨찾기
# ════════════════════════════════════════════════════════════════════════════
with tab_fav:
    st.subheader("⭐ 즐겨찾기 목록")

    favs = get_favorites()
    if not favs:
        st.info("즐겨찾기가 없습니다. 후보 탐색이나 SMILES 분석에서 추가하세요.")
    else:
        for fav in favs:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 3, 1])
                col1.markdown(f"**{fav['chembl_id']}**")
                col2.caption(
                    f"타겟: {fav.get('target','—')} | "
                    f"IC50: {fav.get('ic50_nM','—')} nM | "
                    f"약물점수: {fav.get('drug_score','—')}"
                )
                if fav.get("note"):
                    st.caption(f"📝 {fav['note']}")
                if col3.button("삭제", key=f"del_{fav['chembl_id']}"):
                    remove_favorite(fav["chembl_id"])
                    st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — 검색 기록
# ════════════════════════════════════════════════════════════════════════════
with tab_history:
    st.subheader("📜 검색 기록")
    history = get_search_history(30)
    if not history:
        st.info("검색 기록이 없습니다.")
    else:
        hist_df = pd.DataFrame(history)
        st.dataframe(hist_df, use_container_width=True, height=400)

# ── 푸터 ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style="text-align:center; color:#999; font-size:12px; padding:10px 0;">
🔬 Cancer Pain Drug Discovery · 공동 창작: 사용자 50% + Claude AI (Anthropic) 50%<br>
공익적 목적(학술·연구·교육·공공보건)으로만 사용 가능 · 사적 이익·상업적 목적 사용 금지<br>
데이터 출처: <a href="https://www.ebi.ac.uk/chembl/" target="_blank">ChEMBL</a> ·
<a href="https://pubchem.ncbi.nlm.nih.gov/" target="_blank">PubChem</a>
</div>
""", unsafe_allow_html=True)
